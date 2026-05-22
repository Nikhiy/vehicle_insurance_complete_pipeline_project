pipeline {

    agent any

    environment {
        DOCKERHUB_USER = "vikasvikky56"
        IMAGE_NAME = "vehicle-insurance"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                sh '''
                rm -rf .pytest_cache
                rm -rf .ruff_cache
                rm -rf logs
                find . -type d -name "__pycache__" -exec rm -rf {} +
                find . -type d -name "*.egg-info" -exec rm -rf {} +
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --break-system-packages --upgrade pip
                    python3 -m pip install --break-system-packages \
                    -r requirements.txt --quiet
                '''
            }
        }

        stage('Quality Checks') {

            parallel {

                stage('Lint') {
                    steps {
                        sh 'ruff check . || true'
                    }
                }

                stage('Tests') {
                    steps {
                        sh 'pytest -q'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG .
                docker tag $DOCKERHUB_USER/$IMAGE_NAME:$IMAGE_TAG $DOCKERHUB_USER/$IMAGE_NAME:latest
                '''
            }
        }

        stage('Push Docker Image') {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: 'docker-hub-credentials',
                        usernameVariable: 'USER',
                        passwordVariable: 'PASS'
                    )
                ]) {

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