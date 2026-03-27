# Customer Support OpenEnv

## Description
AI agent environment for resolving customer support tickets.

## Tasks
- Easy: classification
- Medium: classification + response
- Hard: full resolution

## Run
uvicorn api.main:app --reload

## Docker
docker build -t env .
docker run -p 7860:7860 env