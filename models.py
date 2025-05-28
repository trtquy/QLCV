from dataclasses import dataclass, asdict
from typing import Optional, List
from datetime import datetime
import uuid

@dataclass
class User:
    id: str
    username: str
    email: str
    role: str  # 'member' or 'manager'
    created_at: str
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class Task:
    id: str
    title: str
    description: str
    status: str  # 'todo', 'in_progress', 'completed'
    assignee_id: Optional[str]
    priority: str  # 'low', 'medium', 'high', 'urgent'
    created_at: str
    updated_at: str
    created_by: str
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class Team:
    id: str
    name: str
    description: str
    created_at: str
    members: List[str]  # List of user IDs
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.members:
            self.members = []
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
