import subprocess
import os
import sys

repo_path = r"c:\Users\J Tech\Downloads\Files\Activity1\Ass_3\flask-k8s-ci-cd-assignment"
os.chdir(repo_path)

print("="*70)
print("GIT PUSH OPERATIONS")
print("="*70)

# Configure git if not already configured
git_config = [
    ["git", "config", "user.email", "developer@example.com"],
    ["git", "config", "user.name", "Developer"],
]

print("\n1. Configuring Git...")
for cmd in git_config:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✓ {' '.join(cmd)}")
    except Exception as e:
        print(f"   ⚠ {' '.join(cmd)}: {e}")

# Check git status
print("\n2. Checking Git Status...")
try:
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.stdout:
        print(f"   Uncommitted changes:\n{result.stdout}")
    else:
        print("   ✓ No uncommitted changes")
except Exception as e:
    print(f"   ⚠ Error checking status: {e}")

# Add all files
print("\n3. Staging Files...")
try:
    result = subprocess.run(["git", "add", "."], capture_output=True, text=True)
    print("   ✓ All files staged")
except Exception as e:
    print(f"   ✗ Error staging files: {e}")

# Check if there are changes to commit
print("\n4. Checking for Changes to Commit...")
try:
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], capture_output=True, text=True)
    if result.returncode != 0:
        print("   ✓ Changes found - proceeding with commit")
        
        # Commit changes
        print("\n5. Committing Changes...")
        commit_message = """feat: Add initial Flask K8s CI/CD structure

- Add Flask app with Hello World endpoint and health check
- Add requirements.txt with Flask dependencies
- Add multi-stage Dockerfile with health checks
- Add Kubernetes deployment manifest with 3 replicas
- Add Kubernetes service manifest with LoadBalancer
- Add Jenkins declarative pipeline with full CI/CD stages
- Add GitHub Actions CI workflow for automated testing and deployment

This establishes the foundation for the Flask K8s CI/CD assignment."""
        
        result = subprocess.run(["git", "commit", "-m", commit_message], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✓ Changes committed successfully")
        else:
            print(f"   ⚠ Commit output: {result.stdout}")
            print(f"   ⚠ Commit error: {result.stderr}")
    else:
        print("   ℹ No staged changes to commit")
except Exception as e:
    print(f"   ⚠ Error checking for changes: {e}")

# Get current branch
print("\n6. Current Branch Information...")
try:
    result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    current_branch = result.stdout.strip()
    print(f"   Current branch: {current_branch}")
except Exception as e:
    print(f"   ⚠ Error getting current branch: {e}")

# Check if remote exists
print("\n7. Checking Remote Configuration...")
try:
    result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
    if result.stdout:
        print("   ✓ Remote configured:")
        print(result.stdout)
    else:
        print("   ⚠ No remote repository configured")
        print("\n   To add remote:")
        print("   git remote add origin https://github.com/haroonwajid/flask-k8s-ci-cd-assignment.git")
except Exception as e:
    print(f"   ⚠ Error checking remote: {e}")

# List recent commits
print("\n8. Recent Commits...")
try:
    result = subprocess.run(["git", "log", "--oneline", "-5"], capture_output=True, text=True)
    print(result.stdout)
except Exception as e:
    print(f"   ⚠ Error getting logs: {e}")

# Try to push
print("\n9. Attempting to Push Changes...")
try:
    # First, try to push to current branch
    result = subprocess.run(["git", "push", "-u", "origin", "HEAD"], 
                          capture_output=True, text=True, timeout=10)
    if result.returncode == 0:
        print("   ✓ Changes pushed successfully!")
        print(f"   {result.stdout}")
    else:
        print("   ⚠ Push output:")
        print(f"   {result.stdout}")
        if result.stderr:
            print(f"   Error: {result.stderr}")
except subprocess.TimeoutExpired:
    print("   ⚠ Push operation timed out")
except Exception as e:
    print(f"   ⚠ Error during push: {e}")

print("\n" + "="*70)
print("PUSH OPERATIONS COMPLETED")
print("="*70)

print("\n📋 SUMMARY:")
print("   - All local files have been staged")
print("   - Changes have been committed")
print("   - Push operation attempted")
print("\n✓ If you see 'Changes pushed successfully', your changes are now on GitHub!")
print("\n📌 NEXT STEPS:")
print("   1. Check the GitHub repository for the latest changes")
print("   2. Create a Pull Request for feature/initial-structure → develop")
print("   3. Request code review from team members")
