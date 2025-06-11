from app import db
from datetime import datetime
from typing import Optional

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(200), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='analyst')  # 'analyst', 'manager', 'director', or 'admin'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    
    # Relationships
    created_tasks = db.relationship('Task', foreign_keys='Task.created_by', backref='creator', lazy='dynamic')
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assignee_id', backref='assignee', lazy='dynamic')
    
    def set_password(self, password):
        """Set password hash"""
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'team_id': str(self.team_id) if self.team_id else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Team(db.Model):
    __tablename__ = 'teams'
    
    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('User', backref='team', lazy='dynamic')
    tasks = db.relationship('Task', backref='team', lazy='dynamic')
    
    def __repr__(self):
        return f'<Team {self.name}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'member_count': self.members.count(),
            'task_count': self.tasks.count()
        }

class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='todo')  # 'todo', 'in_progress', 'completed'
    priority = db.Column(db.String(20), nullable=False, default='medium')  # 'low', 'medium', 'high', 'urgent'
    complexity = db.Column(db.String(20), nullable=False, default='medium')  # 'very_simple', 'simple', 'medium', 'complex', 'very_complex'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Time tracking fields
    estimated_hours = db.Column(db.Float, nullable=True)
    actual_hours = db.Column(db.Float, nullable=True, default=0.0)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Foreign Keys
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    
    # Indexes for better performance
    __table_args__ = (
        db.Index('idx_task_status', 'status'),
        db.Index('idx_task_assignee', 'assignee_id'),
        db.Index('idx_task_created_by', 'created_by'),
        db.Index('idx_task_team', 'team_id'),
    )
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    def get_total_time_logged(self):
        """Calculate total time logged from time entries"""
        return sum(log.duration_hours for log in self.time_logs if log.duration_hours) if hasattr(self, 'time_logs') else 0.0
    
    def get_time_variance(self):
        """Calculate variance between estimated and actual time"""
        if self.estimated_hours and self.actual_hours:
            return self.actual_hours - self.estimated_hours
        return None
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'complexity': self.complexity,
            'assignee_id': str(self.assignee_id) if self.assignee_id else None,
            'created_by': str(self.created_by),
            'team_id': str(self.team_id) if self.team_id else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'total_time_logged': self.get_total_time_logged(),
            'time_variance': self.get_time_variance()
        }


class TimeLog(db.Model):
    __tablename__ = 'time_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    duration_hours = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='time_logs')
    task = db.relationship('Task', backref='time_logs')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_time_log_task', 'task_id'),
        db.Index('idx_time_log_user', 'user_id'),
        db.Index('idx_time_log_date', 'start_time'),
    )
    
    def __repr__(self):
        return f'<TimeLog {self.id}: Task {self.task_id} - {self.duration_hours}h>'
    
    def calculate_duration(self):
        """Calculate duration between start and end time"""
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            self.duration_hours = delta.total_seconds() / 3600
        return self.duration_hours
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'task_id': str(self.task_id),
            'user_id': str(self.user_id),
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_hours': self.duration_hours,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
