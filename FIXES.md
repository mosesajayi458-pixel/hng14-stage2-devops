File: api/main.py  
Line: 8  
Problem: Redis connection was hardcoded to localhost, which breaks in containerized environments  
Fix: Replaced with environment variables REDIS_HOST and REDIS_PORT  
File: api/main.py  
Problem: No health check endpoint for container monitoring  
Fix: Added /health endpoint returning service status  
File: worker/worker.py  
Line: 6  
Problem: Redis connection hardcoded to localhost, fails in containerized setup  
Fix: Replaced with environment variables REDIS_HOST and REDIS_PORT  
File: worker/worker.py  
Problem: Worker runs infinite loop without graceful shutdown handling  
Fix: Added signal handlers for SIGTERM and SIGINT to allow clean shutdown  
File: frontend/app.js  
Line: 6  
Problem: API URL hardcoded to localhost, breaks in container environment  
Fix: Replaced with environment variable API_URL  
File: frontend/app.js  
Line: 29 
Problem: Port hardcoded to 3000  
Fix: Replaced with environment variable PORT
File: frontend/app.js  
Problem: No health endpoint for container monitoring  
Fix: Added /health route 
File: api/requirements.txt  
Problem: Dependencies were not version-pinned, leading to non-reproducible builds  
Fix: Added explicit version numbers for all dependencies  
File: frontend/package.json  
Problem: Dependency versions used caret (^) allowing uncontrolled upgrades  
Fix: Pinned exact versions for express and axios  
File: api/Dockerfile  
Problem: No containerization provided  
Fix: Created production-ready Dockerfile with multi-stage build, non-root user, and healthcheck
File: frontend/app.js  
Problem: Frontend could not resolve "api" hostname outside Docker network  
Fix: Used environment variable API_URL and set it to localhost for local development
File: worker/worker.py  
Problem: Redis hostname "redis" not resolvable in local environment  
Fix: Configured REDIS_HOST to use localhost during local testing
File: worker/worker.py  
Problem: Attempted to set environment variable using shell syntax inside Python file  
Fix: Removed invalid syntax and configured REDIS_HOST using environment variables in the runtime environment  
File: api/main.py & worker/worker.py  
Problem: Environment variables required manual export for local testing  
Fix: Added python-dotenv and load_dotenv() to automatically load variables from .env file  
File: frontend/app.js  
Problem: Environment variables were not automatically loaded  
Fix: Added dotenv package and require('dotenv').config() at top of file
File: api/main.py  
Problem: .env file not being loaded automatically, requiring manual export of REDIS_HOST  
Fix: Explicitly loaded .env using load_dotenv with correct path  
File: worker/Dockerfile  
Problem: No containerization provided for worker service  
Fix: Created production-ready Dockerfile with multi-stage build, non-root user, and healthcheck  
File: frontend/Dockerfile  
Problem: No containerization for frontend service  
Fix: Created production-ready Dockerfile with multi-stage build, non-root user, and healthcheck  
File: frontend/  
Problem: No linting configuration for JavaScript  
Fix: Added ESLint configuration to enable lint stage in CI/CD pipeline  
File: frontend/eslint.config.mjs  
Problem: ESLint configuration used plugin syntax that may fail in CI environments  
Fix: Simplified config to use js.configs.recommended with Node globals  
File: frontend/eslint.config.mjs / package.json  
Problem: ESLint config used ES module syntax but Node treated it as CommonJS, causing parsing error  
Fix: Enabled ES modules by adding "type": "module" to package.json  
File: frontend/eslint.config.js  
Problem: ESLint attempted to lint its own config file, causing parsing errors with ES module syntax  
Fix: Added ignore rule to exclude eslint.config.js from linting  
File: frontend/eslint.config.js  
Problem: ESLint v9 does not support .eslintignore and attempted to lint its own config file  
Fix: Added ignores field in eslint.config.js and removed .eslintignore  
File: frontend/eslint.config.js  
Problem: ESLint v9 configuration issues caused parsing errors and ignored rules  
Fix: Configured ESLint using flat config format, added ignore rules, and ensured Node.js compatibility  