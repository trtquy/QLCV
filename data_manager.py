from typing import List, Optional
from models import User, Task
from app import db
from flask import session
import logging

class DataManager:
    def __init__(self):
        self.current_user_id = None
    
    # User management
    def create_user(self, username: str, email: str, role: str = 'member') -> User:
        """Create a new user"""
        user = User(username=username, email=email, role=role)
        db.session.add(user)
        db.session.commit()
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return User.query.get(int(user_id))
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return User.query.filter_by(username=username).first()
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return User.query.all()
    
    def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        """Update user data"""
        user = User.query.get(int(user_id))
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            db.session.commit()
        return user
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        user = User.query.get(int(user_id))
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
    
    # Task management
    def create_task(self, title: str, description: str, created_by: str, 
                   assignee_id: Optional[str] = None, priority: str = 'medium') -> Task:
        """Create a new task"""
        task = Task(
            title=title,
            description=description,
            created_by=int(created_by),
            assignee_id=int(assignee_id) if assignee_id else None,
            priority=priority,
            status='todo'
        )
        db.session.add(task)
        db.session.commit()
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return Task.query.get(int(task_id))
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return Task.query.all()
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Get tasks by status"""
        return Task.query.filter_by(status=status).all()
    
    def get_tasks_by_assignee(self, assignee_id: str) -> List[Task]:
        """Get tasks by assignee"""
        return Task.query.filter_by(assignee_id=int(assignee_id)).all()
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """Update task data"""
        task = Task.query.get(int(task_id))
        if task:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    if key == 'assignee_id' and value:
                        setattr(task, key, int(value))
                    else:
                        setattr(task, key, value)
            db.session.commit()
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """Delete task"""
        task = Task.query.get(int(task_id))
        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        return False
    
    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description"""
        return Task.query.filter(
            db.or_(
                Task.title.contains(query),
                Task.description.contains(query)
            )
        ).all()
    
    # Session management
    def set_current_user(self, user_id: str):
        """Set current user in session"""
        self.current_user_id = user_id
        session['user_id'] = user_id
    
    def get_current_user(self) -> Optional[User]:
        """Get current user"""
        user_id = session.get('user_id') or self.current_user_id
        if user_id:
            return User.query.get(int(user_id))
        return None
    
    def logout_current_user(self):
        """Logout current user"""
        self.current_user_id = None
        session.pop('user_id', None)

# Global instance
data_manager = DataManager()