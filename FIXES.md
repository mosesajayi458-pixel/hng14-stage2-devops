
---

````md
# FIXES.md

This document tracks all issues encountered during development and CI/CD pipeline setup, along with their fixes.

---

## 1. API Service Fixes (`api/main.py`)

### 1.1 Redis Host Configuration
- **File:** `api/main.py`
- **Issue:** Redis connection was hardcoded to `localhost`, which fails in container environments.
- **Fix:** Replaced Redis host/port with environment variables:
  - `REDIS_HOST`
  - `REDIS_PORT`

---

### 1.2 Environment Variable Loading
- **File:** `api/main.py`
- **Issue:** `.env` variables had to be manually exported for local testing.
- **Fix:** Added `python-dotenv` and implemented `load_dotenv()` to automatically load `.env`.

---

### 1.3 Health Check Endpoint
- **File:** `api/main.py`
- **Issue:** No health check route existed for monitoring containers.
- **Fix:** Added `/health` endpoint returning API service status.

---

### 1.4 Flake8 Linting Fixes
- **File:** `api/main.py`
- **Issues:**
  - Imports were not at the top of the file (`flake8 E402`)
  - Blank line contained whitespace (`flake8 W293`)
  - Missing newline at end of file (`flake8 W292`)
- **Fix:** Reordered imports properly, removed trailing whitespace, and ensured newline at EOF.

---

## 2. Worker Service Fixes (`worker/worker.py`)

### 2.1 Redis Host Configuration
- **File:** `worker/worker.py`
- **Issue:** Redis hostname was hardcoded to `localhost`, causing failure in Docker containers.
- **Fix:** Replaced Redis configuration with environment variables:
  - `REDIS_HOST`
  - `REDIS_PORT`

---

### 2.2 Graceful Shutdown Handling
- **File:** `worker/worker.py`
- **Issue:** Worker ran an infinite loop with no shutdown support.
- **Fix:** Added signal handlers for `SIGTERM` and `SIGINT` to stop worker cleanly.

---

### 2.3 Environment Variable Loading
- **File:** `worker/worker.py`
- **Issue:** Environment variables required manual export during local testing.
- **Fix:** Added `python-dotenv` and implemented `load_dotenv()` to automatically load `.env`.

---

### 2.4 Invalid Shell Syntax in Python
- **File:** `worker/worker.py`
- **Issue:** Attempted to set environment variables using shell syntax inside Python.
- **Fix:** Removed invalid code and relied on runtime environment variables instead.

---

### 2.5 Flake8 Linting Fixes
- **File:** `worker/worker.py`
- **Issues:**
  - Imports not at the top (`flake8 E402`)
  - Missing spacing before functions (`flake8 E302`)
  - Missing spacing after function definitions (`flake8 E305`)
  - Missing newline at EOF (`flake8 W292`)
- **Fix:** Reordered imports, added required blank lines, and added newline at EOF.

---

## 3. Frontend Fixes (`frontend/app.js`)

### 3.1 API URL Configuration
- **File:** `frontend/app.js`
- **Issue:** API URL was hardcoded to `localhost`, breaking container networking.
- **Fix:** Replaced API URL with environment variable `API_URL`.

---

### 3.2 Port Configuration
- **File:** `frontend/app.js`
- **Issue:** Frontend port was hardcoded to `3000`.
- **Fix:** Replaced port value with environment variable `PORT`.

---

### 3.3 Health Check Endpoint
- **File:** `frontend/app.js`
- **Issue:** No health endpoint existed for monitoring.
- **Fix:** Added `/health` endpoint returning frontend service status.

---

### 3.4 Automatic Environment Variable Loading
- **File:** `frontend/app.js`
- **Issue:** Frontend environment variables were not automatically loaded.
- **Fix:** Added `dotenv` and configured `require("dotenv").config()`.

---

### 3.5 Localhost Hostname Fix
- **File:** `frontend/app.js`
- **Issue:** Frontend could not resolve Docker hostname `api` outside container network.
- **Fix:** Configured `API_URL` to use `localhost` during local development.

---

## 4. Dependency Fixes

### 4.1 API Requirements Version Pinning
- **File:** `api/requirements.txt`
- **Issue:** Dependencies were not pinned, leading to non-reproducible builds.
- **Fix:** Pinned explicit versions for all dependencies.

---

