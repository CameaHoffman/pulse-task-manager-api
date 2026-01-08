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

    def reset(self) -> None:
        self._projects_by_id.clear()
        self._next_id = 1