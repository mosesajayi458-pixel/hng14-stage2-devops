# FIXES.md

This document contains all bugs, misconfigurations, and CI/CD issues found in the project, including how they were fixed.

---

## 1. API Service Fixes

### 1.1 Redis Host Configuration
File: `api/main.py`  
Issue: Redis connection was hardcoded to `localhost`, which fails in Docker environments.  
Fix: Replaced Redis host/port with environment variables `REDIS_HOST` and `REDIS_PORT`.

---

### 1.2 Environment Variable Loading
File: `api/main.py`  
Issue: `.env` variables required manual export for local testing.  
Fix: Added `python-dotenv` and implemented `load_dotenv()` to automatically load environment variables from `.env`.

---

### 1.3 Health Check Endpoint
File: `api/main.py`  
Issue: No health check route existed for container monitoring.  
Fix: Added `/health` endpoint returning API service status.

---

### 1.4 Flake8 Linting Fixes
File: `api/main.py`  
Issue: Imports were not placed at the top of the file (flake8 E402).  
Fix: Moved all imports to the top of the file.

File: `api/main.py`  
Issue: Blank line contained whitespace (flake8 W293).  
Fix: Removed trailing whitespace.

File: `api/main.py`  
Issue: Missing newline at end of file (flake8 W292).  
Fix: Added newline at the end of the file.

---

## 2. Worker Service Fixes

### 2.1 Redis Host Configuration
File: `worker/worker.py`  
Issue: Redis hostname was hardcoded, which fails in container environments.  
Fix: Replaced Redis configuration with environment variables `REDIS_HOST` and `REDIS_PORT`.

---

### 2.2 Graceful Shutdown Handling
File: `worker/worker.py`  
Issue: Worker ran an infinite loop with no shutdown support.  
Fix: Added signal handlers for SIGTERM and SIGINT to allow clean shutdown.

---

### 2.3 Environment Variable Loading
File: `worker/worker.py`  
Issue: Environment variables required manual export for local testing.  
Fix: Added `python-dotenv` and implemented `load_dotenv()` to automatically load `.env`.

---

### 2.4 Invalid Shell Syntax in Python
File: `worker/worker.py`  
Issue: Attempted to set environment variables using shell syntax inside Python file.  
Fix: Removed invalid syntax and relied on runtime environment variables.

---

### 2.5 Flake8 Linting Fixes
File: `worker/worker.py`  
Issue: Imports were not at the top of the file (flake8 E402).  
Fix: Reordered imports properly.

File: `worker/worker.py`  
Issue: Missing spacing before function definitions (flake8 E302).  
Fix: Added correct blank lines.

File: `worker/worker.py`  
Issue: Missing spacing after function definition (flake8 E305).  
Fix: Added correct blank lines after functions.

File: `worker/worker.py`  
Issue: Missing newline at end of file (flake8 W292).  
Fix: Added newline at end of file.

---

## 3. Frontend Fixes

### 3.1 API URL Configuration
File: `frontend/app.js`  
Issue: API URL was hardcoded to `localhost`, which breaks Docker container networking.  
Fix: Replaced API URL with environment variable `API_URL`.

---

### 3.2 Port Configuration
File: `frontend/app.js`  
Issue: Frontend port was hardcoded to 3000.  
Fix: Replaced port value with environment variable `PORT`.

---

### 3.3 Health Check Endpoint
File: `frontend/app.js`  
Issue: No health endpoint existed for monitoring.  
Fix: Added `/health` endpoint returning frontend service status.

---

### 3.4 Automatic Environment Variable Loading
File: `frontend/app.js`  
Issue: Environment variables were not automatically loaded.  
Fix: Added `dotenv` package and implemented `require("dotenv").config()`.

---

### 3.5 Localhost Hostname Fix
File: `frontend/app.js`  
Issue: Frontend could not resolve the `api` hostname outside Docker network.  
Fix: Used `API_URL` environment variable and configured it to use localhost during local development.

---

## 4. Dependency Fixes

### 4.1 API Requirements Version Pinning
File: `api/requirements.txt`  
Issue: Dependencies were not pinned, causing non-reproducible builds.  
Fix: Added explicit version numbers for all dependencies.

---

### 4.2 Frontend Dependency Pinning
File: `frontend/package.json`  
Issue: Dependencies used caret (`^`) which allowed uncontrolled upgrades.  
Fix: Pinned exact versions for express and axios.

---

### 4.3 httpx Compatibility Fix
File: `api/requirements.txt`  
Issue: Tests failed due to incompatible httpx version with Starlette/FastAPI TestClient.  
Fix: Added pinned version `httpx==0.27.0`.

---