### 4.2 httpx Compatibility Fix
- **File:** `api/requirements.txt`
- **Issue:** Tests failed due to incompatible `httpx` version with FastAPI/Starlette TestClient.
- **Fix:** Added:
  ```txt
  httpx==0.27.0
````

---

### 4.3 Frontend Dependency Pinning

* **File:** `frontend/package.json`
* **Issue:** Dependencies used caret (`^`) allowing uncontrolled upgrades.
* **Fix:** Pinned exact versions for `express` and `axios`.

---

## 5. ESLint Configuration Fixes

### 5.1 Missing Linting Setup

* **File:** `frontend/`
* **Issue:** No ESLint configuration existed for CI linting stage.
* **Fix:** Added ESLint configuration.

---

### 5.2 CI Parsing Errors (ES Modules)

* **Files:** `frontend/eslint.config.mjs`, `frontend/package.json`
* **Issue:** ESLint config used ES module syntax but Node treated project as CommonJS.
* **Fix:** Added `"type": "module"` in `package.json`.

---

### 5.3 ESLint Self-Linting Issue

* **File:** `frontend/eslint.config.js`
* **Issue:** ESLint attempted to lint its own config file, causing parsing errors.
* **Fix:** Added ignore rules to exclude ESLint config file.

---

### 5.4 ESLint v9 Ignore Handling

* **File:** `frontend/eslint.config.js`
* **Issue:** ESLint v9 does not support `.eslintignore`.
* **Fix:** Used `ignores` field in flat config and removed `.eslintignore`.

---

## 6. Dockerfile Fixes and Improvements

### 6.1 API Dockerfile (`api/Dockerfile`)

* **Issue:** Missing production Dockerfile.
* **Fix:** Created multi-stage Dockerfile with:

  * non-root user
  * healthcheck
  * smaller production image

#### Hadolint Fixes

* **Issues:**

  * Missing `--no-install-recommends` (`DL3015`)
  * Unpinned apt versions (`DL3008`)
* **Fix:**

  * Added `--no-install-recommends`
  * Cleaned apt cache
  * Added `# hadolint ignore=DL3008`

#### Trivy Security Fix

* **Issue:** Vulnerabilities detected in base Debian packages.
* **Fix:** Added `apt-get upgrade -y` to install latest security patches.

---

### 6.2 Worker Dockerfile (`worker/Dockerfile`)

* **Issue:** Missing production Dockerfile.
* **Fix:** Created multi-stage Dockerfile with:

  * non-root user
  * healthcheck

#### Hadolint Fixes

* **Issues:**

  * Missing `--no-install-recommends` (`DL3015`)
  * Unpinned apt versions (`DL3008`)
* **Fix:**

  * Added `--no-install-recommends`
  * Cleaned apt cache
  * Added `# hadolint ignore=DL3008`

#### Trivy Security Fix

* **Issue:** Vulnerabilities detected in base Debian packages.
* **Fix:** Added `apt-get upgrade -y` to install latest security patches.

---

### 6.3 Frontend Dockerfile (`frontend/Dockerfile`)

* **Issue:** Missing production Dockerfile.
* **Fix:** Created multi-stage Dockerfile with:

  * non-root user
  * healthcheck

#### Trivy Security Fix

* **Issue:** Alpine base image contained outdated vulnerable packages.
* **Fix:** Added:

  ```sh
  apk upgrade --no-cache
  ```

---

## 7. CI/CD Pipeline Fixes (`.github/workflows/pipeline.yml`)

### 7.1 Dockerfile Lint Fix (Hadolint)

* **Issue:** Hadolint action failed because multiple Dockerfiles were passed incorrectly.
* **Fix:** Split Dockerfile linting into three separate steps:

  * API Dockerfile lint
  * Worker Dockerfile lint
  * Frontend Dockerfile lint

---

### 7.2 Workflow Syntax Fix

* **Issue:** GitHub Actions rejected the workflow due to YAML indentation errors.
* **Fix:** Corrected indentation and ensured all jobs were nested properly.

---

### 7.3 Test Stage Fix (PYTHONPATH)

* **Issue:** Pytest could not import `api.main` (`ModuleNotFoundError: No module named 'api'`).
* **Fix:** Added:

  ```bash
  export PYTHONPATH=$PYTHONPATH:.
  ```

---

### 7.4 Trivy Scan Fix

* **Issue:** Trivy scan failed without clear log output.
* **Fix:** Configured Trivy to:

  * output scan results in readable table format
  * also generate SARIF output for grading

---

### 7.5 Deploy Stage Logic

* **Issue:** Deploy stage did not properly depend on previous stages.
* **Fix:** Updated deploy stage to run only after all required jobs passed using `needs:`.

---

## 8. Security Fixes (`.trivyignore`)

### .trivyignore

* **Issue:** Trivy detected CRITICAL vulnerabilities with no available fix, failing the pipeline.
* **Fix:** Added ignored CVEs:

  * `CVE-2023-45853` (zlib issue, will_not_fix)
  * `CVE-2025-7458` (sqlite issue, no fixed version available)

---

# Summary

All pipeline stages were implemented and stabilized:

* Linting (flake8, eslint, hadolint)
* Unit testing with pytest + coverage
* Docker image build and tagging
* Security scanning using Trivy
* Integration testing with live containers
* Deployment stage execution

