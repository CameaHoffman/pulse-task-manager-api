from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class UserRecord:
    id: int
    email: str
    name: Optional[str] = None

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