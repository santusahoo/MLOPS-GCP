pipeline{
    agent any
    stages{
        stage('Cloning github repo to Jenkins workspace'){
            steps{
                echo 'Cloning the repo'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/santusahoo/MLOPS-GCP.git']])
    }
}