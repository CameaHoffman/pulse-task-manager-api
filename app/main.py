from fastapi import FastAPI,HTTPException, status
from app.schemas import UserCreate, UserRead, ProjectCreate, ProjectRead, ProjectUpdate
from app.repository import InMemoryUserRepository, InMemoryProjectRepository

app = FastAPI()

user_repo = InMemoryUserRepository()
project_repo = InMemoryProjectRepository()

@app.get("/health")
def health_check():
    return {"status": "ok"}

# ---------- USERS ----------

@app.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    user = user_repo.create(email=payload.email, name=payload.name)
    return UserRead(id=user.id, email=user.email, name=user.name)

@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    user = user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead(id=user.id, email=user.email, name=user.name)

@app.get("/users", response_model=list[UserRead])
def get_users_list(limit: int = 50, offset: int=0):
    users = user_repo.list(limit=limit, offset=offset)
    return [UserRead(id=u.id, email=u.email, name=u.name) for u in users]

# ---------- PROJECTS ----------

@app.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate):
    project = project_repo.create(name=payload.name, description=payload.description)
    return ProjectRead(id=project.id, name=project.name, description=project.description)

@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: int):
    project = project_repo.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectRead(id=project.id, name=project.name, description=project.description)

@app.get("/projects", response_model=list[ProjectRead])
def get_projects_list(limit: int=50, offset: int=0):
    projects = project_repo.list(limit=limit, offset=offset)
    return [ProjectRead(id=p.id, name=p.name, description=p.description) for p in projects]

# ------ PROJECTS ROUTER ------

@app.patch("/projects/{project_id}", response_model=ProjectRead)
def update_project(project_id: int, update: ProjectUpdate):
    project = project_repo.update(project_id=project_id,
                                  name=update.name,
                                  description=update.description)
    
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if update.name is None and update.description is None:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    return ProjectRead(id=project.id, name=project.name, description=project.description)

