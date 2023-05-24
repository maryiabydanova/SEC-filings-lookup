#!/bin/bash

# Stop and remove all running containers
docker-compose down

# Remove existing images
docker-compose rm -f

# Build new images
docker-compose build

# Start the containers
docker-compose up -d
