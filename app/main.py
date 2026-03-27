from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from app.schemas import (
    UserCreate, UserRead, UserUpdate, 
    ProjectCreate, ProjectRead, ProjectUpdate, 
    TaskCreate, TaskRead, TaskUpdate, Token
)
from app.repository import (SQLiteUserRepository, 
                            SQLiteProjectRepository, 
                            SQLiteTaskRepository
)
from app.database import init_db
from app.auth import (
    hash_password, 
    verify_password, 
    create_access_token,
)

from app.config import (SECRET_KEY,
                        ALGORITHM,
)

app = FastAPI()
init_db()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_repo = SQLiteUserRepository()
project_repo = SQLiteProjectRepository()
task_repo = SQLiteTaskRepository()

def to_user_read(user):
    return UserRead(id=user.id, email=user.email, name=user.name)

def to_project_read(project):
    return ProjectRead(
        id=project.id,
        name=project.name,
        description=project.description,
        )

def to_task_read(task):
    return TaskRead(
        id=task.id,
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        is_done=task.is_done,
    )

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = user_repo.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    
    return user

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {
        "service": "Pulse Task Manager API",
        "status": "running"
        }

# ---------- USERS ----------

@app.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    hashed_password = hash_password(payload.password)

    user = user_repo.create(
        email=payload.email,
        hashed_password=hashed_password,
        name=payload.name
        )
    
    return to_user_read(user)

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    user = user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return to_user_read(user)

@app.get("/users", response_model=list[UserRead])
def get_users_list(limit: int = 50, offset: int = 0):
    users = user_repo.list(limit=limit, offset=offset)
    return [to_user_read(u) for u in users]

@app.patch("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, update: UserUpdate):

    if update.name is None and update.email is None:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    
    user = user_repo.update(user_id=user_id,
                            email=update.email,
                            name=update.name,
                            )
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return to_user_read(user)

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    deleted = user_repo.delete(user_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
            )
    
# ---------- TOKEN -----------

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_repo.get_user_by_email(form_data.username)

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# ---------- PROJECTS ----------

@app.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, current_user=Depends(get_current_user)):
    project = project_repo.create(name=payload.name, description=payload.description)
    return to_project_read(project)

@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int):
    project = project_repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return to_project_read(project)

@app.get("/projects", response_model=list[ProjectRead])
def get_projects_list(limit: int=50, offset: int=0):
    projects = project_repo.list(limit=limit, offset=offset)
    return [to_project_read(p) for p in projects]

@app.patch("/projects/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, update: ProjectUpdate, current_user=Depends(get_current_user)):

    if update.name is None and update.description is None:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    
    project = project_repo.update(project_id=project_id,
                                  name=update.name,
                                  description=update.description)
    
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return to_project_read(project)

@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, current_user=Depends(get_current_user)):
    deleted = project_repo.delete(project_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
            )

# ------ TASKS ------

@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, current_user=Depends(get_current_user)):
    task = task_repo.create(
        title=payload.title,
        project_id=payload.project_id,
        description=payload.description,
        is_done=payload.is_done
        )
    
    return to_task_read(task)

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int):
    task = task_repo.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return to_task_read(task)
    
@app.get("/projects/{project_id}/tasks", response_model=list[TaskRead])
def get_tasks_list(project_id: int, limit: int = 50, offset: int = 0):
    tasks = task_repo.list_by_project(
        project_id=project_id,
        limit=limit,
        offset=offset
        )
    
    return [to_task_read(t) for t in tasks]

@app.get("/tasks", response_model=list[TaskRead])
def get_all_tasks(limit: int=50, offset: int = 0):
    tasks = task_repo.list(limit=limit, offset=offset)
    return [to_task_read(t) for t in tasks]

@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, update: TaskUpdate, current_user=Depends(get_current_user)):

    if (
        update.title is None
        and update.description is None
        and update.is_done is None
        ):
        raise HTTPException(status_code=400,
                            detail="No fields provided to update")
    
    task = task_repo.update(
        task_id=task_id,
        title=update.title,
        description=update.description,
        is_done=update.is_done,
        )
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return to_task_read(task)

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, current_user=Depends(get_current_user)):
    deleted = task_repo.delete(task_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found")

