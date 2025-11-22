pipeline {
  agent any

  environment {
    VENV_DIR = 'venv'
    GCP_PROJECT = 'wise-hub-478710-q8'
    CLOUDSDK_CORE_DISABLE_PROMPTS = '1'   // avoid interactive prompts
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
          # On Debian images you may need: apt-get update && apt-get install -y python3-venv
          python3 -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          elif [ -f pyproject.toml ] || [ -f setup.py ]; then
            pip install -e .
          else
            echo "No dependency files; skipping."
          fi
        '''
      }
    }

    stage('Build & Push to GCR') {
      steps {
        withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          sh '''
            set -eux
            # Ensure gcloud exists (install it in your agent image or PATH). On Debian package it’s /usr/bin/gcloud.
            gcloud --version

            gcloud auth activate-service-account --key-file="${GOOGLE_APPLICATION_CREDENTIALS}"
            gcloud config set project "${GCP_PROJECT}"

            # Configure Docker auth for GCR (scope only gcr.io)
            gcloud auth configure-docker gcr.io --quiet

            IMAGE="gcr.io/${GCP_PROJECT}/mlops-gcp:latest"
            docker build -t "${IMAGE}" .
            docker push "${IMAGE}"
          '''
        }
      }
    }

    stage('Deploy to Google Cloud Run') {
      steps {
        withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
          sh '''
            set -eux
            # Ensure gcloud exists (install it in your agent image or PATH). On Debian package it’s /usr/bin/gcloud.
            gcloud --version

            gcloud auth activate-service-account --key-file="${GOOGLE_APPLICATION_CREDENTIALS}"
            gcloud config set project "${GCP_PROJECT}"

            gcloud run deploy mlops-gcp \
              --image gcr.io/${GCP_PROJECT}/mlops-gcp:latest \
              --platform managed \
              --region us-central1 \
              --allow-unauthenticated \
              --quiet
          '''
        }
      }
    }
  }
}
