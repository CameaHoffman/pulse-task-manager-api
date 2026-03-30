# FastAPI Users, Projects, and Tasks API

## Description

A production-style REST API built with FastAPI for managing users, projects, and tasks.

This project demonstrates clean backend architecture, authentication, relational data modeling, and deployment to a live cloud environment.

The API models a simple task management system with Users, Projects, and Tasks, backed by a SQLite persistence layer.

## Live Demo

Deployed on Azure App Service:

https://pulse-task-manager-api-bjceasdtcackdebf.westus3-01.azurewebsites.net

- Health Check: '/health'
- API Docs: '/docs'

## Features

- Create, retrieve, update, and list Users
- Create, retrieve, update, and list Projects
- Create, retrieve, update, and list Tasks
- List tasks by project
- Pagination using limit and offset
- Partial updates using PATCH
- JWT-based authentication (login + protected routes)
- Password hashing using bcrypt
- Input validation using Pydantic
- Repository pattern with SQLite persistence
- Fully tested with pytest

## Tech Stack

- Python 3.x
- FastAPI
- Pydantic
- SQLite
- PyJWT
- passlib (bcrypt)
- pytest
- Azure App Service (deployment)
- GitHub Actions (CI/CD)

## Project Structure

app/
    main.py
    schemas.py
    repository.py
    database.py
    auth.py

tests/
    conftest.py
    test_users.py
    test_projects.py
    test_tasks.py
    test_authentication.py
    test_health.py

## Authentication

This API uses JWT-based authentication.

- Users register with an email and password
- Passwords are securely hashed using bcrypt
- Clients obtain a token via:

POST/token
- Protected endpoints require:

Authorization: Bearer <access_token>

## System Architecture

This API follows a layered backend design to separate HTTP handling, validation, and persistence logic.

API layer (main.py) defines FastAPI routes and handles HTTP requests and responses.

Validation layer (schemas.py) defines request/response models.

Repository layer (repository.py) encapsulates database operations.

Auth layer (auth.py) handles password hashing and JWT creation/verification.

Database layer (database.py) manages SQLite connections and schema.

Tests validate API behavior, error handling, and edge cases.

### Request Flow

Client
↓
FastAPI Routes (main.py)
↓
Authentication Dependency (JWT validation)
↓
Validation via Pydantic Schemas
↓
Repository Operations
↓
SQLite Database

## API Endpoints

Authenticated endpoints require a Bearer token.

### Users

POST /users – create a user  
GET /users/{user_id} – retrieve a user by ID  
GET /users – list users
PATCH /users/{user_id} - update user 
DELETE /users/{user_id} - delete a user

### Authentication

POST /token - obtain access token

### Projects (Authenticated)

POST /projects – create a project
PATCH /projects/{project_id} - update a project  
DELETE /projects/{project_id} - delete a project

### Tasks

POST /tasks – create a task  
PATCH /tasks/{task_id} – update a task  
DELETE /tasks/{task_id} – delete a task

### Public Reads

GET /projects – list projects
GET /projects/{project_id} – retrieve a project by ID
GET /tasks – list tasks  
GET /tasks/{task_id} – retrieve a task by ID
GET /projects/{project_id}/tasks – list tasks for a project  

## Example API Usage

Create a User

Request

### POST /users

{
  "email": "user@example.com",
  "name": "Test User",
  "password": "securepassword"
}

### Login

POST/token

username=user@example.om
password=securepassword

### Use Token

Authorization: Bearer <access_token>

## Running the App

pip install -r requirements.txt
uvicorn app.main:app --reload

Then open your browser:

http://127.0.0.1:8000  
http://127.0.0.1:8000/docs

## Running Tests

pytest

## Deployment

This application is deployed to Azure App Service using GitHub Actions CI/CD.

Deployment highlights:
- Automated deploys on push to `main`
- Environment variables managed via Azure App Settings
- Production server using Gunicorn + Uvicorn workers

## Future Improvements

- Associate resources with users (multi-tenant ownership)
- Role-based access control (RBAC)
- Refresh tokens/token rotation
- Docker containerization
- Deployment

## Design Decisions

- Repository pattern isolates persistence logic from the API layer
- JWT enables stateless authentication
- bcrypt ensures secure password storage
- SQLite keeps setup lightweight for local development
- Pagination via limit/offset supports scalability
- PATCH allows partial updates without full replacement

## Author

Camea Hoffman  
https://github.com/CameaHoffman