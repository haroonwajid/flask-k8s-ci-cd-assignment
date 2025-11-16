pipeline {
    agent any
    
    environment {
        // Docker configuration
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE_NAME = 'flask-app'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_FULL_IMAGE = "${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG}"
        DOCKER_LATEST_IMAGE = "${DOCKER_IMAGE_NAME}:latest"
        
        // Kubernetes configuration
        K8S_NAMESPACE = 'default'
        K8S_DEPLOYMENT = 'flask-app'
        K8S_CONFIG_PATH = 'kubernetes/'
        
        // Git configuration
        GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        BUILD_TIMESTAMP = sh(script: "date '+%Y-%m-%d_%H-%M-%S'", returnStdout: true).trim()
    }
    
    options {
        // Keep only last 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // Timeout after 30 minutes
        timeout(time: 30, unit: 'MINUTES')
        // Add timestamps to console output
        timestamps()
    }
    
    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "=== Checking out code from Git ==="
                    echo "Branch: ${BRANCH_NAME ?: 'N/A'}"
                    echo "Commit: ${GIT_COMMIT_SHORT}"
                    echo "Build Number: ${BUILD_NUMBER}"
                }
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo "=========================================="
                    echo "STAGE 1: Build Docker Image"
                    echo "=========================================="
                    
                    try {
                        echo "Building Docker image: ${DOCKER_FULL_IMAGE}"
                        
                        // Build Docker image
                        sh """
                            docker build \
                                --tag ${DOCKER_FULL_IMAGE} \
                                --tag ${DOCKER_LATEST_IMAGE} \
                                --label "build.number=${BUILD_NUMBER}" \
                                --label "build.timestamp=${BUILD_TIMESTAMP}" \
                                --label "git.commit=${GIT_COMMIT_SHORT}" \
                                .
                        """
                        
                        echo "✓ Docker image built successfully"
                        
                        // List the built images
                        echo "\nBuilt images:"
                        sh "docker images | grep ${DOCKER_IMAGE_NAME}"
                        
                        // Optional: Push to registry (requires credentials configured)
                        echo "\nSkipping push to registry (configure credentials in Jenkins for production)"
                        
                    } catch (Exception e) {
                        echo "✗ Failed to build Docker image: ${e.message}"
                        error("Docker build failed")
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "=========================================="
                    echo "STAGE 2: Deploy to Kubernetes"
                    echo "=========================================="
                    
                    try {
                        echo "Deploying manifests from: ${K8S_CONFIG_PATH}"
                        
                        // Check if kubectl is available
                        sh "kubectl version --client"
                        
                        // Apply Kubernetes manifests
                        echo "\nApplying Kubernetes manifests..."
                        sh """
                            kubectl apply -f ${K8S_CONFIG_PATH}deployment.yaml
                            kubectl apply -f ${K8S_CONFIG_PATH}service.yaml
                        """
                        
                        echo "✓ Kubernetes manifests applied successfully"
                        
                        // List deployed resources
                        echo "\nDeployed resources:"
                        sh "kubectl get deployments -n ${K8S_NAMESPACE}"
                        sh "kubectl get services -n ${K8S_NAMESPACE}"
                        sh "kubectl get pods -n ${K8S_NAMESPACE}"
                        
                    } catch (Exception e) {
                        echo "✗ Failed to deploy to Kubernetes: ${e.message}"
                        error("Kubernetes deployment failed")
                    }
                }
            }
        }
        
        stage('Verify Deployment') {
            steps {
                script {
                    echo "=========================================="
                    echo "STAGE 3: Verify Deployment"
                    echo "=========================================="
                    
                    try {
                        echo "Verifying deployment status..."
                        
                        // Wait for rollout to complete
                        echo "\nWaiting for rollout to complete (timeout: 5 minutes)..."
                        sh """
                            kubectl rollout status deployment/${K8S_DEPLOYMENT} \
                                -n ${K8S_NAMESPACE} \
                                --timeout=5m
                        """
                        
                        echo "✓ Rollout completed successfully"
                        
                        // Verify pods are running
                        echo "\nVerifying pod status..."
                        sh """
                            echo "Pods in ${K8S_NAMESPACE} namespace:"
                            kubectl get pods -n ${K8S_NAMESPACE} -o wide
                            
                            echo "\nPod details:"
                            kubectl describe pods -n ${K8S_NAMESPACE} -l app=${K8S_DEPLOYMENT}
                        """
                        
                        // Verify services
                        echo "\nVerifying service status..."
                        sh """
                            echo "Services in ${K8S_NAMESPACE} namespace:"
                            kubectl get services -n ${K8S_NAMESPACE} -o wide
                            
                            echo "\nEndpoints:"
                            kubectl get endpoints -n ${K8S_NAMESPACE}
                        """
                        
                        // Verify deployment configuration
                        echo "\nVerifying deployment configuration..."
                        sh """
                            echo "Deployment details:"
                            kubectl describe deployment ${K8S_DEPLOYMENT} -n ${K8S_NAMESPACE}
                            
                            echo "\nDeployment strategy:"
                            kubectl get deployment ${K8S_DEPLOYMENT} -n ${K8S_NAMESPACE} -o jsonpath='{.spec.strategy}'
                            echo ""
                            
                            echo "\nReplica status:"
                            kubectl get deployment ${K8S_DEPLOYMENT} -n ${K8S_NAMESPACE} -o jsonpath='{.status.replicas}' | xargs -I {} echo "Desired: {}"
                            kubectl get deployment ${K8S_DEPLOYMENT} -n ${K8S_NAMESPACE} -o jsonpath='{.status.updatedReplicas}' | xargs -I {} echo "Updated: {}"
                            kubectl get deployment ${K8S_DEPLOYMENT} -n ${K8S_NAMESPACE} -o jsonpath='{.status.readyReplicas}' | xargs -I {} echo "Ready: {}"
                            kubectl get deployment ${K8S_DEPLOYMENT} -n ${K8S_NAMESPACE} -o jsonpath='{.status.availableReplicas}' | xargs -I {} echo "Available: {}"
                        """
                        
                        // Check probe status
                        echo "\nChecking probe status..."
                        sh """
                            kubectl get pods -n ${K8S_NAMESPACE} -l app=${K8S_DEPLOYMENT} -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.conditions[?(@.type=="Ready")].status}{"\n"}{end}'
                        """
                        
                        echo "✓ Deployment verification completed successfully"
                        echo "\n✓✓✓ ALL STAGES COMPLETED SUCCESSFULLY ✓✓✓"
                        
                    } catch (Exception e) {
                        echo "✗ Deployment verification failed: ${e.message}"
                        error("Deployment verification failed")
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo "=========================================="
            echo "POST BUILD: Cleaning up and Reporting"
            echo "=========================================="
            
            script {
                // Generate summary
                sh """
                    echo "\n=== Final Status Summary ==="
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "Build Timestamp: ${BUILD_TIMESTAMP}"
                    echo "Git Commit: ${GIT_COMMIT_SHORT}"
                    echo "Docker Image: ${DOCKER_FULL_IMAGE}"
                    echo "Kubernetes Namespace: ${K8S_NAMESPACE}"
                    echo "Kubernetes Deployment: ${K8S_DEPLOYMENT}"
                    
                    echo "\n=== Final Pod Status ==="
                    kubectl get pods -n ${K8S_NAMESPACE} -l app=${K8S_DEPLOYMENT}
                    
                    echo "\n=== Final Service Status ==="
                    kubectl get services -n ${K8S_NAMESPACE}
                """
            }
        }
        
        success {
            echo "✓ Pipeline completed successfully!"
            echo "Access the application at: http://localhost:30080/"
        }
        
        failure {
            echo "✗ Pipeline failed! Check logs above for details."
            // Optional: Send notifications (email, Slack, etc.)
        }
        
        unstable {
            echo "⚠ Pipeline unstable. Check for warnings in logs."
        }
    }
}
