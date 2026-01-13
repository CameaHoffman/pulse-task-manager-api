from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

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
        user = UserRecord(id=self._next_id, email=email, name=name)

        self._users_by_id[user.id] = user
        self._next_id += 1
        return user
    
    def get(self, user_id: int) -> Optional[UserRecord]:
        return self._users_by_id.get(user_id)
    
    def list(self, limit: int = 50, offset: int = 0) -> List[UserRecord]:
        users = sorted(self._users_by_id.values(), key=lambda u: u.id)
        return users[offset : offset + limit]
    
    def update(self, user_id: int, name: Optional[str], email: Optional[str]) -> Optional[UserRecord]:
        user = self._users_by_id.get(user_id)
        
        if user is None:
            return None
        
        if email is not None:
            user.email = email

        if name is not None:
            user.name = name

        return user
    
    def delete(self, user_id: int):
        user = self._users_by_id.get(user_id)
        
        if user is None:
            return False
        
        else:
            self._users_by_id.pop(user_id)
            return True
    
    def reset(self) -> None:
        """ Convenience for tests."""
        self._users_by_id.clear()
        self._next_id = 1

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
        

