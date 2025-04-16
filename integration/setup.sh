#!/bin/bash

# OpenDeepSearch Integration Setup Script

# Print colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================"
echo -e "OpenDeepSearch PRD Generator Setup"
echo -e "========================================${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Create environment files
echo -e "${YELLOW}Creating environment files...${NC}"
cp .env.example.microservice .env
cp .env.example.proxy .env.proxy

echo -e "${YELLOW}Please edit the .env file with your API keys before proceeding.${NC}"
echo -e "Press Enter when you're ready to continue..."
read

# Build and start services
echo -e "${YELLOW}Building and starting services...${NC}"
docker-compose build
docker-compose up -d

# Check if services are running
echo -e "${YELLOW}Checking if services are running...${NC}"
sleep 5
if docker-compose ps | grep -q "Up"; then
    echo -e "${GREEN}Services are running!${NC}"
else
    echo -e "${RED}There might be an issue with the services. Please check 'docker-compose logs'.${NC}"
    exit 1
fi

# Test the API
echo -e "${YELLOW}Testing the API...${NC}"
curl -s -X GET http://localhost:8000/api/health
echo
curl -s -X GET http://localhost:3000/api/health
echo

echo -e "${GREEN}========================================"
echo -e "Setup completed successfully!"
echo -e "OpenDeepSearch PRD Generator is running at: http://localhost:8000"
echo -e "Proxy Backend is running at: http://localhost:3000"
echo -e "========================================${NC}"

echo -e "${YELLOW}Next steps:${NC}"
echo -e "1. Test the PRD generator with:"
echo -e "   curl -X POST -H \"Content-Type: application/json\" -d '{\"query\":\"A social media app for pet owners\"}' http://localhost:3000/api/deep-research"
echo -e "2. Update your web application to use the new API endpoint."
echo -e "3. See INTEGRATION.md for more details." 