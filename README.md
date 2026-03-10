# FastAPI Users, Projects, and Tasks API

## Description

This project is a RESTful API built with FastAPI. It demonstrates test-driven development, request validation, clean REST API design, and partial updates using PATCH.

The API models a simple task management system with Users, Projects, and Tasks, backed by a SQLite persistence layer.

## Features

- Create, retrieve, update, and list Users
- Create, retrieve, update, and list Projects
- Create, retrieve, update, and list Tasks
- List tasks by project
- Pagination using limit and offset
- Partial updates using PATCH
- Input validation using Pydantic
- Repository pattern with SQLite persistence
- Fully tested with pytest (98% coverage)

## Tech Stack

- Python 3.x
- FastAPI
- Pydantic
- SQLite
- pytest

## Project Structure

app/
    main.py
    schemas.py
    repository.py
    database.py

tests/
    conftest.py
    test_users.py
    test_projects.py
    test_tasks.py
    test_health.py

main.py defines the FastAPI application and API routes.

schemas.py defines Pydantic request and response models.

repository.py implements repository classes for Users, Projects, and Tasks.

database.py manages the SQLite connection and database initialization.

tests/ contains pytest test suites covering API behavior and edge cases.

Shared pytest fixtures reset the database between tests to ensure deterministic results.

## System Architecture

This API follows a layered backend design to separate HTTP handling, validation, and persistence logic.

API layer (main.py) defines FastAPI routes and handles HTTP requests and responses.

Validation layer (schemas.py) defines Pydantic models for request validation and serialization.

Repository layer (repository.py) encapsulates database operations.

Database layer (database.py) manages SQLite connections and schema initialization.

Tests validate API behavior, error handling, and edge cases.

### Request Flow

Client
↓
FastAPI Routes (main.py)
↓
Validation via Pydantic Schemas (schemas.py)
↓
Repository Operations (repository.py)
↓
SQLite Database

## API Endpoints

### Users

POST /users – create a user  
GET /users/{user_id} – retrieve a user by ID  
GET /users – list users

### Projects

POST /projects – create a project  
GET /projects/{project_id} – retrieve a project by ID  
GET /projects – list projects

### Tasks

POST /tasks – create a task  
GET /tasks/{task_id} – retrieve a task by ID  
GET /tasks – list tasks  
GET /projects/{project_id}/tasks – list tasks for a project  
PATCH /tasks/{task_id} – partially update a task  
DELETE /tasks/{task_id} – delete a task

## Example API Usage

Create a User

Request

POST /users

{
  "email": "user@example.com",
  "name": "Test User"
}

Response

{
  "id": 1,
  "email": "user@example.com",
  "name": "Test User"
}

## Running the App

Install dependencies:

pip install -r requirements.txt

Start the FastAPI development server:

uvicorn app.main:app --reload

Then open your browser:

http://127.0.0.1:8000  
http://127.0.0.1:8000/docs

## Running Tests

From the project directory:

pytest

All tests should pass.

## Future Improvements

- Add authentication and authorization
- Add filtering and sorting options
- Add Docker containerization
- Deploy the API

## Design Decisions

- The repository pattern isolates persistence logic from the API layer.
- SQLite provides lightweight persistence while keeping the project easy to run locally.
- Pagination via limit and offset keeps list endpoints scalable.
- PATCH is used for partial updates to avoid requiring full resource replacement.
- Tasks reference projects using a foreign key relationship.

## Author

Camea Hoffman  
https://github.com/CameaHoffman