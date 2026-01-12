from pydantic import BaseModel, EmailStr
from typing import Optional

# ------ USER SCHEMAS ------

class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None

# ------ PROJECT SCHEMAS ------

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# ------ TASK SCHEMAS ------

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool = False
    project_id: int

class TaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_done: bool = False
    project_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = None

