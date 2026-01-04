from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None

