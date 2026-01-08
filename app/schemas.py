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

# ------ PROJECT SCHEMAS ------

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class ProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str] = None
