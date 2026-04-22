pipeline {
    agent any
    environment {
        DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')  // ID from Jenkins creds
        IMAGE_NAME = 'yourusername/vehicle-insurance:latest'  // Change 'yourusername' to Docker Hub username
    }
    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/yourusername/vehicle-insurance-complete_pipeline_project.git', branch: 'main'  // Update repo URL
            }
        }
        stage('Lint & Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pylint src/ || true'  // Optional lint
                sh 'python -m pytest src/ || true'  // Add tests if exist
            }
        }
        stage('Build Docker') {
            steps {
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }
        stage('Push to Docker Hub') {
            steps {
                sh 'echo $DOCKER_HUB_CREDENTIALS_PSW | docker login -u $DOCKER_HUB_CREDENTIALS_USR --password-stdin'
                sh 'docker push ${IMAGE_NAME}'
            }
        }
        stage('Deploy Local') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker stop vehicle-app || true'
                sh 'docker rm vehicle-app || true'
                sh 'docker run -d -p 5000:5000 --name vehicle-app -e MONGODB_URL=${MONGODB_URL} ${IMAGE_NAME}'
            }
        }
    }
    post {
        always {
            sh 'docker logout'
        }
    }
}

