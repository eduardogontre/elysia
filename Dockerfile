# Build stage for Python dependencies
FROM python:3.12-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./
COPY README.md ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir build && \
    python -m build --wheel && \
    pip wheel --no-cache-dir --wheel-dir /app/wheels .

# Runtime stage
FROM python:3.12-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    # Required for some Python packages
    libgomp1 \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 elysia

# Set working directory
WORKDIR /app

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels

# Install Elysia and dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir /wheels/*.whl && \
    # Download spaCy model
    python -m spacy download en_core_web_sm && \
    rm -rf /wheels

# Copy application code
COPY --chown=elysia:elysia . .

# Create necessary directories
RUN mkdir -p /app/elysia/api/user_configs && \
    chown -R elysia:elysia /app

# Switch to non-root user
USER elysia

# Expose the application port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Default command
CMD ["python", "-m", "uvicorn", "elysia.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
