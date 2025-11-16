import os
import subprocess
import json
from datetime import datetime

repo_path = r"c:\Users\J Tech\Downloads\Files\Activity1\Ass_3\flask-k8s-ci-cd-assignment"

# Configure git settings for this operation
os.chdir(repo_path)

# Set up git configuration for commits
git_config_cmds = [
    ["git", "config", "user.email", "developer@example.com"],
    ["git", "config", "user.name", "Developer"],
]

for cmd in git_config_cmds:
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✓ Executed: {' '.join(cmd)}")
    except Exception as e:
        print(f"⚠ {' '.join(cmd)}: {e}")

# Check if .git exists, if not initialize
if not os.path.exists(".git"):
    print("\nInitializing git repository...")
    subprocess.run(["git", "init"], check=True, capture_output=True)
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], check=True, capture_output=True)
    print("✓ Git repository initialized")

# Create develop branch if it doesn't exist
try:
    result = subprocess.run(["git", "rev-parse", "--verify", "develop"], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        subprocess.run(["git", "checkout", "-b", "develop"], check=True, capture_output=True)
        subprocess.run(["git", "push", "-u", "origin", "develop"], capture_output=True)
        print("✓ Created and switched to develop branch")
    else:
        subprocess.run(["git", "checkout", "develop"], check=True, capture_output=True)
        print("✓ Switched to existing develop branch")
except Exception as e:
    print(f"⚠ Could not create develop branch: {e}")

# Create feature branch from develop
try:
    subprocess.run(["git", "checkout", "-b", "feature/initial-structure"], 
                  check=True, capture_output=True)
    print("✓ Created and switched to feature/initial-structure branch")
except subprocess.CalledProcessError as e:
    print(f"✗ Error creating feature branch: {e}")
    exit(1)

# Stage all files
try:
    subprocess.run(["git", "add", "."], check=True, capture_output=True)
    print("✓ Staged all files")
except Exception as e:
    print(f"✗ Error staging files: {e}")

# Commit the changes
try:
    commit_message = """Add initial Flask K8s CI/CD structure

- Add Flask app with Hello World endpoint
- Add requirements.txt with Flask dependency
- Add multi-stage Dockerfile for Flask app
- Add Kubernetes deployment manifest
- Add Kubernetes service manifest
- Add Jenkins declarative pipeline
- Add GitHub Actions CI workflow

This establishes the foundation for the Flask K8s CI/CD assignment."""
    
    subprocess.run(["git", "commit", "-m", commit_message], 
                  check=True, capture_output=True)
    print("✓ Committed all changes")
except Exception as e:
    print(f"✗ Error committing changes: {e}")

# Display branch information
print("\n" + "="*60)
print("Git Branch Information:")
print("="*60)

result = subprocess.run(["git", "branch", "-a"], capture_output=True, text=True)
print(result.stdout)

result = subprocess.run(["git", "log", "--oneline", "-5"], capture_output=True, text=True)
print("Recent commits:")
print(result.stdout)

print("="*60)
print(f"✓ Feature branch 'feature/initial-structure' created successfully!")
print(f"  Location: {repo_path}")
print("="*60)
