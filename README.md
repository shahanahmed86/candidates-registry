# @shahanahmed86/candidate-registry

## Prerequisites

- ### Resources
  - [Docker Desktop](https://docs.docker.com/desktop/ 'https://docs.docker.com/desktop/')
  - [FastAPI](https://fastapi.tiangolo.com/ 'https://fastapi.tiangolo.com/')
  - [Make](https://linuxhint.com/install-make-ubuntu/ 'https://linuxhint.com/install-make-ubuntu/')
  - ### Knowledge
  - Python
  - Restful
  - Docker architecture
  - Container orchestration with docker compose **_(at-least)_**
  - fastapi and the poetry as the package manager
  - swagger for api documentation

## Implemented Feature

- api documents are exposed on /docs
- User authentication APIs
- Candidates CRUD operations
- Pre-commit hook to check linting and formatting
- Used JWT for authentication

## Installation steps

```sh
cp .env.example .env # Please read the comments carefully
cp .env.example .env.dev # for development

# to create containers for mongodb, mongo-express, nginx along-with server
# and this will also expose the server to `http://localhost`
make run-container-up
make run-container-down # to remove containers
make run-container-down-hard # to remove containers and clean their data also
```
