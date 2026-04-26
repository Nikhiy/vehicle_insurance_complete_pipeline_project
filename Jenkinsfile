pipeline {
    agent {
    docker {
        image 'python:3.10'
        args '-u root:root'
    }
}

    environment {
        DOCKERHUB_USER = "vikasvikky56"
        IMAGE_NAME = "vehicle-insurance"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        // stage('Checkout') {
        //     steps {
        //         git 'https://github.com/Vikas-N-2006/vehicle_insurance_complete_pipeline_project.git'
        //     }
        // }

        stage('Install Dependencies') {
            steps {
                sh '''
                pip install --upgrade pip
                pip install -r requirements.txt --timeout 100 --retries 5 \
                -i https://pypi.org/simple
                '''
            }
        }

        stage('Lint') {
            steps {
                sh 'ruff check . || true'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest -q'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                git checkout k8s/deployment.yaml
                sed -i "s|IMAGE_TAG|$IMAGE_TAG|g" k8s/deployment.yaml
                kubectl apply -f k8s/deployment.yaml
                '''
            }
        }
    }
}