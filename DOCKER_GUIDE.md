# 🐳 Elysia Docker Guide

This guide explains how to build, run, and publish Elysia using Docker.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+ (optional)
- Docker Hub or GitHub Container Registry account (for publishing)

## 🚀 Quick Start

### 1. Build the Docker Image

```bash
# Simple build
docker build -t elysia:latest .

# Or use the build script
./docker-build.sh
```

### 2. Run with Docker

```bash
# Run with environment variables from .env file
docker run -p 8000:8000 --env-file .env elysia:latest

# Or run with individual environment variables
docker run -p 8000:8000 \
  -e WCD_URL="https://your-cluster.weaviate.network" \
  -e WCD_API_KEY="your-weaviate-key" \
  -e OPENAI_API_KEY="your-openai-key" \
  elysia:latest
```

### 3. Run with Docker Compose

```bash
# Start Elysia
docker-compose up -d

# View logs
docker-compose logs -f

# Stop Elysia
docker-compose down
```

## 📦 Building for Production

### Multi-Architecture Build

Build for multiple platforms (AMD64 and ARM64):

```bash
./docker-build.sh --platforms linux/amd64,linux/arm64
```

### Build and Push to Registry

```bash
# Docker Hub
./docker-build.sh --registry docker.io/yourusername --push

# GitHub Container Registry
./docker-build.sh --registry ghcr.io/yourusername --push

# Custom registry
./docker-build.sh --registry registry.example.com/elysia --push
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your configuration:

```env
# Weaviate Configuration (Required)
WCD_URL=https://your-cluster.weaviate.network
WCD_API_KEY=your-weaviate-api-key

# LLM Configuration (Choose one)
OPENAI_API_KEY=sk-your-openai-key
# OR
OPENROUTER_API_KEY=sk-or-your-openrouter-key
# OR
ANTHROPIC_API_KEY=your-anthropic-key

# Optional: Model Configuration
BASE_MODEL=gpt-4o-mini
BASE_PROVIDER=openai
COMPLEX_MODEL=gpt-4o
COMPLEX_PROVIDER=openai

# Optional: Logging
LOGGING_LEVEL=INFO
```

### Docker Compose Configuration

The `docker-compose.yml` file includes:
- Automatic container restart
- Volume persistence for user configs
- Resource limits (2 CPU, 4GB RAM max)
- Health checks
- Custom network isolation

## 🏗️ Dockerfile Details

The Dockerfile uses a multi-stage build:

1. **Builder Stage**: Compiles Python dependencies
2. **Runtime Stage**: Minimal image with only runtime dependencies

Features:
- Python 3.12 slim base image
- Non-root user (`elysia`) for security
- Pre-installed spaCy language model
- Health check endpoint
- Optimized layer caching

## 🚢 Publishing to Docker Hub

### 1. Create Docker Hub Repository

1. Go to [hub.docker.com](https://hub.docker.com)
2. Create a new repository named `elysia`
3. Make it public or private as needed

### 2. Login to Docker Hub

```bash
docker login
```

### 3. Build and Push

```bash
# Tag with your Docker Hub username
docker build -t yourusername/elysia:latest .

# Push to Docker Hub
docker push yourusername/elysia:latest

# Or use the script
./docker-build.sh --registry docker.io/yourusername --push
```

### 4. Pull and Run from Docker Hub

Others can now use your image:

```bash
docker run -p 8000:8000 --env-file .env yourusername/elysia:latest
```

## 🔒 Security Best Practices

1. **Never include secrets in the image**
   - Use environment variables or mounted secrets
   - Don't commit `.env` files

2. **Run as non-root user**
   - The container runs as user `elysia` (UID 1000)

3. **Use specific versions**
   - Pin Python version: `python:3.12-slim`
   - Pin dependency versions in `pyproject.toml`

4. **Scan for vulnerabilities**
   ```bash
   docker scout cves elysia:latest
   ```

## 🐛 Troubleshooting

### Container won't start

Check logs:
```bash
docker logs elysia-app
```

### Connection issues

Ensure the container can reach external services:
```bash
docker exec elysia-app ping -c 3 google.com
```

### Permission errors

The container runs as UID 1000. Ensure mounted volumes have correct permissions:
```bash
sudo chown -R 1000:1000 ./elysia/api/user_configs
```

### Health check failing

Test the health endpoint:
```bash
docker exec elysia-app curl http://localhost:8000/health
```

## 📊 Resource Requirements

Minimum:
- 1 CPU core
- 2GB RAM
- 1GB disk space

Recommended:
- 2+ CPU cores
- 4GB+ RAM
- 5GB+ disk space

## 🔄 Updating

To update to a new version:

```bash
# Pull latest code
git pull

# Rebuild image
docker-compose build

# Restart with new image
docker-compose up -d
```

## 🎯 Example Deployment

### Production docker-compose.yml

```yaml
version: '3.8'

services:
  elysia:
    image: yourusername/elysia:latest
    container_name: elysia-prod
    ports:
      - "80:8000"  # Map to port 80
    env_file:
      - .env.prod
    volumes:
      - ./data:/app/elysia/api/user_configs
    restart: always
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 📝 Notes

- The frontend is included in the image (static files)
- User configurations are persisted in a volume
- The image includes all necessary Python dependencies
- SpaCy language model is pre-downloaded

## 🆘 Support

For issues with Docker deployment:
1. Check the [Elysia documentation](https://weaviate.github.io/elysia/)
2. Open an issue on [GitHub](https://github.com/weaviate/elysia/issues)
3. Check container logs and health status
