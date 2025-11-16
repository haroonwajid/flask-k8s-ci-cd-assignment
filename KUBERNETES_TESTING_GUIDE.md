# Kubernetes Configuration Testing Guide

This document provides step-by-step instructions for testing the Kubernetes manifests locally.

## Prerequisites

- Kubernetes cluster running (e.g., Docker Desktop with K8s enabled, minikube, or any K8s cluster)
- `kubectl` command-line tool installed and configured
- Docker image built and available locally (or pushed to registry)

## Testing Steps

### 1. Apply Kubernetes Manifests

Deploy the application using the manifests:

```bash
# Apply all Kubernetes manifests
kubectl apply -f kubernetes/

# Expected output:
# deployment.apps/flask-app created
# service/flask-app-service created
# service/flask-app-cluster-ip created
```

### 2. Verify Deployment Status

Check if all resources are created and running:

```bash
# Get all resources
kubectl get all

# Get pods specifically
kubectl get pods

# Expected output shows 3 replicas running:
# NAME                         READY   STATUS    RESTARTS   AGE
# pod/flask-app-xxxxx-xxxxx   1/1     Running   0          10s
# pod/flask-app-xxxxx-yyyyy   1/1     Running   0          8s
# pod/flask-app-xxxxx-zzzzz   1/1     Running   0          6s

# Get services
kubectl get services

# Expected output:
# NAME                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
# flask-app-cluster-ip    ClusterIP   10.96.xxx.xxx    <none>        8000/TCP       15s
# flask-app-service       NodePort    10.97.xxx.xxx    <none>        80:30080/TCP   15s
# kubernetes              ClusterIP   10.96.0.1        <none>        443/TCP        1d

# Get deployments
kubectl get deployments

# Expected output:
# NAME        READY   UP-TO-DATE   AVAILABLE   AGE
# flask-app   3/3     3            3           20s

# Get detailed deployment info
kubectl describe deployment flask-app

# Get pod details
kubectl describe pod <pod-name>
```

### 3. Test Rolling Update Strategy

Update the image to trigger a rolling update:

```bash
# Patch the deployment with a new image tag
kubectl set image deployment/flask-app flask-app=flask-app:v2 --record

# Watch the rolling update in progress
kubectl rollout status deployment/flask-app -w

# View rollout history
kubectl rollout history deployment/flask-app

# Expected output shows rolling update:
# Waiting for deployment "flask-app" to rollout. updated 0 of 3
# Waiting for deployment "flask-app" to rollout. updated 1 of 3
# Waiting for deployment "flask-app" to rollout. updated 2 of 3
# Waiting for deployment "flask-app" to rollout. updated 3 of 3
# deployment "flask-app" successfully rolled out
```

### 4. Test Scaling

Scale the deployment up and down:

```bash
# Scale up to 5 replicas
kubectl scale deployment flask-app --replicas=5

# Verify new replicas are running
kubectl get pods

# Expected output shows 5 running pods

# Watch pod creation
kubectl get pods -w

# Scale down to 2 replicas
kubectl scale deployment flask-app --replicas=2

# Verify scaling down
kubectl get pods

# Expected output shows 2 running pods
```

### 5. Test Rollback

Rollback to a previous version:

```bash
# View rollout history
kubectl rollout history deployment/flask-app

# Rollback to previous version
kubectl rollout undo deployment/flask-app

# Watch the rollback
kubectl rollout status deployment/flask-app -w

# Rollback to specific revision
kubectl rollout undo deployment/flask-app --to-revision=1

# Verify rollback completed
kubectl get deployment flask-app
```

### 6. Test Service Load Balancing

Access the application through the service:

```bash
# Port forward to test (for ClusterIP service)
kubectl port-forward service/flask-app-cluster-ip 8000:8000

# In another terminal, test the endpoint
curl http://localhost:8000/

# For NodePort service (if on Docker Desktop or local minikube)
# Get the NodePort
kubectl get service flask-app-service

# Access via node IP:
# - Docker Desktop: localhost:30080
# - Minikube: minikube ip:30080

curl http://localhost:30080/
```

### 7. Test Probes

Monitor probe activities:

```bash
# Check logs for probe activities
kubectl logs <pod-name>

# View probe status in pod details
kubectl describe pod <pod-name>

# Expected output shows probe results:
# Liveness:  http-get http://:5000/health delay=30s timeout=5s period=10s #success=1 #failure=3
# Readiness: http-get http://:5000/health delay=10s timeout=3s period=5s #success=1 #failure=2
```

### 8. Test Resource Limits

Verify resource requests and limits are configured:

```bash
# Check resource configuration
kubectl get pods -o json | jq '.items[].spec.containers[].resources'

# Monitor resource usage (requires metrics-server)
kubectl top nodes
kubectl top pods

# Expected output shows pod resource usage
```

### 9. Clean Up

Remove the deployed resources:

```bash
# Delete all resources
kubectl delete -f kubernetes/

# Expected output:
# deployment.apps "flask-app" deleted
# service "flask-app-service" deleted
# service "flask-app-cluster-ip" deleted

# Verify everything is deleted
kubectl get all
```

## Key Features Tested

- ✅ **Rolling Updates**: maxSurge=1, maxUnavailable=1
- ✅ **Scaling**: Multiple replicas (configurable)
- ✅ **Load Balancing**: NodePort service on port 30080
- ✅ **Resource Management**: Requests (100m CPU, 128Mi memory), Limits (500m CPU, 512Mi memory)
- ✅ **Health Checks**: Liveness and readiness probes
- ✅ **Security**: Non-root user, security context
- ✅ **Pod Distribution**: Anti-affinity for spreading across nodes

## Troubleshooting

### Pods stuck in pending state
```bash
kubectl describe pod <pod-name>
# Check for insufficient resources or scheduling issues
```

### Service not accessible
```bash
kubectl get endpoints
# Ensure endpoints are assigned to pod IPs
```

### Probes failing
```bash
kubectl logs <pod-name>
# Ensure /health endpoint is implemented in Flask app
```

### Image pull errors
```bash
# Verify image exists locally or is accessible from registry
docker images | grep flask-app
```
