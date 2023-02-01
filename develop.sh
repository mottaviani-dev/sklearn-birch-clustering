#!/bin/bash

if [ "$1" == "up" ]; then
    docker-compose -f deploy/docker-compose.yml up -d --build
elif [ "$1" == "down" ]; then
    docker-compose -f deploy/docker-compose.yml down
elif [ "$1" == "update" ]; then
    docker-compose -f deploy/docker-compose.yml build --no-cache --progress=plain
else
    echo "Invalid command: $1"
fi