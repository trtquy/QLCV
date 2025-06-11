from typing import List, Optional
from models import User, Task, Team, TimeLog
from app import db
from flask import session
import logging
from datetime import datetime, timedelta

class DataManager:
    def __init__(self):
        self.current_user_id = None
    
    # User management
    def create_user(self, username: str, email: str, role: str = 'analyst', password: str = '123') -> User:
        """Create a new user"""
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return User.query.get(int(user_id))
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return User.query.filter_by(username=username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return User.query.filter_by(email=email).first()
    
    def authenticate_user(self, username_or_email: str, password: str) -> Optional[User]:
        """Authenticate user by username/email and password"""
        # Try to find user by username first
        user = self.get_user_by_username(username_or_email)
        
        # If not found, try by email
        if not user:
            user = self.get_user_by_email(username_or_email)
        
        # Check password if user exists
        if user and user.check_password(password):
            return user
        
        return None
    
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
                   assignee_id: Optional[str] = None, priority: str = 'medium', 
                   complexity: str = 'medium') -> Task:
        """Create a new task"""
        task = Task(
            title=title,
            description=description,
            created_by=int(created_by),
            assignee_id=int(assignee_id) if assignee_id else None,
            priority=priority,
            complexity=complexity,
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
    
    # Team management
    def get_all_teams(self) -> List[Team]:
        """Get all teams"""
        return Team.query.all()
    
    def get_team(self, team_id: str) -> Optional[Team]:
        """Get team by ID"""
        return Team.query.get(int(team_id))
    
    def get_tasks_by_team(self, team_id: str) -> List[Task]:
        """Get tasks by team"""
        return Task.query.filter_by(team_id=int(team_id)).all()
    
    def get_users_by_team(self, team_id: str) -> List[User]:
        """Get users by team"""
        return User.query.filter_by(team_id=int(team_id)).all()
    
    # Time tracking methods
    def start_time_tracking(self, task_id: str, user_id: str, description: str = None) -> TimeLog:
        """Start time tracking for a task"""
        # Check if there's already an active time log for this user/task
        active_log = TimeLog.query.filter_by(
            task_id=int(task_id),
            user_id=int(user_id),
            end_time=None
        ).first()
        
        if active_log:
            return active_log  # Return existing active log
        
        time_log = TimeLog(
            task_id=int(task_id),
            user_id=int(user_id),
            start_time=datetime.utcnow(),
            description=description
        )
        
        # Update task start time if not set
        task = self.get_task(task_id)
        if task and not task.started_at:
            task.started_at = datetime.utcnow()
            if task.status == 'todo':
                task.status = 'in_progress'
        
        db.session.add(time_log)
        db.session.commit()
        return time_log
    
    def stop_time_tracking(self, time_log_id: str) -> TimeLog:
        """Stop time tracking and calculate duration"""
        time_log = TimeLog.query.get(int(time_log_id))
        if time_log and not time_log.end_time:
            time_log.end_time = datetime.utcnow()
            time_log.calculate_duration()
            
            # Update task actual hours
            task = time_log.task
            if task:
                task.actual_hours = (task.actual_hours or 0) + time_log.duration_hours
            
            db.session.commit()
        return time_log
    
    def get_active_time_log(self, user_id: str, task_id: str = None) -> Optional[TimeLog]:
        """Get active time log for user (optionally for specific task)"""
        query = TimeLog.query.filter_by(user_id=int(user_id), end_time=None)
        if task_id:
            query = query.filter_by(task_id=int(task_id))
        return query.first()
    
    def get_time_logs_for_task(self, task_id: str) -> List[TimeLog]:
        """Get all time logs for a task"""
        return TimeLog.query.filter_by(task_id=int(task_id)).order_by(TimeLog.start_time.desc()).all()
    
    def get_time_logs_for_user(self, user_id: str, start_date: datetime = None, end_date: datetime = None) -> List[TimeLog]:
        """Get time logs for a user within date range"""
        query = TimeLog.query.filter_by(user_id=int(user_id))
        
        if start_date:
            query = query.filter(TimeLog.start_time >= start_date)
        if end_date:
            query = query.filter(TimeLog.start_time <= end_date)
            
        return query.order_by(TimeLog.start_time.desc()).all()
    
    def update_task_estimate(self, task_id: str, estimated_hours: float) -> Optional[Task]:
        """Update task time estimate"""
        task = self.get_task(task_id)
        if task:
            task.estimated_hours = estimated_hours
            db.session.commit()
        return task
    
    def complete_task_with_time(self, task_id: str) -> Optional[Task]:
        """Complete task and record completion time"""
        task = self.get_task(task_id)
        if task:
            task.status = 'completed'
            task.completed_at = datetime.utcnow()
            
            # Stop any active time tracking for this task
            active_logs = TimeLog.query.filter_by(task_id=int(task_id), end_time=None).all()
            for log in active_logs:
                log.end_time = datetime.utcnow()
                log.calculate_duration()
                task.actual_hours = (task.actual_hours or 0) + log.duration_hours
            
            db.session.commit()
        return task
    
    def get_time_report_data(self, team_id: str = None, start_date: datetime = None, end_date: datetime = None):
        """Generate time tracking report data"""
        # Default to last 30 days if no date range specified
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        if not end_date:
            end_date = datetime.utcnow()
        
        # Base query for time logs
        query = db.session.query(TimeLog).join(Task).join(User)
        
        if team_id:
            query = query.filter(Task.team_id == int(team_id))
        
        query = query.filter(TimeLog.start_time >= start_date, TimeLog.start_time <= end_date)
        
        time_logs = query.all()
        
        # Calculate summary statistics
        total_hours = sum(log.duration_hours for log in time_logs if log.duration_hours)
        total_tasks = len(set(log.task_id for log in time_logs))
        total_users = len(set(log.user_id for log in time_logs))
        
        # Group by user
        user_stats = {}
        for log in time_logs:
            user_id = log.user_id
            if user_id not in user_stats:
                user_stats[user_id] = {
                    'user': log.user,
                    'total_hours': 0,
                    'task_count': set(),
                    'logs': []
                }
            user_stats[user_id]['total_hours'] += log.duration_hours or 0
            user_stats[user_id]['task_count'].add(log.task_id)
            user_stats[user_id]['logs'].append(log)
        
        # Convert sets to counts
        for user_id in user_stats:
            user_stats[user_id]['task_count'] = len(user_stats[user_id]['task_count'])
        
        return {
            'total_hours': total_hours,
            'total_tasks': total_tasks,
            'total_users': total_users,
            'user_stats': user_stats,
            'time_logs': time_logs,
            'start_date': start_date,
            'end_date': end_date
        }

# Global instance
data_manager = DataManager()