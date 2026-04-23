# ---- Stage 1: Build dependencies ----
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---- Stage 2: Final image ----
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install curl (optional but useful for debugging/healthcheck)
# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m appuser
USER appuser

# Healthcheck (basic process check)
HEALTHCHECK CMD pgrep -f worker.py || exit 1

# Run worker
CMD ["python", "worker.py"]