## 5. ESLint Configuration Fixes

### 5.1 Missing Linting Setup
File: `frontend/`  
Issue: No linting configuration existed for CI lint stage.  
Fix: Added ESLint configuration file.

---

### 5.2 CI Parsing Errors (ES Modules)
File: `frontend/eslint.config.mjs`  
File: `frontend/package.json`  
Issue: ESLint config used ES module syntax but Node treated project as CommonJS.  
Fix: Added `"type": "module"` in `package.json`.

---

### 5.3 ESLint Self-Linting Issue
File: `frontend/eslint.config.js`  
Issue: ESLint attempted to lint its own config file, causing parsing errors.  
Fix: Added ignore rules to exclude the ESLint config file.

---

### 5.4 ESLint v9 Ignore Handling
File: `frontend/eslint.config.js`  
Issue: ESLint v9 does not support `.eslintignore`.  
Fix: Used `ignores` field in flat config and removed `.eslintignore`.

---

## 6. Dockerfile Fixes and Improvements

### 6.1 API Dockerfile Creation
File: `api/Dockerfile`  
Issue: No containerization existed for API service.  
Fix: Created production-ready multi-stage Dockerfile with non-root user and healthcheck.

---

### 6.2 Worker Dockerfile Creation
File: `worker/Dockerfile`  
Issue: No containerization existed for worker service.  
Fix: Created production-ready multi-stage Dockerfile with non-root user and healthcheck.

---

### 6.3 Frontend Dockerfile Creation
File: `frontend/Dockerfile`  
Issue: No containerization existed for frontend service.  
Fix: Created production-ready multi-stage Dockerfile with non-root user and healthcheck.

---

### 6.4 Hadolint Compliance Fixes
File: `api/Dockerfile`  
File: `worker/Dockerfile`  
Issue: Hadolint warned about missing `--no-install-recommends` (DL3015).  
Fix: Added `--no-install-recommends` and cleaned apt cache.

File: `api/Dockerfile`  
File: `worker/Dockerfile`  
Issue: Hadolint warned about unpinned apt versions (DL3008).  
Fix: Added `# hadolint ignore=DL3008` to allow unpinned installs.

---

### 6.5 Trivy Security Fixes (Debian)
File: `api/Dockerfile`  
File: `worker/Dockerfile`  
Issue: Trivy detected CRITICAL CVEs from outdated Debian packages.  
Fix: Added `apt-get upgrade -y` to ensure latest security patches.

---

### 6.6 Trivy Security Fixes (Alpine)
File: `frontend/Dockerfile`  
Issue: Trivy detected CRITICAL CVEs in Alpine base packages.  
Fix: Added `apk upgrade --no-cache` to update system packages.

---

## 7. CI/CD Pipeline Fixes

### 7.1 Dockerfile Lint Fix (Hadolint)
File: `.github/workflows/pipeline.yml`  
Issue: Hadolint action failed because multiple Dockerfiles were passed incorrectly.  
Fix: Split hadolint linting into three separate steps (API, Worker, Frontend).

---

### 7.2 Workflow YAML Syntax Fix
File: `.github/workflows/pipeline.yml`  
Issue: Pipeline failed due to YAML indentation and job structure errors.  
Fix: Corrected indentation and properly separated jobs.

---

### 7.3 Test Stage Import Fix
File: `.github/workflows/pipeline.yml`  
Issue: Pytest failed with `ModuleNotFoundError: No module named 'api'`.  
Fix: Added PYTHONPATH export step:
`export PYTHONPATH=$PYTHONPATH:.`

---

### 7.4 Trivy Scan Configuration Fix
File: `.github/workflows/pipeline.yml`  
Issue: Trivy scan failed without printing readable results.  
Fix: Configured Trivy scan to output table results in logs and also generate SARIF output.

---

### 7.5 Deploy Stage Logic Fix
File: `.github/workflows/pipeline.yml`  
Issue: Deploy stage needed correct dependencies and rolling update behavior.  
Fix: Implemented deploy stage logic to ensure healthcheck passes before replacing old container.

---

## 8. Trivy Ignore Fixes

### 8.1 Suppressing Unfixable Vulnerabilities
File: `.trivyignore`  
Issue: Trivy detected CRITICAL vulnerabilities with no fixed versions, failing the pipeline.  
Fix: Added ignored CVEs:
- CVE-2023-45853
- CVE-2025-7458

---

## Summary

The project was stabilized for production readiness by implementing:
- Proper environment variable support
- Health endpoints for all services
- Clean Dockerfiles (multi-stage, non-root, healthchecks)
- Full CI/CD pipeline (lint → test → build → scan → integration → deploy)
- Security scanning and vulnerability management