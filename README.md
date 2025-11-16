# Flask Kubernetes CI/CD Assignment

A complete end-to-end CI/CD solution demonstrating Flask application deployment to Kubernetes with Docker containerization, automated testing, and Jenkins pipeline orchestration.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Local Development](#local-development)
- [Docker Build and Run](#docker-build-and-run)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Jenkins Pipeline](#jenkins-pipeline)
- [Key Features Explained](#key-features-explained)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)

## Project Overview

This project demonstrates a production-ready Flask microservice with complete CI/CD automation. It showcases:

- **Containerization**: Multi-stage Docker builds for optimized images
- **Orchestration**: Kubernetes manifests with advanced features
- **CI/CD Pipeline**: GitHub Actions for automated testing and Jenkins for deployment
- **Infrastructure as Code**: Declarative K8s manifests and pipeline definitions
- **Best Practices**: Health checks, resource management, security contexts, and rollout strategies

**Technology Stack:**
- **Application**: Python Flask 3.0.0
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Kubernetes (K8s)
- **CI/CD**: GitHub Actions & Jenkins
- **Testing**: pytest & flake8

## Architecture

```
┌─────────────────┐
│   Developer     │
│   Push to Git   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐         ┌──────────────────┐
│ GitHub Actions  │         │ Jenkins Pipeline │
│  (CI Testing)   │         │  (Build & Deploy)│
└────────┬────────┘         └────────┬─────────┘
         │                           │
         ├───────────┬───────────────┘
         │           │
         ▼           ▼
    ┌────────────────────────┐
    │   Docker Registry      │
    │   (flask-app:latest)   │
    └────────┬───────────────┘
             │
             ▼
    ┌────────────────────────┐
    │  Kubernetes Cluster    │
    │  ┌──────────────────┐  │
    │  │   Deployment     │  │
    │  │  (3 Replicas)    │  │
    │  └────────┬─────────┘  │
    │           │            │
    │  ┌────────▼─────────┐  │
    │  │  Rolling Update  │  │
    │  │  Health Checks   │  │
    │  └──────────────────┘  │
    │                        │
    │  ┌──────────────────┐  │
    │  │  NodePort Service│  │
    │  │  (Port 30080)    │  │
    │  └──────────────────┘  │
    └────────────────────────┘
             │
             ▼
       ┌──────────────┐
       │  Users (HTTP)│
       └──────────────┘
```

## Features

### ✨ Core Features

✅ **Flask REST API** with Hello World and health check endpoints  
✅ **Multi-stage Docker Builds** for minimal image size  
✅ **Kubernetes Deployment** with rolling update strategy  
✅ **Automated Testing** with pytest and flake8 linting  
✅ **GitHub Actions CI** for continuous integration  
✅ **Jenkins Pipeline** for automated deployment  
✅ **Health Checks** with liveness and readiness probes  
✅ **Resource Management** with CPU and memory limits  
✅ **Load Balancing** with NodePort and ClusterIP services  
✅ **Scaling Support** with configurable replicas  

### 🚀 Advanced Kubernetes Features

✅ **Rolling Updates** - Zero-downtime deployments (maxSurge=1, maxUnavailable=1)  
✅ **Pod Anti-affinity** - Spreads pods across different nodes  
✅ **Resource Requests** - 100m CPU, 128Mi memory guaranteed per pod  
✅ **Resource Limits** - 500m CPU, 512Mi memory maximum per pod  
✅ **Security Context** - Non-root user execution (UID 1000)  
✅ **Volume Mounts** - Persistent application logs  
✅ **Probe Configuration** - Health monitoring with customizable thresholds  

## Prerequisites

### Local Development
- Python 3.11+
- Docker 20.10+
- Docker Compose (optional)

### Kubernetes Deployment
- Kubernetes cluster (1.24+)
- kubectl configured with cluster access
- Docker images accessible (local or registry)

### Jenkins Pipeline
- Jenkins 2.361+
- Pipeline plugin
- Docker plugin
- Kubernetes CLI plugin
- kubectl installed on Jenkins agent

## Quick Start

### Clone Repository
```bash
git clone https://github.com/haroonwajid/flask-k8s-ci-cd-assignment.git
cd flask-k8s-ci-cd-assignment
```

### Run Application Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

# Test endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
```

### Deploy to Kubernetes
```bash
# Apply manifests
kubectl apply -f kubernetes/

# Verify deployment
kubectl get pods,services,deployments

# Access application
curl http://localhost:30080/
```

### Run Jenkins Pipeline
```bash
# Configure Jenkins job to use Jenkinsfile
# Trigger build in Jenkins UI
# Monitor three stages: Build → Deploy → Verify
```

## Local Development

### Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Application
```bash
# Run in development mode
python app.py

# App runs on http://localhost:5000
```

### Available Endpoints
- `GET /` - Returns Hello World message
- `GET /health` - Health check endpoint (returns status: healthy)

### Run Tests
```bash
# Run all tests with verbose output
pytest test_utils.py -v

# Run specific test
pytest test_utils.py::TestMathOperations::test_add_numbers_positive -v

# Run with coverage
pytest test_utils.py --cov=. --cov-report=html
```

### Code Linting
```bash
# Check code style (max line length 90 characters)
flake8 . --max-line-length=90

# Check specific file
flake8 app.py --max-line-length=90
```

## Docker Build and Run

### Build Docker Image
```bash
# Build image with tag
docker build -t flask-app:latest .

# Build with multiple tags
docker build -t flask-app:latest -t flask-app:v1.0 .

# Build with build arguments
docker build -t flask-app:latest \
    --build-arg PYTHON_VERSION=3.11 \
    .
```

### Run Docker Container
```bash
# Run container in foreground
docker run -p 5000:5000 flask-app:latest

# Run container in background
docker run -d -p 5000:5000 --name flask-app flask-app:latest

# Run with environment variables
docker run -p 5000:5000 \
    -e FLASK_ENV=production \
    flask-app:latest

# Run with volume mount for logs
docker run -p 5000:5000 \
    -v $(pwd)/logs:/app/logs \
    flask-app:latest
```

### Test Docker Container
```bash
# Verify container is running
docker ps

# View container logs
docker logs flask-app

# Access health endpoint
docker exec flask-app curl http://localhost:5000/health

# Stop container
docker stop flask-app

# Remove container
docker rm flask-app
```

### Multi-stage Build Details

The Dockerfile uses a two-stage build:

**Stage 1: Builder**
```dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
```

**Stage 2: Runtime**
```dockerfile
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
```

**Benefits:**
- Final image size: ~150MB (vs 300MB+ without optimization)
- Reduced attack surface
- Faster deployment
- Better caching

## Kubernetes Deployment

### Prerequisites
```bash
# Verify kubectl is installed
kubectl version --client

# Verify cluster access
kubectl get nodes

# Verify kubeconfig
kubectl config current-context
```

### Deploy to Kubernetes

**Apply Manifests:**
```bash
# Apply all manifests
kubectl apply -f kubernetes/

# Apply specific manifest
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

**Verify Deployment:**
```bash
# Check deployment status
kubectl get deployments

# Expected output:
# NAME        READY   UP-TO-DATE   AVAILABLE   AGE
# flask-app   3/3     3            3           2m

# Check pods
kubectl get pods -o wide

# Check services
kubectl get services

# Check endpoints
kubectl get endpoints
```

### Kubernetes Manifest Details

#### Deployment Features

**Replicas and Scaling:**
```yaml
spec:
  replicas: 3  # Initial replicas
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # 1 extra pod during update
      maxUnavailable: 1  # 1 pod can be unavailable
```

**Resource Management:**
```yaml
resources:
  requests:
    cpu: 100m      # Guaranteed 0.1 cores
    memory: 128Mi   # Guaranteed 128MB
  limits:
    cpu: 500m      # Maximum 0.5 cores
    memory: 512Mi  # Maximum 512MB
```

**Health Checks:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health
    port: 5000
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 2
```

**Security:**
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  allowPrivilegeEscalation: false
```

#### Service Features

**NodePort Service (External Access):**
```yaml
spec:
  type: NodePort
  ports:
    - port: 80          # Service port
      targetPort: 5000  # Pod port
      nodePort: 30080   # External port
```

**ClusterIP Service (Internal):**
```yaml
spec:
  type: ClusterIP
  ports:
    - port: 8000
      targetPort: 5000
```

### Common Kubernetes Operations

**Scaling:**
```bash
# Scale up to 5 replicas
kubectl scale deployment flask-app --replicas=5

# Scale down to 2 replicas
kubectl scale deployment flask-app --replicas=2

# View scaling status
kubectl get deployment flask-app -w
```

**Rolling Updates:**
```bash
# Update image
kubectl set image deployment/flask-app \
    flask-app=flask-app:v2 --record

# Watch rollout
kubectl rollout status deployment/flask-app -w

# View rollout history
kubectl rollout history deployment/flask-app
```

**Rollback:**
```bash
# Rollback to previous version
kubectl rollout undo deployment/flask-app

# Rollback to specific revision
kubectl rollout undo deployment/flask-app --to-revision=1

# Verify rollback
kubectl rollout status deployment/flask-app
```

**Pod Management:**
```bash
# Get pod logs
kubectl logs -l app=flask-app

# Follow logs in real-time
kubectl logs -f -l app=flask-app

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/bash

# Describe pod (detailed info)
kubectl describe pod <pod-name>
```

**Port Forwarding:**
```bash
# Forward local port to service
kubectl port-forward service/flask-app-cluster-ip 8000:8000

# Access via http://localhost:8000
```

## Jenkins Pipeline

### Pipeline Overview

The Jenkins pipeline automates the complete deployment workflow with three stages:

**Stage 1: Build Docker Image**
- Builds Docker image with metadata labels
- Tags with build number and "latest"
- Displays built images
- Ready for registry push

**Stage 2: Deploy to Kubernetes**
- Verifies kubectl availability
- Applies deployment manifest
- Applies service manifest(s)
- Lists deployed resources

**Stage 3: Verify Deployment**
- Waits for rollout completion
- Verifies pods are running and ready
- Checks service endpoints
- Reports replica status
- Verifies probe status

### Jenkins Setup

**Install Plugins:**
1. Go to Manage Jenkins → Manage Plugins
2. Search and install:
   - Pipeline
   - Docker
   - Kubernetes CLI
   - AnsiColor (optional)

**Create Pipeline Job:**
1. Click New Item
2. Enter job name
3. Select Pipeline
4. Configure Pipeline → Pipeline script from SCM
5. Set Git repository URL
6. Set Script path to `Jenkinsfile`
7. Save and build

### Run Pipeline

**Manual Trigger:**
```bash
# Click "Build Now" in Jenkins UI
# Monitor stages in real-time
# View console output for details
```

**Automated Trigger:**
```bash
# Configure GitHub webhook in Jenkins
# Pipeline runs automatically on push/PR
```

### Pipeline Logs

View detailed pipeline output:
```bash
# Each stage shows:
# - Stage start/end time
# - Build steps executed
# - Success/failure status
# - Performance metrics

# Navigate to Build → Console Output in Jenkins UI
```

## Key Features Explained

### 1. Rolling Update Strategy

**What it does:**
- Gradually replaces old pods with new ones during deployment
- Ensures zero or minimal downtime
- Allows automatic rollback if issues occur

**Configuration:**
```yaml
maxSurge: 1        # Creates 1 extra pod temporarily
maxUnavailable: 1  # Allows 1 pod to be down during update
```

**Example Scenario:**
```
Initial: [Pod1][Pod2][Pod3]
Step 1:  [Pod1][Pod2][Pod3][New1]  # Create new pod
Step 2:  [Pod2][Pod3][New1][New2]  # Remove old, create new
Step 3:  [Pod3][New1][New2][New3]  # Remove old, create new
Final:   [New1][New2][New3]        # All updated
```

**Benefits:**
- ✅ Zero-downtime deployments
- ✅ Automatic rollback capability
- ✅ Gradual traffic shift
- ✅ Health check verification

### 2. Scaling

**Horizontal Pod Autoscaling:**
```bash
# Scale up
kubectl scale deployment flask-app --replicas=5

# Scale down
kubectl scale deployment flask-app --replicas=2

# Current replicas
kubectl get deployment flask-app
# Output shows DESIRED, READY, AVAILABLE
```

**Auto-scaling (with metrics-server):**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: flask-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: flask-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

**Use Cases:**
- Handle traffic spikes automatically
- Reduce costs during low usage periods
- Ensure performance during peak loads

### 3. Load Balancing

**NodePort Service (External):**
```yaml
type: NodePort
ports:
  - port: 80           # Service cluster IP port
    targetPort: 5000   # Pod port
    nodePort: 30080    # External access port
```

**Access Pattern:**
```
External Client → Node IP:30080 → Service 80 → Pod 5000
```

**ClusterIP Service (Internal):**
```yaml
type: ClusterIP
ports:
  - port: 8000
    targetPort: 5000
```

**Access Pattern:**
```
Internal Pod → Service DNS → LoadBalancer → Pod 5000
```

**Load Balancing Features:**
- ✅ Round-robin pod selection
- ✅ Session affinity support
- ✅ Endpoint management
- ✅ Service discovery via DNS

### 4. Health Checks

**Liveness Probe:**
- Checks if pod is alive
- Restarts pod if probe fails
- Prevents zombie pods

**Readiness Probe:**
- Checks if pod is ready for traffic
- Removes from load balancer if not ready
- Ensures only healthy pods receive requests

**Configuration:**
```yaml
livenessProbe:
  initialDelaySeconds: 30    # Wait 30s before first check
  periodSeconds: 10          # Check every 10s
  failureThreshold: 3        # Restart after 3 failures

readinessProbe:
  initialDelaySeconds: 10    # Wait 10s before first check
  periodSeconds: 5           # Check every 5s
  failureThreshold: 2        # Remove from LB after 2 failures
```

### 5. Resource Management

**Requests (Guaranteed):**
```yaml
requests:
  cpu: 100m      # Scheduler allocates 100 millicores
  memory: 128Mi   # Scheduler allocates 128 megabytes
```

**Limits (Maximum):**
```yaml
limits:
  cpu: 500m      # Hard limit - pod throttled if exceeded
  memory: 512Mi   # Hard limit - pod killed if exceeded
```

**Benefit:**
- Prevents one pod from consuming all cluster resources
- Enables efficient cluster utilization
- Ensures fair resource distribution

### 6. Security Context

**Applied Configuration:**
```yaml
securityContext:
  runAsNonRoot: true            # Must run as non-root
  runAsUser: 1000               # Run as UID 1000
  allowPrivilegeEscalation: false # Prevent privilege escalation
  readOnlyRootFilesystem: false   # Allow writing to filesystem
```

**Benefits:**
- ✅ Reduced privilege levels
- ✅ Prevents container breakout
- ✅ Complies with security policies
- ✅ Limits blast radius if compromised

## Project Structure

```
flask-k8s-ci-cd-assignment/
├── app.py                           # Flask application
├── utils.py                         # Utility functions
├── test_utils.py                    # Unit tests
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Multi-stage Docker build
├── Jenkinsfile                      # Jenkins pipeline
├── README.md                        # This file
│
├── .github/workflows/
│   └── ci.yml                       # GitHub Actions workflow
│
├── kubernetes/
│   ├── deployment.yaml              # Kubernetes Deployment
│   └── service.yaml                 # Kubernetes Services
│
└── Documentation/
    ├── KUBERNETES_TESTING_GUIDE.md  # K8s testing procedures
    ├── JENKINS_PIPELINE_GUIDE.md    # Jenkins setup guide
    ├── PR_CREATION_GUIDE.md         # Pull request template
    └── QUICK_REFERENCE.md           # Quick command reference
```

## Documentation

Comprehensive guides available in the repository:

| Document | Purpose |
|----------|---------|
| **KUBERNETES_TESTING_GUIDE.md** | Step-by-step K8s testing procedures |
| **JENKINS_PIPELINE_GUIDE.md** | Jenkins setup, configuration, troubleshooting |
| **PR_CREATION_GUIDE.md** | How to create pull requests |
| **QUICK_REFERENCE.md** | Common commands and quick reference |

## Troubleshooting

### Docker Issues

**Issue: Build fails**
```bash
# Verify Docker is running
docker ps

# Check Dockerfile syntax
docker build --dry-run .

# Clean up and rebuild
docker system prune -a
docker build -t flask-app:latest .
```

**Issue: Container won't start**
```bash
# View container logs
docker logs flask-app

# Check resource availability
docker stats

# Run with debugging
docker run -it flask-app:latest /bin/bash
```

### Kubernetes Issues

**Issue: Pods stuck in pending**
```bash
# Describe pod for details
kubectl describe pod <pod-name>

# Check resource availability
kubectl top nodes
kubectl describe nodes

# Check for pod scheduling issues
kubectl get events
```

**Issue: Service not accessible**
```bash
# Verify service exists
kubectl get svc

# Check endpoints
kubectl get endpoints

# Verify pod IPs match endpoints
kubectl get pods -o wide
```

**Issue: Probes failing**
```bash
# Check pod logs
kubectl logs <pod-name>

# Verify endpoint exists
curl http://localhost:5000/health

# Check probe configuration
kubectl get pod <pod-name> -o yaml | grep -A 10 Probe
```

### Jenkins Issues

**Issue: Pipeline fails at build stage**
```bash
# Verify Docker daemon
docker ps

# Check Docker permissions
groups jenkins  # Should include docker group

# Test docker build
docker build -t test-image .
```

**Issue: kubectl not found in pipeline**
```bash
# Install kubectl on Jenkins agent
sudo apt-get install -y kubectl

# Verify kubectl path
which kubectl

# Add to Jenkins PATH if needed
```

## Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes and test
4. Commit: `git commit -m "feat: Description"`
5. Push: `git push origin feature/your-feature`
6. Create Pull Request to `develop`

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review documentation files
3. Create GitHub issue
4. Contact project maintainer

---

**Last Updated:** November 2025  
**Version:** 1.0.0  
**Maintainer:** Haroon Wajid