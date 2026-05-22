pipeline {
    agent any   
    environment {
        DOCKERHUB_USER = "vikasvikky56"
        IMAGE_NAME = "vehicle-insurance"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }


    stages {

        stage('Install + Test') {
            agent {
                docker {
                    image 'python:3.10'
                    args '-u root:root'
                }
            }
            steps {
                sh '''
                pip install --upgrade pip
                pip install -r requirements.txt --timeout 100 --retries 5
                ruff check . || true
                pytest -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG .
                docker tag $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG $DOCKERHUB_USER/$IMAGE_NAME:latest
                docker images
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG
                    docker push $DOCKERHUB_USER/$IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                sed -i "s|IMAGE_TAG|$IMAGE_TAG|g" k8s/deployment.yaml
                kubectl apply -f k8s/deployment.yaml
                '''
            }
        }
    }
}