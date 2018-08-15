#!/usr/bin/env bash
set -e

docker build -t hbuoj-site:latest -f deploy/Dockerfile .
docker run hbuoj-site:latest