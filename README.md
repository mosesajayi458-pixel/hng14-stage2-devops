# hng14-stage2-devops
````md
# Containerized Microservices Job Processing System (Stage 2 - DevOps)

This repository contains a microservices-based job processing application that has been containerized and shipped with a complete CI/CD pipeline.

The goal of this project is to make the system production-ready by ensuring:

- all services run in containers
- proper service healthchecks are implemented
- security scanning is enforced
- CI/CD pipeline stages run in strict order
- deployment is performed safely using rolling updates

---

## Application Overview

The system contains four services:

Service: Frontend (Node.js)  
Purpose: Allows users submit jobs and view job status.

Service: API (FastAPI)  
Purpose: Creates jobs, stores job status, and provides job status updates.

Service: Worker (Python)  
Purpose: Processes jobs pulled from the Redis queue and updates status.

Service: Redis  
Purpose: Shared queue and job status storage between API and Worker.

---

## How the System Works

Step 1: User submits a job through the Frontend.  
Step 2: Frontend forwards the request to the API.  
Step 3: API pushes the job into Redis queue.  
Step 4: Worker pulls jobs from Redis and processes them.  
Step 5: Worker updates job status in Redis.  
Step 6: API retrieves job status from Redis.  
Step 7: Frontend displays the updated job status.

---

## Prerequisites

Tool: Git  
Purpose: Clone and manage the repository.

Tool: Docker  
Purpose: Run services in containers.

Tool: Docker Compose  
Purpose: Run the multi-service stack.

Optional tools (only needed for running without Docker):  
Python 3.11+  
Node.js 18+

---

## Repository Setup

Step 1: Clone the repository

```bash
git clone https://github.com/mosesajayi458-pixel/hng14-stage2-devops.git
cd hng14-stage2-devops
````

---

## Environment Variables

File: `.env.example`
Purpose: Contains all required environment variables with placeholder values.

Step 1: Create a `.env` file

```bash
cp .env.example .env
```

Step 2: Edit the `.env` file if needed.

Important:
Do not commit `.env` into GitHub. It must never be tracked in git history.

---

## Running the Application Locally

Step 1: Build and start all services

```bash
docker compose up --build
```

Step 2: (Optional) Run in detached mode

```bash
docker compose up --build -d
```

---

## Confirming Services Are Running

Step 1: Check running containers

```bash
docker ps
```

Expected containers:

frontend
api
worker
redis

---

## Health Check Verification

The services expose health endpoints for monitoring.

API health check:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Frontend health check:

```bash
curl http://localhost:3000/health
```

Expected response:

```json
{"status":"ok"}
```

---

## Testing the Job Processing Flow

### Submit a Job

```bash
curl -X POST http://localhost:8000/jobs
```

Expected response:

```json
{
  "job_id": "some-uuid",
  "status": "queued"
}
```

---

### Check Job Status

Replace `<job_id>` with the job id returned above:

```bash
curl http://localhost:8000/jobs/<job_id>
```

Expected response (initially):

```json
{
  "job_id": "some-uuid",
  "status": "queued"
}
```

Expected response (after worker processing):

```json
{
  "job_id": "some-uuid",
  "status": "completed"
}
```

---

## Stopping the Application

Step 1: Stop all services

```bash
docker compose down
```

Step 2: (Optional) Stop and remove volumes

```bash
docker compose down -v
```

---

## CI/CD Pipeline

This repository contains a complete CI/CD pipeline implemented using GitHub Actions.

File: `.github/workflows/pipeline.yml`

The pipeline runs in strict order:

lint → test → build → security scan → integration test → deploy

---

## Pipeline Stages

### Stage 1: Lint

Tools used:

flake8 (API + Worker)
eslint (Frontend)
hadolint (Dockerfiles)

Purpose: Ensures consistent coding style and detects errors early.

---

### Stage 2: Test

Tool: pytest
Purpose: Runs unit tests for the API service.

Requirement:
Redis is mocked during tests to avoid dependency on a real Redis instance.

Output:
Coverage report is generated and uploaded as a pipeline artifact.

---

### Stage 3: Build

Purpose: Builds Docker images for all services and tags them.

Images built:

api
worker
frontend

Tags applied:

latest
git SHA

Images are pushed into a local Docker registry running inside the GitHub Actions runner.

---

### Stage 4: Security Scan

Tool: Trivy
Purpose: Scans Docker images for vulnerabilities.

Pipeline rule:
Pipeline fails if CRITICAL vulnerabilities are found unless ignored in `.trivyignore`.

Output:
Scan results are uploaded as SARIF artifacts.

---

### Stage 5: Integration Test

Purpose: Validates that the full system works when deployed as a stack.

Integration test actions:

* starts all containers
* submits a job to the API
* polls until the job is completed
* tears down containers cleanly

---

### Stage 6: Deploy

Trigger: Runs only on pushes to `main`.

Purpose: Performs a rolling update deployment.

Deployment rule:

* new container must pass healthcheck before stopping old container
* if healthcheck does not pass within 60 seconds, deployment aborts and old container remains running

---

## Important Files

File: `docker-compose.yml`
Purpose: Defines the full multi-service stack.

File: `.env.example`
Purpose: Placeholder environment variables.

File: `.trivyignore`
Purpose: Ignored vulnerabilities that have no available fix.

File: `FIXES.md`
Purpose: Documents all bugs found and the fixes applied.

File: `.github/workflows/pipeline.yml`
Purpose: CI/CD pipeline definition.

---

## Production Readiness Notes

All services run as non-root users.
Multi-stage Docker builds were used for smaller images.
Healthchecks are implemented for monitoring.
Redis is not exposed to the host machine.

---

## Author

GitHub:https://github.com/mosesajayi458-pixel
Olowookere Damilola

```
```
