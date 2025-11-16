# Pull Request Creation Guide

## Create PR from feature/kubernetes-config to develop

### Step 1: Navigate to GitHub Repository

Go to: https://github.com/haroonwajid/flask-k8s-ci-cd-assignment

### Step 2: Create New Pull Request

**Option A: Using GitHub UI**
1. Click on the **"Pull requests"** tab
2. Click **"New pull request"** button
3. Set base branch: **`develop`**
4. Set compare branch: **`feature/kubernetes-config`**
5. Click **"Create pull request"**

**Option B: Using GitHub Notification**
1. After pushing, GitHub shows a notification banner
2. Click **"Compare & pull request"** button
3. Verify branches are correct (develop ← feature/kubernetes-config)
4. Click **"Create pull request"**

### Step 3: Fill in PR Details

**Title:**
```
feat: Enhance Kubernetes manifests with rolling updates, scaling, and load balancing
```

**Description:**
```markdown
## Changes

This PR enhances the Kubernetes configuration for production-ready deployment.

### Features Added

- **Rolling Update Strategy**
  - `maxSurge: 1` - One additional pod during updates
  - `maxUnavailable: 1` - One pod can be unavailable during updates

- **Scaling Configuration**
  - 3 replicas for load distribution
  - Pod anti-affinity rules for better distribution

- **Resource Management**
  - Resource requests: 100m CPU, 128Mi memory
  - Resource limits: 500m CPU, 512Mi memory

- **Health Checks**
  - Liveness probe on `/health` endpoint
  - Readiness probe for traffic readiness

- **Load Balancing**
  - NodePort service on port 30080
  - ClusterIP service for internal communication

- **Security**
  - Non-root user execution (UID 1000)
  - Security context configuration

### Files Changed

- `kubernetes/deployment.yaml` - Enhanced deployment manifest
- `kubernetes/service.yaml` - Dual service configuration
- `KUBERNETES_TESTING_GUIDE.md` - Comprehensive testing guide

### Testing

All features have been documented in `KUBERNETES_TESTING_GUIDE.md`:
- Deployment verification
- Rolling update testing
- Scaling up/down
- Rollback procedures
- Load balancing tests

### Related Issues

Closes #[issue-number] (if applicable)
Relates to #[issue-number] (if applicable)

---

**Note**: This PR should be tested locally with `kubectl` before merging.
See `KUBERNETES_TESTING_GUIDE.md` for testing instructions.
```

### Step 4: Review and Submit

1. Review the **"Files changed"** tab to verify all changes
2. Check the CI/CD checks pass (if enabled)
3. Click **"Create pull request"**

## PR Checklist

Before submitting, verify:

- [x] Branch is `feature/kubernetes-config`
- [x] Base branch is `develop`
- [x] Commits are properly formatted
- [x] Files are pushed to remote
- [x] PR title is clear and descriptive
- [x] PR description includes all changes
- [x] No merge conflicts with develop

## After PR Creation

### Getting Reviews
- Assign reviewers from the team
- Add labels (e.g., "kubernetes", "enhancement")
- Add to a project/milestone if applicable

### Address Feedback
- If changes are requested, update the branch locally
- Commit the changes
- Push to the same branch (comments will update automatically)

### Merging

Once approved:
1. Click **"Squash and merge"** or **"Merge pull request"**
2. Confirm the merge
3. Delete the feature branch if prompted

## Command Line Alternative

If you prefer using git CLI:

```bash
# Create PR using GitHub CLI (if installed)
gh pr create --base develop --head feature/kubernetes-config --title "feat: Enhance Kubernetes manifests..." --body "$(cat FEATURE_KUBERNETES_CONFIG_SUMMARY.md)"
```

## Links

- GitHub Repository: https://github.com/haroonwajid/flask-k8s-ci-cd-assignment
- Pull Requests: https://github.com/haroonwajid/flask-k8s-ci-cd-assignment/pulls
- Branch: https://github.com/haroonwajid/flask-k8s-ci-cd-assignment/tree/feature/kubernetes-config
