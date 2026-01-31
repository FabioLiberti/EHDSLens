# EHDSLens Docker Image
# Multi-stage build for efficient image size

# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/

# Install package
RUN pip install --no-cache-dir build && \
    python -m build --wheel && \
    pip install --no-cache-dir dist/*.whl

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash ehdslens

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/ehdslens* /usr/local/bin/
COPY --from=builder /usr/local/bin/streamlit /usr/local/bin/
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/

# Copy source for Streamlit
COPY --from=builder /app/src/ehdslens /app/ehdslens

# Set ownership
RUN chown -R ehdslens:ehdslens /app

USER ehdslens

# Expose ports for Dashboard (8501) and API (8000)
EXPOSE 8501 8000

# Default command: run dashboard
CMD ["streamlit", "run", "/app/ehdslens/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
