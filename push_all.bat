@echo off
REM Quick Git Push Script for Flask K8s CI/CD Assignment

setlocal enabledelayexpansion

echo.
echo ================================================================
echo  Flask K8s CI/CD Assignment - Git Push Script
echo ================================================================
echo.

cd /d "c:\Users\J Tech\Downloads\Files\Activity1\Ass_3\flask-k8s-ci-cd-assignment"

if not exist .git (
    echo Initializing Git repository...
    git init
)

echo.
echo Configuring Git user...
git config --local user.name "Developer"
git config --local user.email "developer@example.com"

echo.
echo Current status:
git status

echo.
echo Staging all files...
git add .

echo.
echo Checking for changes...
git diff --cached --quiet
if !errorlevel! equ 0 (
    echo No changes to commit
) else (
    echo.
    echo Committing changes...
    git commit -m "feat: Add initial Flask K8s CI/CD structure" ^
        -m "- Add Flask app with Hello World endpoint and health check" ^
        -m "- Add requirements.txt with Flask dependencies" ^
        -m "- Add multi-stage Dockerfile with health checks" ^
        -m "- Add Kubernetes deployment manifest with 3 replicas" ^
        -m "- Add Kubernetes service manifest with LoadBalancer" ^
        -m "- Add Jenkins declarative pipeline with full CI/CD stages" ^
        -m "- Add GitHub Actions CI workflow for automated testing and deployment"
)

echo.
echo Current branches:
git branch -a

echo.
echo Checking remote configuration...
git remote -v
if !errorlevel! neq 0 (
    echo.
    echo No remote configured. Adding origin...
    git remote add origin https://github.com/haroonwajid/flask-k8s-ci-cd-assignment.git
)

echo.
echo Recent commits:
git log --oneline -5

echo.
echo Pushing changes...
git push -u origin feature/initial-structure

echo.
echo ================================================================
echo  Push Complete!
echo ================================================================
echo.
echo Check GitHub to verify the changes:
echo https://github.com/haroonwajid/flask-k8s-ci-cd-assignment
echo.

pause
