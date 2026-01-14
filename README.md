# FastAPI Users, Projects, and Tasks API

## Description

This project is a RESTful API built with FastAPI. It demonstrates test-driven development, request validation, clean REST API design, and partial updates using PATCH.

## Features

- Create, retrieve, update, and list Users
- Create, retrieve, update, and list Projects
- Create, retrieve, update, and list Tasks
- List tasks by project
- Partial updates using PATCH
- Input validation using Pydantic
- In-memory repositories with a clean abstraction layer
- Fully tested with pytest (98% coverage)

## Tech Stack

- Python 3.x
- FastAPI
- Pydantic
- pytest

## Project Structure

app/
    main.py
    schemas.py
    repository.py
tests/
    conftest.py
    test_users.py
    test_projects.py
    test_tasks.py
    test_health.py

The main application file defines the FastAPI app and routes.  
Schemas define Pydantic request and response models.  
The repository layer provides in-memory data storage.  
Tests validate CRUD behavior, error handling, and partial updates for Users, Projects and Tasks.
conftest.py provides shared pytest fixtures used to reset in-memory repositories between tests.

## API Endpoints

### Users
- POST /users – create a user
- GET /users/{user_id} – retrieve a user by ID
- GET /users – list users

### Projects
- POST /projects – create a project
- GET /projects/{project_id} – retrieve a project by ID
- GET /projects – list projects

### Tasks
- POST /tasks – create a task
- GET /tasks/{task_id} – retrieve a task by ID
- GET /tasks - list tasks
- GET /projects/{project_id}/tasks – list tasks for a project
- PATCH /tasks/{task_id} - partially update a task
- DELETE /tasks/{task_id} - delete a task

## Running the App

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the FastAPI development server:
```bash
fastapi app/dev main.py
```

Then open your browser:
- http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs

## Running Tests

From the project directory:
```bash
pytest
```

All tests should pass.

## Future Improvements

- Replace in-memory repositories with a database-backed implementation
- Add authentication and authorization
- Add filtering and sorting options
- Deployment configuration

## Design Decisions

- An in-memory repository was used to keep the focus on API design, correctness, and testability.
- The repository abstraction allows storage to be replaced without changing the API layer.
- PATCH is used for partial updates to avoid requiring full resource replacement.
- Tasks are addressed by global ID, with a nested endpoint for listing tasks by project.

## Author

Camea Hoffman  
https://github.com/CameaHoffman
