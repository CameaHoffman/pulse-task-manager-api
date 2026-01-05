from fastapi import FastAPI, HTTPException, status
from app.schemas import UserCreate, UserRead
from app.repository import InMemoryUserRepository

app = FastAPI()

user_repo = InMemoryUserRepository()

@app.get("/health")
def health_check():
    return {"status": "ok"}

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
