pipeline {
  agent any

  environment {
    VENV_DIR = 'venv'
  }

  stages {
    stage('Cloning github repo to Jenkins workspace') {
      steps {
        echo 'Cloning the repo'
        git branch: 'main',
            url: 'https://github.com/santusahoo/MLOPS-GCP.git',
            credentialsId: 'github-token'
      }
    }

    stage('Setting up Python Virtual Environment and installing dependencies') {
      steps {
        echo 'Setting up Python Virtual Environment'
        sh """
          python3 --version
          pip3 --version || true
          python3 -m venv ${VENV_DIR}
          . ${VENV_DIR}/bin/activate
          pip install --upgrade pip
          if [ -f requirements.txt ]; then
            pip install -r requirements.txt
          elif [ -f pyproject.toml ] || [ -f setup.py ]; then
            pip install -e .
          else
            echo "No requirements.txt / setup.py / pyproject.toml found; skipping installs."
          fi
        """
      }
    }
  }
}
