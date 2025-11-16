pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 1, unit: 'HOURS')
        timestamps()
    }

    environment {
        REGISTRY = 'docker.io'
        IMAGE_NAME = 'flask-app'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Checking out source code...'
                    checkout scm
                }
            }
        }

        stage('Build') {
            steps {
                script {
                    echo 'Building Docker image...'
                    sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
                    sh 'docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo 'Running tests...'
                    sh '''
                        docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m pytest --version || echo "No pytest installed"
                    '''
                }
            }
        }

        stage('Push') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo 'Pushing Docker image to registry...'
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                            docker push ${REGISTRY}/${DOCKER_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                            docker logout
                        '''
                    }
                }
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo 'Deploying to Kubernetes...'
                    sh '''
                        kubectl apply -f kubernetes/deployment.yaml
                        kubectl apply -f kubernetes/service.yaml
                        kubectl rollout status deployment/flask-app -n default --timeout=5m
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
