import json
import os
from typing import List, Optional, Dict, Any
from models import User, Task, Team
import logging

class DataManager:
    def __init__(self, data_file='data.json'):
        self.data_file = data_file
        self.data = self.load_data()
    
    def load_data(self) -> Dict[str, Any]:
        """Load data from JSON file or create default structure"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                logging.warning(f"Could not load data from {self.data_file}, creating new data structure")
        
        # Create default data structure
        return {
            'users': [],
            'tasks': [],
            'teams': [],
            'current_user_id': None
        }
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving data: {e}")
    
    # User management
    def create_user(self, username: str, email: str, role: str = 'member') -> User:
        """Create a new user"""
        user = User('', username, email, role, '')
        self.data['users'].append(user.to_dict())
        self.save_data()
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        for user_data in self.data['users']:
            if user_data['id'] == user_id:
                return User.from_dict(user_data)
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        for user_data in self.data['users']:
            if user_data['username'] == username:
                return User.from_dict(user_data)
        return None
    
    def get_all_users(self) -> List[User]:
        """Get all users"""
        return [User.from_dict(user_data) for user_data in self.data['users']]
    
    def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        """Update user data"""
        for i, user_data in enumerate(self.data['users']):
            if user_data['id'] == user_id:
                user_data.update(kwargs)
                self.data['users'][i] = user_data
                self.save_data()
                return User.from_dict(user_data)
        return None
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user"""
        for i, user_data in enumerate(self.data['users']):
            if user_data['id'] == user_id:
                del self.data['users'][i]
                self.save_data()
                return True
        return False
    
    # Task management
    def create_task(self, title: str, description: str, created_by: str, 
                   assignee_id: Optional[str] = None, priority: str = 'medium') -> Task:
        """Create a new task"""
        task = Task('', title, description, 'todo', assignee_id, priority, '', '', created_by)
        self.data['tasks'].append(task.to_dict())
        self.save_data()
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        for task_data in self.data['tasks']:
            if task_data['id'] == task_id:
                return Task.from_dict(task_data)
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return [Task.from_dict(task_data) for task_data in self.data['tasks']]
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """Get tasks by status"""
        return [Task.from_dict(task_data) for task_data in self.data['tasks'] 
                if task_data['status'] == status]
    
    def get_tasks_by_assignee(self, assignee_id: str) -> List[Task]:
        """Get tasks by assignee"""
        return [Task.from_dict(task_data) for task_data in self.data['tasks'] 
                if task_data['assignee_id'] == assignee_id]
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """Update task data"""
        from datetime import datetime
        for i, task_data in enumerate(self.data['tasks']):
            if task_data['id'] == task_id:
                task_data.update(kwargs)
                task_data['updated_at'] = datetime.now().isoformat()
                self.data['tasks'][i] = task_data
                self.save_data()
                return Task.from_dict(task_data)
        return None
    
    def delete_task(self, task_id: str) -> bool:
        """Delete task"""
        for i, task_data in enumerate(self.data['tasks']):
            if task_data['id'] == task_id:
                del self.data['tasks'][i]
                self.save_data()
                return True
        return False
    
    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description"""
        query = query.lower()
        results = []
        for task_data in self.data['tasks']:
            if (query in task_data['title'].lower() or 
                query in task_data['description'].lower()):
                results.append(Task.from_dict(task_data))
        return results
    
    # Session management
    def set_current_user(self, user_id: str):
        """Set current user in session"""
        self.data['current_user_id'] = user_id
        self.save_data()
    
    def get_current_user(self) -> Optional[User]:
        """Get current user"""
        if self.data['current_user_id']:
            return self.get_user(self.data['current_user_id'])
        return None
    
    def logout_current_user(self):
        """Logout current user"""
        self.data['current_user_id'] = None
        self.save_data()

# Global instance
data_manager = DataManager()
