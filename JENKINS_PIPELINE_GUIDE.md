# Jenkins Kubernetes Pipeline Documentation

## Overview

This document describes the Jenkins Declarative Pipeline configured in `Jenkinsfile` for building Docker images and deploying Flask applications to Kubernetes.

## Pipeline Architecture

### Three Main Stages

#### **Stage 1: Build Docker Image**
- Builds a Docker image from the Dockerfile
- Tags the image with build number and "latest" tag
- Adds build metadata as labels (build number, timestamp, git commit)
- Displays the built images
- Ready for optional push to Docker registry

**Key Commands:**
```bash
docker build \
    --tag flask-app:${BUILD_NUMBER} \
    --tag flask-app:latest \
    --label "build.number=${BUILD_NUMBER}" \
    --label "build.timestamp=${BUILD_TIMESTAMP}" \
    --label "git.commit=${GIT_COMMIT_SHORT}" \
    .
```

#### **Stage 2: Deploy to Kubernetes**
- Verifies kubectl availability
- Applies Kubernetes Deployment manifest
- Applies Kubernetes Service manifest(s)
- Lists deployed resources (deployments, services, pods)

**Key Commands:**
```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl get deployments -n default
kubectl get services -n default
kubectl get pods -n default
```

#### **Stage 3: Verify Deployment**
- Waits for rollout to complete (5-minute timeout)
- Verifies all pods are running and ready
- Checks service endpoints
- Displays deployment configuration and strategy
- Reports replica status (desired, updated, ready, available)
- Verifies probe status (liveness, readiness)

**Key Commands:**
```bash
kubectl rollout status deployment/flask-app -n default --timeout=5m
kubectl get pods -n default -o wide
kubectl describe deployment flask-app -n default
kubectl get services -n default -o wide
```

## Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `DOCKER_REGISTRY` | docker.io | Docker registry URL |
| `DOCKER_IMAGE_NAME` | flask-app | Application image name |
| `DOCKER_IMAGE_TAG` | ${BUILD_NUMBER} | Build-specific tag |
| `DOCKER_FULL_IMAGE` | flask-app:${BUILD_NUMBER} | Full image name with tag |
| `DOCKER_LATEST_IMAGE` | flask-app:latest | Latest image tag |
| `K8S_NAMESPACE` | default | Kubernetes namespace |
| `K8S_DEPLOYMENT` | flask-app | Deployment name |
| `K8S_CONFIG_PATH` | kubernetes/ | Path to manifests |
| `GIT_COMMIT_SHORT` | (from git) | Short commit hash |
| `BUILD_TIMESTAMP` | (generated) | Build timestamp |

## Jenkins Configuration

### Prerequisites

Before running the pipeline, ensure:

1. **Jenkins Installation**
   - Jenkins server is running and accessible
   - Jenkins has appropriate permissions

2. **Required Plugins**
   - Pipeline plugin (usually pre-installed)
   - Docker plugin (for Docker integration)
   - Kubernetes CLI plugin (for kubectl)

3. **System Requirements**
   - Docker installed and accessible to Jenkins
   - kubectl installed and configured
   - kubeconfig file configured for cluster access

4. **GitHub Integration** (Optional)
   - GitHub credentials configured in Jenkins
   - Webhook set up for automated builds

### Jenkins Setup Steps

#### 1. Install Required Plugins

Go to **Manage Jenkins** → **Manage Plugins** → **Available**

Search and install:
- Pipeline
- Docker
- Kubernetes CLI
- GitHub Integration (optional)
- AnsiColor (for colored output)

#### 2. Configure System Settings

Go to **Manage Jenkins** → **Configure System**

**Docker Configuration:**
- Ensure Docker daemon is accessible
- Test with: `docker ps` command

**Kubernetes Configuration:**
- Ensure kubeconfig is properly configured
- Test with: `kubectl get nodes` command

#### 3. Create Pipeline Job

1. Click **New Item**
2. Enter job name (e.g., "flask-k8s-pipeline")
3. Select **Pipeline**
4. Click **OK**

#### 4. Pipeline Configuration

In the pipeline job:

**General Section:**
- Check "GitHub project" (if using GitHub)
- Enter project URL

**Build Triggers:**
- Check "GitHub hook trigger for GITscm polling" (for webhook)
- Or check "Poll SCM" with schedule (optional)

**Pipeline Section:**
- Select "Pipeline script from SCM"
- SCM: Git
- Repository URL: `https://github.com/haroonwajid/flask-k8s-ci-cd-assignment.git`
- Credentials: Configure GitHub credentials
- Branches to build: `*/feature/jenkins-k8s-pipeline`
- Script path: `Jenkinsfile`

