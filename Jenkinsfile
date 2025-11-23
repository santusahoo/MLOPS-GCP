pipeline {
  agent any

  environment {
    VENV_DIR   = 'venv'
    GCP_PROJECT = 'wise-hub-478710-q8'
    REGION      = 'us-central1'
    SERVICE     = 'mlops-gcp'
    IMAGE       = "gcr.io/${GCP_PROJECT}/mlops-gcp:latest"
    CLOUDSDK_CORE_DISABLE_PROMPTS = '1'
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: 'main',
            url: 'https://github.com/santusahoo/MLOPS-GCP.git',
            credentialsId: 'github-token'
      }
    }

    stage('Python venv & deps') {
      steps {
        sh '''
          set -eux
          python3 --version
          command -v pip3 || true
          python3 -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          fi
        '''
      }
    }

    stage('Buildx: Build & Push (amd64 + arm64)') {
      steps {
        withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          sh '''
            set -eux
            gcloud --version

            gcloud auth activate-service-account --key-file="${GOOGLE_APPLICATION_CREDENTIALS}"
            gcloud config set project "${GCP_PROJECT}"
            gcloud auth configure-docker gcr.io --quiet

            docker run --privileged --rm tonistiigi/binfmt --install all || true

            docker buildx create --name xbuilder --use || docker buildx use xbuilder
            docker buildx inspect --bootstrap

            docker buildx build \
              --platform linux/amd64,linux/arm64 \
              -t "${IMAGE}" \
              --push \
              .

            docker buildx imagetools inspect "${IMAGE}"
          '''
        }
      }
    }

    stage('Deploy to Google Cloud Run') {
    steps {
        withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
        sh '''
            set -eux
            gcloud --version

            gcloud auth activate-service-account --key-file="${GOOGLE_APPLICATION_CREDENTIALS}"
            gcloud config set project "${GCP_PROJECT}"

            gcloud run deploy "${SERVICE}" \
            --image "${IMAGE}" \
            --platform managed \
            --region "${REGION}" \
            --allow-unauthenticated \
            --timeout 300 \
            --cpu 2 \
            --memory 2Gi \
            --quiet
        '''
        }
    }
    }
  }

  post {
    always {
      sh 'docker buildx rm xbuilder || true'
    }
  }
}