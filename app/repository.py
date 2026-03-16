from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from app.database import get_connection

@dataclass
class UserRecord:
    id: int
    email: str
    hashed_password: str
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
    
class SQLiteUserRepository:

    def create(self, email: str, hashed_password: str, name: Optional[str] = None) -> UserRecord:
        with get_connection() as conn:
            cursor = conn.cursor()
        
            cursor.execute(
                "INSERT INTO users (email, name, hashed_password) VALUES (?, ?, ?)",
                (email, name, hashed_password)
            )

            user_id = cursor.lastrowid
        
        return self.get(user_id)

    def get(self, user_id: int) -> Optional[UserRecord]:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, email, name, hashed_password FROM users WHERE id = ?",
                (user_id,)
            )
            row = cursor.fetchone()

        if row is None:
            return None
        
        return UserRecord(
            id=row["id"],
            email=row["email"],
            name=row["name"],
            hashed_password=row["hashed_password"]
        )
    
    def get_user_by_email(self, email: str) -> Optional[UserRecord]:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, email, name, hashed_password FROM users WHERE email = ?",
                (email,)
            )

            row = cursor.fetchone()

        if row is None:
            return None
        
        return UserRecord(
            id=row["id"],
            email=row["email"],
            name=row["name"],
            hashed_password=row["hashed_password"]
        )
    
    def list(self, limit: int = 50, offset: int = 0) -> List[UserRecord]:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, email, name, hashed_password FROM users ORDER BY id LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = cursor.fetchall()

        return [
            UserRecord(
                id=row["id"],
                email=row["email"],
                name=row["name"],
                hashed_password=row["hashed_password"]
            )
            for row in rows
        ]
    
    def update(self, user_id: int, name: Optional[str] = None, email: Optional[str] = None) -> Optional[UserRecord]:
        existing_user = self.get(user_id)

        if existing_user is None:
            return None
        
        updated_name = name if name is not None else existing_user.name
        updated_email = email if email is not None else existing_user.email
        
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE users SET email = ?, name = ? WHERE id = ?",
                (updated_email, updated_name, user_id,)
            )
            
        return self.get(user_id)
    
    def delete(self, user_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM users WHERE id = ?",
                (user_id,)
            )
        
            deleted = cursor.rowcount

        return deleted > 0

    def reset(self) -> None:
        """ Convenience for tests."""
        with get_connection() as conn:
            cursor = conn.cursor()
        
            cursor.execute("DELETE FROM users")

class SQLiteProjectRepository:

    def create(self, name: str, description: Optional[str] = None) -> ProjectRecord:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO projects (name, description) VALUES (?, ?)",
                (name, description)
            )

            project_id = cursor.lastrowid

        return self.get(project_id)
    
    def get(self, project_id: int) -> Optional[ProjectRecord]:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, name, description FROM projects WHERE id = ?",
                (project_id,)
            )
            row = cursor.fetchone()

        if row is None:
            return None
        
        return ProjectRecord(
            id=row["id"],
            name=row["name"],
            description=row["description"]
            )
        
    def list(self, limit: int = 50, offset: int = 0) -> List[ProjectRecord]:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, name, description FROM projects ORDER BY id LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = cursor.fetchall()

        return [
            ProjectRecord(
                id=row["id"],
                name=row["name"],
                description=row["description"]
            )
            for row in rows
        ]
    
    def update(self, project_id: int, name: Optional[str], description: Optional[str]) -> Optional[ProjectRecord]:
        existing_project = self.get(project_id)

        if existing_project is None:
            return None
        
        updated_name = name if name is not None else existing_project.name
        updated_description = description if description is not None else existing_project.description
        
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE projects SET name = ?, description = ? WHERE id = ?",
                (updated_name, updated_description, project_id,)
            )

        return self.get(project_id)
    
    def delete(self, project_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM projects WHERE id = ?",
                (project_id,)
            )
        
            deleted = cursor.rowcount

        return deleted > 0
    
    def reset(self) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects")

class SQLiteTaskRepository:

    def create(self, title: str, project_id: int, description: Optional[str] = None,
               is_done: bool = False) -> TaskRecord:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO tasks (title, project_id, description, is_done) VALUES (?, ?, ?, ?)",
                (title, project_id, description, int(is_done))
                )

            task_id = cursor.lastrowid
        
        return self.get(task_id)
    
    def get(self, task_id: int) -> Optional[TaskRecord]:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, project_id, title, description, is_done FROM tasks WHERE id = ?",
                (task_id,)
            )
            row = cursor.fetchone()

        if row is None:
            return None
        
        return TaskRecord(
            id=row["id"],
            project_id=row["project_id"],
            title=row["title"],
            description=row["description"],
            is_done=bool(row["is_done"])
            )
    
    def list_by_project(self, project_id: int, limit: int = 50, offset: int = 0) -> List[TaskRecord]:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT id, project_id, title, description, is_done
                FROM tasks
                WHERE project_id = ?
                ORDER BY id
                LIMIT ? OFFSET ?
                """,
                (project_id, limit, offset)
            )

            rows = cursor.fetchall()

        return [
            TaskRecord(
                id=row["id"],
                project_id=row["project_id"],
                title=row["title"],
                description=row["description"],
                is_done=bool(row["is_done"])
            )
            for row in rows
        ]
    
    def list(self, limit: int = 50, offset: int = 0) -> List[TaskRecord]:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, project_id, title, description, is_done FROM tasks ORDER BY id LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = cursor.fetchall()

        return [
            TaskRecord(
                id=row["id"],
                project_id=row["project_id"],
                title=row["title"],
                description=row["description"],
                is_done=bool(row["is_done"])
            )
            for row in rows
        ]

    def update(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
               is_done: Optional[bool] = None) -> Optional[TaskRecord]:
        
        existing_task = self.get(task_id)

        if existing_task is None:
            return None
        
        updated_title = title if title is not None else existing_task.title
        updated_description = description if description is not None else existing_task.description
        updated_is_done = is_done if is_done is not None else existing_task.is_done
        
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE tasks SET title = ?, description = ?, is_done = ? WHERE id = ?",
                (updated_title, updated_description, int(updated_is_done), task_id,)
            )

        return self.get(task_id)
    
    def delete(self, task_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,)
            )
        
            deleted = cursor.rowcount

        return deleted > 0
        
    def reset(self) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks")

