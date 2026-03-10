from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from app.database import get_connection

@dataclass
class UserRecord:
    id: int
    email: str
    name: Optional[str] = None

@dataclass
class ProjectRecord:
    id: int
    name: str
    description: Optional[str] = None

@dataclass
class TaskRecord:
    id: int
    project_id: int
    title: str
    description: Optional[str] = None
    is_done: bool = False
    
class InMemoryUserRepository:
    """
    In-memory repository for Users. Replace later.
    """

    def __init__(self) -> None:
        self._users_by_id: Dict[int, UserRecord] = {}
        self._next_id: int=1

    def create(self, email: str, name: Optional[str] = None) -> UserRecord:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (email, name) VALUES (?, ?)",
            (email, name)
        )
        conn.commit()

        user_id = cursor.lastrowid
        conn.close()

        return self.get(user_id)

    def get(self, user_id: int) -> Optional[UserRecord]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, email, name FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None
        
        return UserRecord(
            id=row["id"],
            email=row["email"],
            name=row["name"]
        )
    
    def list(self, limit: int = 50, offset: int = 0) -> List[UserRecord]:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, email, name FROM users ORDER BY id LIMIT ? OFFSET ?",
            (limit, offset)
        )
        rows = cursor.fetchall()
        conn.close()

        return [
            UserRecord(id=row["id"],
                       email=row["email"],
                       name=row["name"]
                       )
                       for row in rows
        ]
    
    def update(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None) -> Optional[UserRecord]:
        existing_user = self.get(user_id)

        if existing_user is None:
            return None
        
        updated_name = name if name is not None else existing_user.name
        updated_email = email if email is not None else existing_user.email
        
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE users SET email = ?, name = ? WHERE id = ?",
                (updated_email, updated_name, user_id,)
            )
            conn.commit()
        finally:
            conn.close()

        return self.get(user_id)
    
    def delete(self, user_id: int):
        conn = get_connection()
        try:

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM users WHERE id = ?",
                (user_id,)
            )
        
            deleted = cursor.rowcount
            conn.commit()
        finally:
            conn.close()

        return deleted > 0

    def reset(self) -> None:
        """ Convenience for tests."""
        conn = get_connection()

        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users")
            conn.commit()
        finally:
            conn.close()

class InMemoryProjectRepository:
    """
    In-memory repository for Projects. Replace Later."""

    def __init__(self) -> None:
        self._projects_by_id: Dict[int, ProjectRecord] = {}
        self._next_id: int=1

    def create(self, name: str, description: Optional[str] = None) -> ProjectRecord:
        project = ProjectRecord(id=self._next_id, name=name, description=description)

        self._projects_by_id[project.id] = project
        self._next_id += 1
        return project
    
    def get(self, project_id: int) -> Optional[ProjectRecord]:
        return self._projects_by_id.get(project_id)

    def list(self, limit: int = 50, offset: int = 0) -> List[ProjectRecord]:
        projects = sorted(self._projects_by_id.values(), key=lambda p: p.id)
        return projects[offset : offset + limit]
    
    def update(self, project_id: int, name: Optional[str], description: Optional[str]) -> Optional[ProjectRecord]:
        project = self._projects_by_id.get(project_id)
        
        if project is None:
            return None
        
        if name is not None:
            project.name = name

        if description is not None:
            project.description = description

        return project
    
    def delete(self, project_id: int):
        project = self._projects_by_id.get(project_id)
        
        if project is None:
            return False
        
        else:
            self._projects_by_id.pop(project_id)
            return True

    def reset(self) -> None:
        self._projects_by_id.clear()
        self._next_id = 1

class InMemoryTaskRepository:
    """
    In-memory repository for Tasks. Replace Later.
    """

    def __init__(self) -> None:
        self._tasks_by_id: Dict[int, TaskRecord] = {}
        self._next_id: int=1

    def create(self, title: str, project_id: int, description: Optional[str] = None,
               is_done: bool = False) -> TaskRecord:
        
        task = TaskRecord(id=self._next_id, title=title,
                          description=description, is_done=is_done, project_id=project_id)

        self._tasks_by_id[task.id] = task
        self._next_id += 1

        return task
    
    def get(self, task_id: int) -> Optional[TaskRecord]:
        return self._tasks_by_id.get(task_id)
    
    def list_by_project(self, project_id: int, limit: int = 50, offset: int = 0) -> List[TaskRecord]:
        tasks = [t for t in self._tasks_by_id.values() if t.project_id == project_id]
        tasks = sorted(tasks, key=lambda t: t.id)
        return tasks[offset : offset + limit]
    
    def list(self, limit: int = 50, offset: int = 0) -> List[TaskRecord]:
        tasks = sorted(self._tasks_by_id.values(), key=lambda t: t.id)
        return tasks[offset : offset + limit]

    def update(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
               is_done: Optional[bool] = None) -> Optional[TaskRecord]:
        
        task = self._tasks_by_id.get(task_id)
        if task is None:
            return None
        
        if title is not None:
            task.title = title

        if description is not None:
            task.description = description

        if is_done is not None:
            task.is_done = is_done
            
        return task
    
    def delete(self, task_id: int):
        task = self._tasks_by_id.get(task_id)

        if task is None:
            return False
        
        else:
            self._tasks_by_id.pop(task_id)
            return True
        
    def reset(self) -> None:
        self._tasks_by_id.clear()
        self._next_id = 1
        

