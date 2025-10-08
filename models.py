from app import db
from datetime import datetime
from typing import Optional


task_tags = db.Table(
    'task_tags',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    display_name = db.Column(db.String(200), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='analyst')  # 'analyst', 'manager', 'director'
    is_administrator = db.Column(db.Boolean, nullable=False, default=False)  # Administrator privilege
    is_active = db.Column(db.Boolean, nullable=False, default=True)  # Active status
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    
    # Relationships
    created_tasks = db.relationship('Task', foreign_keys='Task.created_by', backref='creator', lazy='dynamic')
    assigned_tasks = db.relationship('Task', foreign_keys='Task.assignee_id', backref='assignee', lazy='dynamic')
    supervised_tasks = db.relationship('Task', foreign_keys='Task.supervisor_id', backref='supervisor', lazy='dynamic')
    
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
            'display_name': self.display_name,
            'role': self.role,
            'is_administrator': self.is_administrator,
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
    is_active = db.Column(db.Boolean, nullable=False, default=True)  # Active status
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
    status = db.Column(db.String(20), nullable=False, default='todo')  # 'todo', 'in_progress', 'in_review', 'completed'
    priority = db.Column(db.String(20), nullable=False, default='medium')  # 'low', 'medium', 'high', 'urgent'
    complexity = db.Column(db.String(20), nullable=False, default='medium')  # 'very_simple', 'simple', 'medium', 'complex', 'very_complex'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Time tracking fields
    estimated_hours = db.Column(db.Float, nullable=True)
    actual_hours = db.Column(db.Float, nullable=True, default=0.0)
    started_at = db.Column(db.DateTime, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Foreign Keys
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    parent_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)  # For sub-tasks
    
    # Sub-task relationships
    parent_task = db.relationship('Task', remote_side=[id], backref=db.backref('subtasks', lazy='dynamic'))

    tags = db.relationship(
        'Tag',
        secondary=task_tags,
        back_populates='tasks',
        lazy='selectin'
    )
    custom_fields = db.relationship(
        'TaskCustomField',
        back_populates='task',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    
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
        # Import here to avoid circular imports
        from models import TimeLog
        time_logs = TimeLog.query.filter_by(task_id=self.id).all()
        return sum(log.duration_hours for log in time_logs if log.duration_hours) or 0.0
    
    def get_subtask_progress(self):
        """Calculate progress based on completed subtasks"""
        subtask_list = list(self.subtasks.all()) if self.subtasks else []
        if not subtask_list:
            return None
        
        total_subtasks = len(subtask_list)
        completed_subtasks = len([st for st in subtask_list if st.status == 'completed'])
        
        if total_subtasks == 0:
            return 0
        
        return (completed_subtasks / total_subtasks) * 100
    
    def is_subtask(self):
        """Check if this task is a subtask"""
        return self.parent_task_id is not None
    
    def can_be_completed(self):
        """Check if task can be completed (all subtasks must be completed)"""
        subtask_list = list(self.subtasks.all()) if self.subtasks else []
        incomplete_subtasks = [st for st in subtask_list if st.status != 'completed']
        return len(incomplete_subtasks) == 0
    
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
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'total_time_logged': self.get_total_time_logged(),
            'time_variance': self.get_time_variance(),
            'parent_task_id': str(self.parent_task_id) if self.parent_task_id else None,
            'subtask_progress': self.get_subtask_progress(),
            'subtask_count': self.subtasks.count() if self.subtasks else 0,
            'is_subtask': self.is_subtask(),
            'can_be_completed': self.can_be_completed(),
            'tags': [tag.to_dict() for tag in self.tags],
            'tag_names': [tag.name for tag in self.tags],
            'custom_fields': [field.to_dict() for field in self.custom_fields]
        }


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    color = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    tasks = db.relationship('Task', secondary=task_tags, back_populates='tags', lazy='selectin')

    def __repr__(self):
        return f'<Tag {self.name}>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'color': self.color,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class TaskCustomField(db.Model):
    __tablename__ = 'task_custom_fields'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    field_name = db.Column(db.String(100), nullable=False)
    field_value = db.Column(db.Text, nullable=True)
    field_type = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    task = db.relationship('Task', back_populates='custom_fields')

    def __repr__(self):
        return f'<TaskCustomField {self.field_name}>'

    def to_dict(self):
        return {
            'id': str(self.id),
            'task_id': str(self.task_id),
            'field_name': self.field_name,
            'field_value': self.field_value,
            'field_type': self.field_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class TaskAttachment(db.Model):
    __tablename__ = 'task_attachments'
    
    def __init__(self, task_id=None, filename=None, original_filename=None, file_size=None, file_type=None, uploaded_by=None):
        self.task_id = task_id
        self.filename = filename
        self.original_filename = original_filename
        self.file_size = file_size
        self.file_type = file_type
        self.uploaded_by = uploaded_by
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    file_type = db.Column(db.String(100), nullable=True)  # MIME type
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    task = db.relationship('Task', backref='attachments')
    uploader = db.relationship('User', backref='uploaded_files')
    
    def __repr__(self):
        return f'<TaskAttachment {self.original_filename}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'task_id': str(self.task_id),
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'uploaded_by': str(self.uploaded_by),
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
    
    def get_human_readable_size(self):
        """Convert file size to human readable format"""
        if self.file_size is None:
            return "0 B"
        
        size = float(self.file_size)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"


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

class TaskComment(db.Model):
    __tablename__ = 'task_comments'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relationships
    task = db.relationship('Task', backref=db.backref('comments', order_by='TaskComment.created_at'))
    user = db.relationship('User', backref='task_comments')
    
    def __repr__(self):
        return f'<TaskComment {self.id}: Task {self.task_id}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'task_id': str(self.task_id),
            'user_id': str(self.user_id),
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'user': {
                'username': self.user.username,
                'display_name': self.user.display_name or self.user.username
            } if self.user else None
        }

class TaskHistory(db.Model):
    __tablename__ = 'task_history'
    
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # 'created', 'updated', 'status_changed', etc.
    field_name = db.Column(db.String(50))  # which field was changed
    old_value = db.Column(db.Text)  # previous value
    new_value = db.Column(db.Text)  # new value
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relationships
    task = db.relationship('Task', backref=db.backref('history', order_by='TaskHistory.created_at.desc()'))
    user = db.relationship('User', backref='task_history')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_task_history_task', 'task_id'),
        db.Index('idx_task_history_user', 'user_id'),
        db.Index('idx_task_history_date', 'created_at'),
    )
    
    def __repr__(self):
        return f'<TaskHistory {self.id}: {self.action} on Task {self.task_id}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'task_id': str(self.task_id),
            'user_id': str(self.user_id),
            'action': self.action,
            'field_name': self.field_name,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user': {
                'username': self.user.username,
                'display_name': self.user.display_name or self.user.username
            } if self.user else None
        }
