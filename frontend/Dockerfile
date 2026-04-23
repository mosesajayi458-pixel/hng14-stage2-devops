# ---- Stage 1: Install dependencies ----
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first (for caching)
COPY package*.json ./

RUN npm install --only=production

# Copy app code
COPY . .


# ---- Stage 2: Final image ----
FROM node:18-alpine

WORKDIR /app

# Upgrade alpine packages to fix security vulnerabilities (openssl)
RUN apk update && apk upgrade --no-cache

# Copy app from builder
COPY --from=builder /app /app

# Create non-root user
RUN adduser -D appuser
USER appuser

# Expose port
EXPOSE 3000

# Healthcheck
HEALTHCHECK CMD wget --spider http://localhost:3000/health || exit 1

# Start app
CMD ["node", "app.js"]