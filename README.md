# FastAPI Users and Projects API

## Description

This project is a RESTful API built with FastAPI. It demonstrates test-driven development, request validation, and clean API design.

## Features

- Create, retrieve, and list Users
- Create, retrieve, and list Projects
- Input validation using Pydantic
- In-memory repositories (will be replaced with a database)
- Fully tested with pytest

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
    test_users.py
    test_projects.py

The main application file defines the FastAPI app and routes.  
Schemas define Pydantic request and response models.  
The repository layer provides in-memory data storage.  
Tests validate create, retrieve-by-id, and list behavior for both Users and Projects.

## API Endpoints

### Users
- POST /users – create a user
- GET /users/{user_id} – retrieve a user by ID
- GET /users – list users

### Projects
- POST /projects – create a project
- GET /projects/{project_id} – retrieve a project by ID
- GET /projects – list projects

## Running the App

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the FastAPI development server:
```bash
fastapi dev main.py
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

- Add update and delete endpoints
- Replace in-memory repositories with a database
- Add authentication
- Pagination improvements

## Author

Camea Hoffman  
https://github.com/CameaHoffman
