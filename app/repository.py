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
    
class SQLiteUserRepository:

    def create(self, email: str, name: Optional[str] = None) -> UserRecord:
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (email, name) VALUES (?, ?)",
                (email, name)
            )
            conn.commit()

            user_id = cursor.lastrowid
        finally:
            conn.close()

        return self.get(user_id)

    def get(self, user_id: int) -> Optional[UserRecord]:
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, email, name FROM users WHERE id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
        finally:
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
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, email, name FROM users ORDER BY id LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = cursor.fetchall()
        finally:

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

class SQLiteProjectRepository:

    def create(self, name: str, description: Optional[str] = None) -> ProjectRecord:
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO projects (name, description) VALUES (?, ?)",
                (name, description)
            )
            conn.commit()

            project_id = cursor.lastrowid
        finally:
            conn.close()

        return self.get(project_id)
    
    def get(self, project_id: int) -> Optional[ProjectRecord]:
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, name, description FROM projects WHERE id = ?",
                (project_id,)
            )
            row = cursor.fetchone()
        finally:
            conn.close()

        if row is None:
            return None
        
        return ProjectRecord(
            id=row["id"],
            name=row["name"],
            description=row["description"]
            )
        
    def list(self, limit: int = 50, offset: int = 0) -> List[ProjectRecord]:
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, name, description FROM projects ORDER BY id LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = cursor.fetchall()
        finally:
            conn.close()

        return [
            ProjectRecord(id=row["id"],
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
        
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE projects SET name = ?, description = ? WHERE id = ?",
                (updated_name, updated_description, project_id,)
            )
            conn.commit()
        finally:
            conn.close()

        return self.get(project_id)
    
    def delete(self, project_id: int):
        conn = get_connection()
        try:

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM projects WHERE id = ?",
                (project_id,)
            )
        
            deleted = cursor.rowcount
            conn.commit()
        finally:
            conn.close()

        return deleted > 0
    
    def reset(self) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects")
            conn.commit()

        finally:
            conn.close()

class SQLiteTaskRepository:

    def create(self, title: str, project_id: int, description: Optional[str] = None,
               is_done: bool = False) -> TaskRecord:
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO tasks (title, project_id, description, is_done) VALUES (?, ?, ?, ?)",
                (title, project_id, description, int(is_done))
                )

            conn.commit()

            task_id = cursor.lastrowid
        finally:
            conn.close()

        return self.get(task_id)
    
    def get(self, task_id: int) -> Optional[TaskRecord]:
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, project_id, title, description, is_done FROM tasks WHERE id = ?",
                (task_id,)
            )
            row = cursor.fetchone()
        finally:
            conn.close()

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
        conn = get_connection()
        try:
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
        finally:
            conn.close()

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
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, project_id, title, description, is_done FROM tasks ORDER BY id LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = cursor.fetchall()
        finally:
            conn.close()

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
        
        conn = get_connection()
        try:
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE tasks SET title = ?, description = ?, is_done = ? WHERE id = ?",
                (updated_title, updated_description, int(updated_is_done), task_id,)
            )
            conn.commit()
        finally:
            conn.close()

        return self.get(task_id)
    
    def delete(self, task_id: int):
        conn = get_connection()
        try:

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,)
            )
        
            deleted = cursor.rowcount
            conn.commit()
        finally:
            conn.close()

        return deleted > 0
        
    def reset(self) -> None:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks")
            conn.commit()

        finally:
            conn.close()
        

