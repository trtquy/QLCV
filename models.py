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
    
    # Hierarchy and Project fields
    parent_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    task_type = db.Column(db.String(20), nullable=False, default='task')  # 'epic', 'story', 'task', 'subtask'
    hierarchy_level = db.Column(db.Integer, nullable=False, default=0)  # 0=epic, 1=story, 2=task, 3=subtask
    
    # Relationships for hierarchy
    parent_task = db.relationship('Task', remote_side=[id], backref='child_tasks')
    
    # Indexes for better performance
    __table_args__ = (
        db.Index('idx_task_status', 'status'),
        db.Index('idx_task_assignee', 'assignee_id'),
        db.Index('idx_task_created_by', 'created_by'),
        db.Index('idx_task_team', 'team_id'),
        db.Index('idx_task_parent', 'parent_task_id'),
        db.Index('idx_task_project', 'project_id'),
        db.Index('idx_task_hierarchy', 'hierarchy_level'),
    )
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    # Hierarchy methods
    def get_children(self):
        """Get direct child tasks"""
        return Task.query.filter_by(parent_task_id=self.id).all()
    
    def get_all_descendants_new(self):
        """Get all descendant tasks recursively"""
        descendants = []
        for child in self.get_children():
            descendants.append(child)
            descendants.extend(child.get_all_descendants_new())
        return descendants
    
    def get_progress(self):
        """Calculate progress based on completed child tasks"""
        children = self.get_children()
        if not children:
            return 100.0 if self.status == 'completed' else 0.0
        
        completed_children = [c for c in children if c.status == 'completed']
        return (len(completed_children) / len(children)) * 100.0
    
    def can_start_new(self):
        """Check if task can start based on dependencies"""
        try:
            from models import TaskDependency
            dependencies = TaskDependency.query.filter_by(successor_task_id=self.id).all()
            if not dependencies:
                return True
            
            for dep in dependencies:
                predecessor = Task.query.get(dep.predecessor_task_id)
                if predecessor and predecessor.status != 'completed':
                    return False
            return True
        except:
            return True
    
    def is_blocked(self):
        """Check if task is blocked by dependencies"""
        return not self.can_start_new()
    
    @property
    def has_dependencies(self):
        """Check if task has any dependencies"""
        try:
            from models import TaskDependency
            return TaskDependency.query.filter_by(successor_task_id=self.id).count() > 0
        except:
            return False
    
    @property
    def blocks_others(self):
        """Check if task blocks other tasks"""
        try:
            from models import TaskDependency
            return TaskDependency.query.filter_by(predecessor_task_id=self.id).count() > 0
        except:
            return False
    
    def get_total_time_logged(self):
        """Calculate total time logged from time entries"""
        # Import here to avoid circular imports
        from models import TimeLog
        time_logs = TimeLog.query.filter_by(task_id=self.id).all()
        return sum(log.duration_hours for log in time_logs if log.duration_hours) or 0.0
    
    def get_time_variance(self):
        """Calculate variance between estimated and actual time"""
        if self.estimated_hours and self.actual_hours:
            return self.actual_hours - self.estimated_hours
        return None
    
    def get_child_progress(self):
        """Calculate progress based on child task completion"""
        from app import db
        children = db.session.query(Task).filter_by(parent_task_id=self.id).all()
        if not children:
            return None
        
        total_children = len(children)
        completed_children = len([child for child in children if child.status == 'completed'])
        
        if total_children == 0:
            return 0.0
        return (completed_children / total_children) * 100
    
    def get_all_descendants(self):
        """Get all descendant tasks recursively"""
        from app import db
        descendants = []
        children = db.session.query(Task).filter_by(parent_task_id=self.id).all()
        for child in children:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants
    
    def can_start(self):
        """Check if task can start based on dependencies"""
        from app import db
        # Check if all predecessor tasks are completed
        predecessors = db.session.query(TaskDependency).filter_by(successor_task_id=self.id).all()
        for dependency in predecessors:
            if dependency.predecessor.status != 'completed':
                return False
        return True
    
    def get_blocked_successors(self):
        """Get tasks that are blocked by this task"""
        from app import db
        blocked = []
        successors = db.session.query(TaskDependency).filter_by(predecessor_task_id=self.id).all()
        for dependency in successors:
            if dependency.successor.status == 'todo' and not dependency.successor.can_start():
                blocked.append(dependency.successor)
        return blocked
    
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
            'project_id': str(self.project_id) if self.project_id else None,
            'task_type': self.task_type,
            'hierarchy_level': self.hierarchy_level,
            'child_progress': self.get_child_progress(),
            'can_start': self.can_start()
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


