#!/bin/bash
# Docker build and publish script for Elysia

set -e

# Configuration
IMAGE_NAME="elysia"
REGISTRY=""  # e.g., "docker.io/username" or "ghcr.io/username"
VERSION=$(grep version pyproject.toml | head -1 | cut -d'"' -f2)

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🐳 Elysia Docker Build Script${NC}"
echo "================================"

# Function to build image
build_image() {
    local tag=$1
    echo -e "${YELLOW}Building ${tag}...${NC}"
    docker build -t ${tag} .
    echo -e "${GREEN}✓ Built ${tag}${NC}"
}

# Function to push image
push_image() {
    local tag=$1
    echo -e "${YELLOW}Pushing ${tag}...${NC}"
    docker push ${tag}
    echo -e "${GREEN}✓ Pushed ${tag}${NC}"
}

# Parse arguments
PUSH=false
PLATFORMS=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --push)
            PUSH=true
            shift
            ;;
        --registry)
            REGISTRY="$2/"
            shift 2
            ;;
        --platforms)
            PLATFORMS="--platform $2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --push              Push images to registry"
            echo "  --registry REGISTRY Registry to push to (e.g., docker.io/username)"
            echo "  --platforms PLATFORMS Build for multiple platforms (e.g., linux/amd64,linux/arm64)"
            echo "  --help              Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Build tags
TAGS=(
    "${REGISTRY}${IMAGE_NAME}:latest"
    "${REGISTRY}${IMAGE_NAME}:${VERSION}"
    "${REGISTRY}${IMAGE_NAME}:${VERSION%.*}"  # Major.minor version
)

echo ""
echo "Version: ${VERSION}"
echo "Registry: ${REGISTRY:-local}"
echo "Tags to build:"
for tag in "${TAGS[@]}"; do
    echo "  - ${tag}"
done
echo ""

# Multi-platform build if specified
if [ -n "$PLATFORMS" ]; then
    echo -e "${YELLOW}Setting up Docker buildx for multi-platform build...${NC}"
    docker buildx create --use --name elysia-builder 2>/dev/null || true
    docker buildx inspect --bootstrap
    
    # Build command
    BUILD_CMD="docker buildx build ${PLATFORMS} --push=${PUSH}"
    
    # Add all tags
    for tag in "${TAGS[@]}"; do
        BUILD_CMD="${BUILD_CMD} -t ${tag}"
    done
    
    BUILD_CMD="${BUILD_CMD} ."
    
    echo -e "${YELLOW}Building for platforms: ${PLATFORMS#--platform }${NC}"
    eval ${BUILD_CMD}
    
    echo -e "${GREEN}✓ Multi-platform build complete${NC}"
else
    # Standard build
    for tag in "${TAGS[@]}"; do
        build_image ${tag}
    done
    
    # Tag additional versions
    docker tag ${TAGS[0]} ${TAGS[1]}
    docker tag ${TAGS[0]} ${TAGS[2]}
    
    # Push if requested
    if [ "$PUSH" = true ]; then
        if [ -z "$REGISTRY" ]; then
            echo -e "${RED}Error: --registry required when using --push${NC}"
            exit 1
        fi
        
        echo ""
        echo -e "${YELLOW}Pushing images...${NC}"
        for tag in "${TAGS[@]}"; do
            push_image ${tag}
        done
    fi
fi

echo ""
echo -e "${GREEN}✅ Docker build complete!${NC}"
echo ""
echo "To run locally:"
echo "  docker run -p 8000:8000 --env-file .env ${TAGS[0]}"
echo ""
echo "Or with docker-compose:"
echo "  docker-compose up"
