from typing import List, Optional, Dict
from models import User, Task, Team, TimeLog, Project, TaskDependency
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
                   assignee_id: Optional[str] = None, supervisor_id: Optional[str] = None,
                   priority: str = 'medium', complexity: str = 'medium', 
                   started_at=None, due_date=None) -> Task:
        """Create a new task"""
        # Determine initial status based on due date
        initial_status = 'in_progress' if due_date else 'todo'
        
        task = Task(
            title=title,
            description=description,
            created_by=int(created_by),
            assignee_id=int(assignee_id) if assignee_id else None,
            supervisor_id=int(supervisor_id) if supervisor_id else None,
            priority=priority,
            complexity=complexity,
            status=initial_status,
            started_at=started_at,
            due_date=due_date
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
    
    def get_team_managers(self, team_id: str) -> List[User]:
        """Get all managers from a specific team"""
        return User.query.filter_by(team_id=int(team_id), role='manager', is_active=True).all()
    
    def can_user_edit_task(self, user_id: str, task: Task) -> bool:
        """Check if user can edit a task (assignee or team manager)"""
        user = self.get_user(user_id)
        if not user or not task:
            return False
        
        # User is the assignee
        if task.assignee_id == int(user_id):
            return True
        
        # User is a manager of the task's team
        if user.role == 'manager' and task.team_id == user.team_id:
            return True
        
        return False
    
    def get_available_actions_for_task(self, user_id: str, task: Task) -> List[str]:
        """Get available actions for a user on a specific task"""
        user = self.get_user(user_id)
        if not user or not task:
            return []
        
        actions = []
        
        # Only assignee and team manager can modify tasks
        if not self.can_user_edit_task(user_id, task):
            return actions
        
        # If user is analyst and assigned to task
        if user.role == 'analyst' and task.assignee_id == int(user_id):
            if task.status == 'in_progress':
                actions.append('send_for_review')
            elif task.status == 'in_review':
                actions.append('recall')
        
        # Managers can do more actions
        elif user.role in ['manager', 'director']:
            if task.status == 'todo':
                actions.extend(['start', 'complete'])
            elif task.status == 'in_progress':
                actions.extend(['complete', 'send_for_review'])
            elif task.status == 'in_review':
                actions.extend(['approve', 'recall'])
        
        return actions
    
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
    
    # Project Management Methods
    def create_project(self, name: str, description: str = None, owner_id: str = None, team_id: str = None, 
                      priority: str = 'medium', start_date: datetime = None, target_end_date: datetime = None) -> Project:
        """Create a new project"""
        project = Project(
            name=name,
            description=description,
            owner_id=int(owner_id),
            team_id=int(team_id) if team_id else None,
            priority=priority,
            start_date=start_date,
            target_end_date=target_end_date
        )
        db.session.add(project)
        db.session.commit()
        return project
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get project by ID"""
        return Project.query.get(int(project_id))
    
    def get_projects_by_team(self, team_id: str) -> List[Project]:
        """Get projects by team"""
        return Project.query.filter_by(team_id=int(team_id)).all()
    
    def get_all_projects(self) -> List[Project]:
        """Get all projects"""
        return Project.query.all()
    
    def update_project_status(self, project_id: str, status: str) -> Optional[Project]:
        """Update project status"""
        project = self.get_project(project_id)
        if project:
            project.status = status
            if status == 'completed':
                project.actual_end_date = datetime.utcnow()
            db.session.commit()
        return project
    
    # Task Hierarchy Methods
    def create_child_task(self, parent_task_id: str, title: str, description: str = None, 
                         assignee_id: str = None, priority: str = 'medium', 
                         complexity: str = 'medium', task_type: str = 'subtask') -> Task:
        """Create a child task"""
        parent_task = self.get_task(parent_task_id)
        if not parent_task:
            raise ValueError("Parent task not found")
        
        # Determine hierarchy level
        hierarchy_level = parent_task.hierarchy_level + 1
        
        child_task = Task(
            title=title,
            description=description,
            assignee_id=int(assignee_id) if assignee_id else None,
            created_by=parent_task.created_by,
            team_id=parent_task.team_id,
            project_id=parent_task.project_id,
            priority=priority,
            complexity=complexity,
            parent_task_id=int(parent_task_id),
            task_type=task_type,
            hierarchy_level=hierarchy_level
        )
        
        db.session.add(child_task)
        db.session.commit()
        return child_task
    
    def get_child_tasks(self, parent_task_id: str) -> List[Task]:
        """Get child tasks of a parent task"""
        return Task.query.filter_by(parent_task_id=int(parent_task_id)).all()
    
    def get_root_tasks(self) -> List[Task]:
        """Get tasks with no parent (root level tasks)"""
        return Task.query.filter_by(parent_task_id=None).all()
    
    def move_task_to_project(self, task_id: str, project_id: str) -> Optional[Task]:
        """Move task to a different project"""
        task = self.get_task(task_id)
        if task:
            task.project_id = int(project_id) if project_id else None
            db.session.commit()
        return task
    
    # Task Dependency Methods
    def create_task_dependency(self, predecessor_task_id: str, successor_task_id: str, 
                              dependency_type: str = 'finish_to_start', lag_days: int = 0, 
                              created_by: str = None) -> TaskDependency:
        """Create a task dependency"""
        # Check if dependency already exists
        existing = TaskDependency.query.filter_by(
            predecessor_task_id=int(predecessor_task_id),
            successor_task_id=int(successor_task_id)
        ).first()
        
        if existing:
            raise ValueError("Dependency already exists between these tasks")
        
        # Check for circular dependencies
        if self._would_create_circular_dependency(predecessor_task_id, successor_task_id):
            raise ValueError("This dependency would create a circular reference")
        
        dependency = TaskDependency(
            predecessor_task_id=int(predecessor_task_id),
            successor_task_id=int(successor_task_id),
            dependency_type=dependency_type,
            lag_days=lag_days,
            created_by=int(created_by) if created_by else None
        )
        
        db.session.add(dependency)
        db.session.commit()
        return dependency
    
    def get_task_dependencies(self, task_id: str) -> Dict[str, List[TaskDependency]]:
        """Get both predecessor and successor dependencies for a task"""
        predecessors = TaskDependency.query.filter_by(successor_task_id=int(task_id)).all()
        successors = TaskDependency.query.filter_by(predecessor_task_id=int(task_id)).all()
        
        return {
            'predecessors': predecessors,
            'successors': successors
        }
    
    def remove_task_dependency(self, dependency_id: str) -> bool:
        """Remove a task dependency"""
        dependency = TaskDependency.query.get(int(dependency_id))
        if dependency:
            db.session.delete(dependency)
            db.session.commit()
            return True
        return False
    
    def _would_create_circular_dependency(self, predecessor_id: str, successor_id: str) -> bool:
        """Check if adding a dependency would create a circular reference"""
        # Simple check: if successor_id is already a predecessor of predecessor_id
        visited = set()
        
        def has_path(start_id: str, target_id: str) -> bool:
            if start_id in visited:
                return False
            visited.add(start_id)
            
            if start_id == target_id:
                return True
            
            # Get all tasks that this task depends on
            dependencies = TaskDependency.query.filter_by(successor_task_id=int(start_id)).all()
            for dep in dependencies:
                if has_path(str(dep.predecessor_task_id), target_id):
                    return True
            return False
        
        return has_path(successor_id, predecessor_id)
    
    def get_blocked_tasks(self) -> List[Task]:
        """Get tasks that are blocked by dependencies"""
        blocked_tasks = []
        all_tasks = Task.query.filter_by(status='todo').all()
        
        for task in all_tasks:
            if not task.can_start():
                blocked_tasks.append(task)
        
        return blocked_tasks
    
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
        
        # Generate daily time data for charts
        daily_data = self._generate_daily_time_data(time_logs, start_date, end_date)
        
        # Generate team time data for charts
        team_data = self._generate_team_time_data(time_logs)
        
        return {
            'total_hours': total_hours,
            'total_tasks': total_tasks,
            'total_users': total_users,
            'user_stats': user_stats,
            'time_logs': time_logs,
            'start_date': start_date,
            'end_date': end_date,
            'daily_data': daily_data,
            'team_data': team_data
        }
    
    def _generate_daily_time_data(self, time_logs, start_date, end_date):
        """Generate daily time tracking data for charts"""
        from collections import defaultdict
        
        daily_hours = defaultdict(float)
        current_date = start_date.date()
        end_date_only = end_date.date()
        
        # Initialize all dates with 0 hours
        while current_date <= end_date_only:
            daily_hours[current_date.strftime('%Y-%m-%d')] = 0
            current_date += timedelta(days=1)
        
        # Aggregate hours by date
        for log in time_logs:
            if log.duration_hours and log.start_time:
                date_key = log.start_time.strftime('%Y-%m-%d')
                daily_hours[date_key] += log.duration_hours
        
        # Sort by date and prepare for Chart.js
        sorted_dates = sorted(daily_hours.keys())
        return {
            'dates': sorted_dates,
            'hours': [daily_hours[date] for date in sorted_dates]
        }
    
    def _generate_team_time_data(self, time_logs):
        """Generate team-based time tracking data for charts"""
        from collections import defaultdict
        
        team_hours = defaultdict(float)
        
        # Aggregate hours by team
        for log in time_logs:
            if log.duration_hours and log.task and log.task.team:
                team_name = log.task.team.name
                team_hours[team_name] += log.duration_hours
        
        # If no team data, use individual user data
        if not team_hours:
            for log in time_logs:
                if log.duration_hours and log.user:
                    user_name = log.user.display_name or log.user.username
                    team_hours[user_name] += log.duration_hours
        
        return {
            'names': list(team_hours.keys()),
            'hours': list(team_hours.values())
        }

# Global instance
data_manager = DataManager()