class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='active')  # 'active', 'on_hold', 'completed', 'cancelled'
    priority = db.Column(db.String(20), nullable=False, default='medium')  # 'low', 'medium', 'high', 'critical'
    
    # Dates
    start_date = db.Column(db.DateTime, nullable=True)
    target_end_date = db.Column(db.DateTime, nullable=True)
    actual_end_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    
    # Relationships
    owner = db.relationship('User', backref='owned_projects')
    tasks = db.relationship('Task', backref='project', lazy='dynamic')
    
    # Indexes
    __table_args__ = (
        db.Index('idx_project_status', 'status'),
        db.Index('idx_project_owner', 'owner_id'),
        db.Index('idx_project_team', 'team_id'),
    )
    
    def __repr__(self):
        return f'<Project {self.name}>'
    
    def get_progress_percentage(self):
        """Calculate project progress based on completed tasks"""
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0.0
        completed_tasks = self.tasks.filter_by(status='completed').count()
        return (completed_tasks / total_tasks) * 100
    
    def get_task_counts_by_status(self):
        """Get task counts for each status"""
        return {
            'todo': self.tasks.filter_by(status='todo').count(),
            'in_progress': self.tasks.filter_by(status='in_progress').count(),
            'in_review': self.tasks.filter_by(status='in_review').count(),
            'completed': self.tasks.filter_by(status='completed').count(),
        }
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'target_end_date': self.target_end_date.isoformat() if self.target_end_date else None,
            'actual_end_date': self.actual_end_date.isoformat() if self.actual_end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'owner_id': str(self.owner_id),
            'team_id': str(self.team_id) if self.team_id else None,
            'progress_percentage': self.get_progress_percentage(),
            'task_counts': self.get_task_counts_by_status()
        }


class TaskDependency(db.Model):
    __tablename__ = 'task_dependencies'
    
    id = db.Column(db.Integer, primary_key=True)
    predecessor_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    successor_task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    dependency_type = db.Column(db.String(20), nullable=False, default='finish_to_start')  # 'finish_to_start', 'start_to_start', 'finish_to_finish', 'start_to_finish'
    lag_days = db.Column(db.Integer, nullable=False, default=0)  # Delay in days
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    predecessor = db.relationship('Task', foreign_keys=[predecessor_task_id], backref='successors')
    successor = db.relationship('Task', foreign_keys=[successor_task_id], backref='predecessors')
    creator = db.relationship('User', backref='created_dependencies')
    
    # Indexes and constraints
    __table_args__ = (
        db.Index('idx_dependency_predecessor', 'predecessor_task_id'),
        db.Index('idx_dependency_successor', 'successor_task_id'),
        db.UniqueConstraint('predecessor_task_id', 'successor_task_id', name='uq_task_dependency'),
    )
    
    def __repr__(self):
        return f'<TaskDependency {self.predecessor_task_id} -> {self.successor_task_id}>'
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'predecessor_task_id': str(self.predecessor_task_id),
            'successor_task_id': str(self.successor_task_id),
            'dependency_type': self.dependency_type,
            'lag_days': self.lag_days,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': str(self.created_by)
        }
