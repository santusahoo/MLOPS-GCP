pipeline {
  agent any

  stages {
    stage('Cloning github repo to Jenkins workspace') {
      steps {
        echo 'Cloning the repo'
        // EITHER use the simple 'git' step:
        git branch: 'main',
            url: 'https://github.com/santusahoo/MLOPS-GCP.git',
            credentialsId: 'github-token'

        // OR keep your original checkout (comment the other one out):
        // checkout([$class: 'GitSCM',
        //           branches: [[name: '*/main']],
        //           extensions: [],
        //           userRemoteConfigs: [[credentialsId: 'github-token',
        //                                url: 'https://github.com/santusahoo/MLOPS-GCP.git']]])
      }
    }
  }
}