### Manual Pipeline Execution

1. Open the pipeline job in Jenkins
2. Click **Build Now**
3. Monitor the build in **Build History**
4. Click on build number to view console output

### Viewing Pipeline Progress

**Real-time Monitoring:**
1. Click on the active build
2. View **Console Output**
3. Stages display with color coding:
   - 🟢 Green = Passed
   - 🔴 Red = Failed
   - 🟡 Yellow = In Progress

## Error Handling and Troubleshooting

### Common Issues

#### Issue: Docker build fails
**Solution:**
- Verify Docker is running: `docker ps`
- Check Dockerfile syntax
- Check build context includes required files

#### Issue: kubectl not found
**Solution:**
- Install kubectl: `curl -LO https://dl.k8s.io/release/stable.txt`
- Add to PATH
- Verify: `kubectl version --client`

#### Issue: Kubernetes deployment fails
**Solution:**
- Verify kubeconfig: `kubectl config view`
- Check cluster access: `kubectl get nodes`
- Check manifests: `kubectl apply --dry-run=client -f kubernetes/`
- Check service account permissions

#### Issue: Rollout status timeout
**Solution:**
- Check pod logs: `kubectl logs -l app=flask-app`
- Increase timeout in Jenkinsfile if needed
- Verify resource requests are available

### Debug Mode

To enable verbose output, add to pipeline steps:

```groovy
sh 'set -x'  // Enable debug mode
sh 'kubectl apply -f kubernetes/'
sh 'set +x'  // Disable debug mode
```

## Security Considerations

### Credentials Management

For production deployments with Docker registry push:

1. **Store Docker Credentials in Jenkins:**
   - Go to **Credentials** → **System** → **Global credentials**
   - Click **Add Credentials**
   - Select **Username with password**
   - Enter Docker Hub credentials
   - Set ID: `docker-hub-credentials`

2. **Use Credentials in Pipeline:**
```groovy
withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', 
                                   usernameVariable: 'DOCKER_USER', 
                                   passwordVariable: 'DOCKER_PASS')]) {
    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
}
```

### RBAC and Permissions

For Kubernetes:
- Ensure Jenkins service account has permissions to deploy
- Check role bindings: `kubectl get rolebindings`
- Verify namespace access: `kubectl auth can-i create deployments --namespace=default`

## Pipeline Artifacts and Logs

### Build Artifacts

Store pipeline outputs by adding:
```groovy
post {
    always {
        // Archive pipeline logs
        archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
    }
}
```

### Log Retention

Configured in pipeline:
```groovy
buildDiscarder(logRotator(numToKeepStr: '10'))
```

Keeps last 10 builds and their logs.

## Advanced Configuration

### Conditional Stages

Deploy only on main branch:
```groovy
stage('Deploy') {
    when {
        branch 'main'
    }
    steps {
        // deployment steps
    }
}
```

### Parallel Stages

For faster execution:
```groovy
parallel {
    stage('Build Docker') {
        // build steps
    }
    stage('Run Tests') {
        // test steps
    }
}
```

### Post Actions

Send notifications after build:
```groovy
post {
    success {
        emailext(subject: 'Build Successful',
                 body: 'Pipeline completed successfully',
                 to: 'team@example.com')
    }
    failure {
        emailext(subject: 'Build Failed',
                 body: 'Pipeline failed. Check logs.',
                 to: 'team@example.com')
    }
}
```

## Useful Commands

### Local Testing

Test Jenkinsfile syntax before committing:
```bash
# Validate with Jenkins CLI
java -jar jenkins-cli.jar declarative-linter < Jenkinsfile

# Or validate online
# https://www.jenkins.io/doc/book/pipeline/declarative/syntax-check/
```

### Manual Testing

Test individual pipeline steps:
```bash
# Build image
docker build -t flask-app:latest .

# Apply manifests
kubectl apply -f kubernetes/

# Check rollout
kubectl rollout status deployment/flask-app -n default --timeout=5m

# Verify pods
kubectl get pods -n default
```

## Monitoring and Metrics

### Pipeline Metrics

Track in Jenkins:
- Build duration
- Build success rate
- Deployment frequency
- Lead time for changes

### Kubernetes Metrics

Monitor after deployment:
```bash
# CPU and memory usage
kubectl top pods

# Pod events
kubectl describe pods

# Deployment status
kubectl get deployment -o wide
```

## References

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Declarative Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Kubernetes kubectl commands](https://kubernetes.io/docs/reference/kubectl/)
- [Docker build reference](https://docs.docker.com/engine/reference/commandline/build/)
