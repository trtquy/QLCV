from flask import render_template, request, redirect, url_for, flash, session, jsonify, send_file
from app import app, db
from data_manager import data_manager
from models import Team, TaskAttachment
from datetime import datetime, timedelta
import logging
import os
import uuid
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    """Main kanban board page"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    users = data_manager.get_all_users()
    teams = data_manager.get_all_teams()
    
    # Team-based filtering: Users only see their team's tasks (except administrators)
    if current_user.is_administrator:
        # Administrators can see all tasks
        tasks = data_manager.get_all_tasks()
        # Filter by team if specified in URL
        team_filter = request.args.get('team')
        if team_filter:
            tasks = [t for t in tasks if str(t.team_id) == team_filter]
    else:
        # Regular users only see tasks from their team
        if current_user.team_id:
            tasks = data_manager.get_tasks_by_team(str(current_user.team_id))
            team_filter = str(current_user.team_id)  # Set current team as filter
        else:
            tasks = []
            team_filter = None
    
    # Organize tasks by status
    todo_tasks = [t for t in tasks if t.status == 'todo']
    in_progress_tasks = [t for t in tasks if t.status == 'in_progress']
    in_review_tasks = [t for t in tasks if t.status == 'in_review']
    completed_tasks = [t for t in tasks if t.status == 'completed']
    
    return render_template('index.html', 
                         todo_tasks=todo_tasks,
                         in_progress_tasks=in_progress_tasks,
                         in_review_tasks=in_review_tasks,
                         completed_tasks=completed_tasks,
                         users=users,
                         teams=teams,
                         current_user=current_user,
                         selected_team=team_filter)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username_or_email = request.form.get('username')
        password = request.form.get('password')
        
        if username_or_email and password:
            user = data_manager.authenticate_user(username_or_email, password)
            if user:
                data_manager.set_current_user(user.id)
                session['user_id'] = user.id
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect(url_for('index', welcome='true'))
            else:
                flash('Invalid username/email or password', 'error')
        else:
            flash('Please enter both username/email and password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout current user"""
    data_manager.logout_current_user()
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    """User profile page"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    return render_template('profile.html', current_user=current_user)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    """Update user profile"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    display_name = request.form.get('display_name', '').strip()
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Update display name if provided
    if display_name:
        data_manager.update_user(current_user.id, display_name=display_name)
        flash('Display name updated successfully', 'success')
    
    # Update password if provided
    if current_password and new_password and confirm_password:
        # Verify current password
        if not current_user.check_password(current_password):
            flash('Current password is incorrect', 'error')
            return redirect(url_for('profile'))
        
        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
            return redirect(url_for('profile'))
        
        # Check password strength
        if len(new_password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return redirect(url_for('profile'))
        
        # Update password
        current_user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully', 'success')
    elif current_password or new_password or confirm_password:
        # Partial password fields provided
        flash('All password fields are required to change password', 'error')
        return redirect(url_for('profile'))
    
    return redirect(url_for('profile'))

@app.route('/create_task', methods=['POST'])
def create_task():
    """Create a new task - Only managers can create tasks"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    # Check if user is a manager or admin
    if current_user.role not in ['manager', 'admin']:
        flash('Only managers and admins can create tasks', 'error')
        return redirect(url_for('index'))
    
    # Check if manager has a team assigned (admins can create tasks without teams)
    if current_user.role == 'manager' and not current_user.team_id:
        flash('Manager must be assigned to a team to create tasks', 'error')
        return redirect(url_for('index'))
    
    title = request.form.get('title')
    description = request.form.get('description', '')
    assignee_id = request.form.get('assignee_id') or None
    supervisor_id = request.form.get('supervisor_id') or None
    priority = request.form.get('priority', 'medium')
    complexity = request.form.get('complexity', 'medium')
    estimated_hours = request.form.get('estimated_hours')
    started_at = request.form.get('started_at')
    due_date = request.form.get('due_date')
    
    if title:
        # Parse date fields
        parsed_started_at = None
        parsed_due_date = None
        
        if started_at:
            try:
                from datetime import datetime
                parsed_started_at = datetime.strptime(started_at, '%Y-%m-%d')
            except ValueError:
                pass
                
        if due_date:
            try:
                from datetime import datetime
                parsed_due_date = datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                pass
        
        task = data_manager.create_task(
            title=title,
            description=description,
            created_by=current_user.id,
            assignee_id=assignee_id,
            supervisor_id=supervisor_id,
            priority=priority,
            complexity=complexity,
            started_at=parsed_started_at,
            due_date=parsed_due_date
        )
        
        # Automatically set task team to manager's team (if manager has team)
        if current_user.team_id:
            data_manager.update_task(task.id, team_id=current_user.team_id)
        
        # Set estimated hours if provided
        if estimated_hours:
            try:
                est_hours = float(estimated_hours)
                data_manager.update_task_estimate(str(task.id), est_hours)
            except (ValueError, TypeError):
                pass  # Ignore invalid estimates
        
        flash('Task created successfully!', 'success')
    else:
        flash('Task title is required', 'error')
    
    return redirect(url_for('index'))

@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    """Update task status or details"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    # Get the task first to check permissions
    task = data_manager.get_task(task_id)
    if not task:
        if 'status' in request.form:
            return jsonify({'success': False, 'error': 'Task not found'})
        flash('Task not found', 'error')
        return redirect(url_for('index'))
    
    # Check edit permissions - same as priority permissions
    can_edit = (
        current_user.is_administrator or  # Administrators can edit all tasks
        task.assignee_id == current_user.id or  # Assignees can edit their tasks
        task.created_by == current_user.id or  # Task creators can edit their tasks
        (current_user.role in ['manager', 'director'] and task.team_id == current_user.team_id)  # Team managers can edit team tasks
    )
    
    if not can_edit:
        if 'status' in request.form:
            return jsonify({'success': False, 'error': 'Permission denied'})
        flash('You do not have permission to edit this task', 'error')
        return redirect(url_for('index'))
    
    # Handle status update (for drag and drop)
    if 'status' in request.form:
        new_status = request.form.get('status')
        updated_task = data_manager.update_task(task_id, status=new_status)
        if updated_task:
            return jsonify({'success': True, 'task_id': task_id, 'new_status': new_status})
        else:
            return jsonify({'success': False, 'error': 'Failed to update task'})
    
    # Handle full task update
    title = request.form.get('title')
    description = request.form.get('description', '')
    assignee_id = request.form.get('assignee_id') or None
    supervisor_id = request.form.get('supervisor_id') or None
    priority = request.form.get('priority', 'medium')
    complexity = request.form.get('complexity', 'medium')
    status = request.form.get('task_status', 'todo')
    team_id = request.form.get('team_id') or None
    estimated_hours = request.form.get('estimated_hours')
    started_at = request.form.get('started_at')
    due_date = request.form.get('due_date')
    completed_at = request.form.get('completed_at')
    
    if title:
        # Parse date fields
        parsed_started_at = None
        parsed_due_date = None
        parsed_completed_at = None
        
        if started_at:
            try:
                from datetime import datetime
                parsed_started_at = datetime.strptime(started_at, '%Y-%m-%d')
            except ValueError:
                pass
                
        if due_date:
            try:
                from datetime import datetime
                parsed_due_date = datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                pass
                
        if completed_at:
            try:
                from datetime import datetime
                parsed_completed_at = datetime.strptime(completed_at, '%Y-%m-%d')
            except ValueError:
                pass
        
        # Handle automatic workflow progression: To Do → In Progress when Due Date is added
        auto_progress = request.form.get('auto_progress')
        if auto_progress == 'true' and task.status == 'todo' and parsed_due_date:
            status = 'in_progress'
            # Auto-set started_at when moving to in_progress
            if not parsed_started_at:
                from datetime import datetime
                parsed_started_at = datetime.utcnow()
        
        # Auto-set completed date when status changes to completed
        if status == 'completed' and not parsed_completed_at:
            from datetime import datetime
            parsed_completed_at = datetime.utcnow()
        
        task = data_manager.update_task(
            task_id,
            title=title,
            description=description,
            assignee_id=assignee_id,
            supervisor_id=supervisor_id,
            priority=priority,
            complexity=complexity,
            status=status,
            team_id=team_id,
            started_at=parsed_started_at,
            due_date=parsed_due_date,
            completed_at=parsed_completed_at
        )
        
        # Update estimated hours if provided
        if estimated_hours:
            try:
                est_hours = float(estimated_hours)
                data_manager.update_task_estimate(task_id, est_hours)
            except (ValueError, TypeError):
                pass  # Ignore invalid estimates
        if task:
            flash('Task updated successfully!', 'success')
        else:
            flash('Task not found', 'error')
    else:
        flash('Task title is required', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    """Delete a task"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    if data_manager.delete_task(task_id):
        flash('Task deleted successfully!', 'success')
    else:
        flash('Task not found', 'error')
    
    return redirect(url_for('index'))

@app.route('/task/<task_id>/send_for_review', methods=['POST'])
def send_task_for_review(task_id):
    """Send task for review (analyst action)"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    task = data_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('index'))
    
    # Check if user can perform this action
    if not data_manager.can_user_edit_task(str(current_user.id), task):
        flash('You do not have permission to modify this task', 'error')
        return redirect(url_for('index'))
    
    # Allow if task is in progress and user is assigned to task (any role)
    if task.status == 'in_progress' and task.assignee_id == current_user.id:
        data_manager.update_task(task_id, status='in_review')
        flash('Task sent for review successfully!', 'success')
    else:
        flash('Task cannot be sent for review at this time', 'error')
    
    return redirect(url_for('index'))

@app.route('/task/<task_id>/recall', methods=['POST'])
def recall_task(task_id):
    """Recall task from review (analyst action)"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    task = data_manager.get_task(task_id)
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('index'))
    
    # Check if user can perform this action
    if not data_manager.can_user_edit_task(str(current_user.id), task):
        flash('You do not have permission to modify this task', 'error')
        return redirect(url_for('index'))
    
    # Only allow if task is in review and user is analyst assigned to task
    if task.status == 'in_review' and current_user.role == 'analyst' and task.assignee_id == current_user.id:
        data_manager.update_task(task_id, status='in_progress')
        flash('Task recalled from review successfully!', 'success')
    else:
        flash('Task cannot be recalled at this time', 'error')
    
    return redirect(url_for('index'))

@app.route('/approve_task/<task_id>', methods=['POST'])
def approve_task(task_id):
    """Approve task (supervisor action)"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    task = data_manager.get_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Only the assigned supervisor can approve tasks
    if not (current_user.is_administrator or task.supervisor_id == current_user.id):
        return jsonify({'error': 'Only the assigned supervisor can approve tasks'}), 403
    
    # Task must be in review status
    if task.status != 'in_review':
        return jsonify({'error': 'Task must be in review status to approve'}), 400
    
    try:
        # Update task status to completed and set completion time
        updated_task = data_manager.complete_task_with_time(task_id)
        if updated_task:
            return jsonify({'success': True, 'message': f'Task "{task.title}" approved and completed'})
        else:
            return jsonify({'error': 'Failed to approve task'}), 500
    except Exception as e:
        logging.error(f"Error approving task {task_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/reject_task/<task_id>', methods=['POST'])
def reject_task(task_id):
    """Reject task and send back to in progress (supervisor action)"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    task = data_manager.get_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Only the assigned supervisor can reject tasks
    if not (current_user.is_administrator or task.supervisor_id == current_user.id):
        return jsonify({'error': 'Only the assigned supervisor can reject tasks'}), 403
    
    # Task must be in review status
    if task.status != 'in_review':
        return jsonify({'error': 'Task must be in review status to reject'}), 400
    
    try:
        reason = request.form.get('reason', 'No reason provided')
        
        # Update task status back to in_progress
        updated_task = data_manager.update_task(task_id, status='in_progress')
        if updated_task:
            # Log rejection reason
            logging.info(f"Task {task_id} rejected by {current_user.username}. Reason: {reason}")
            return jsonify({'success': True, 'message': f'Task "{task.title}" rejected and sent back to in progress'})
        else:
            return jsonify({'error': 'Failed to reject task'}), 500
    except Exception as e:
        logging.error(f"Error rejecting task {task_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/get_task_data/<task_id>')
def get_task_data(task_id):
    """Get task data for editing"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify({'error': 'Not authenticated'}), 401
    
    task = data_manager.get_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Convert task to dictionary with related objects
    task_dict = task.to_dict()
    
    # Add assignee and supervisor details
    if task.assignee_id:
        assignee = data_manager.get_user(str(task.assignee_id))
        if assignee:
            task_dict['assignee'] = {
                'id': assignee.id,
                'username': assignee.username,
                'display_name': assignee.display_name
            }
    
    if task.supervisor_id:
        supervisor = data_manager.get_user(str(task.supervisor_id))
        if supervisor:
            task_dict['supervisor'] = {
                'id': supervisor.id,
                'username': supervisor.username,
                'display_name': supervisor.display_name
            }
    
    return jsonify(task_dict)

@app.route('/search')
def search():
    """Search tasks"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    query = request.args.get('q', '')
    filter_status = request.args.get('status', '')
    filter_assignee = request.args.get('assignee', '')
    
    if query:
        tasks = data_manager.search_tasks(query)
    else:
        tasks = data_manager.get_all_tasks()
    
    # Apply filters
    if filter_status:
        tasks = [t for t in tasks if t.status == filter_status]
    
    if filter_assignee:
        tasks = [t for t in tasks if t.assignee_id == filter_assignee]
    
    users = data_manager.get_all_users()
    
    return render_template('search.html', 
                         tasks=tasks, 
                         users=users, 
                         current_user=current_user,
                         query=query,
                         filter_status=filter_status,
                         filter_assignee=filter_assignee)

@app.route('/dashboard')
def dashboard():
    """Performance dashboard"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    users = data_manager.get_all_users()
    
    # Team-based filtering: Users only see their team's tasks (except administrators)
    if current_user.is_administrator:
        tasks = data_manager.get_all_tasks()
    else:
        # Regular users only see tasks from their team
        if current_user.team_id:
            tasks = data_manager.get_tasks_by_team(str(current_user.team_id))
        else:
            tasks = []
    
    # Calculate metrics
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == 'completed'])
    in_progress_tasks = len([t for t in tasks if t.status == 'in_progress'])
    todo_tasks = len([t for t in tasks if t.status == 'todo'])
    
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # User performance with detailed status counts
    user_stats = {}
    for user in users:
        user_tasks = [t for t in tasks if t.assignee_id == user.id]
        user_todo = len([t for t in user_tasks if t.status == 'todo'])
        user_in_progress = len([t for t in user_tasks if t.status == 'in_progress'])
        user_in_review = len([t for t in user_tasks if t.status == 'in_review'])
        user_completed = len([t for t in user_tasks if t.status == 'completed'])
        user_total = len(user_tasks)
        user_stats[str(user.id)] = {
            'user': user.to_dict(),
            'total_tasks': user_total,
            'todo_tasks': user_todo,
            'in_progress_tasks': user_in_progress,
            'in_review_tasks': user_in_review,
            'completed_tasks': user_completed,
            'completion_rate': (user_completed / user_total * 100) if user_total > 0 else 0
        }
    
    # Priority distribution
    priority_stats = {
        'urgent': len([t for t in tasks if t.priority == 'urgent']),
        'high': len([t for t in tasks if t.priority == 'high']),
        'medium': len([t for t in tasks if t.priority == 'medium']),
        'low': len([t for t in tasks if t.priority == 'low'])
    }
    
    return render_template('dashboard.html',
                         current_user=current_user,
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         in_progress_tasks=in_progress_tasks,
                         todo_tasks=todo_tasks,
                         completion_rate=completion_rate,
                         user_stats=user_stats,
                         priority_stats=priority_stats)

@app.route('/team')
def team():
    """Team management page"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    users = data_manager.get_all_users()
    tasks = data_manager.get_all_tasks()
    teams = data_manager.get_all_teams()
    
    return render_template('team.html',
                         current_user=current_user,
                         users=users,
                         tasks=tasks,
                         teams=teams)

@app.route('/update_user_role/<user_id>', methods=['POST'])
def update_user_role(user_id):
    """Update user role (administrator only)"""
    current_user = data_manager.get_current_user()
    if not current_user or not current_user.is_administrator:
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('team'))
    
    new_role = request.form.get('role')
    is_admin = request.form.get('is_administrator') == 'on'
    
    if new_role in ['analyst', 'manager', 'director']:
        user = data_manager.update_user(user_id, role=new_role, is_administrator=is_admin)
        if user:
            flash(f'User role updated successfully!', 'success')
        else:
            flash('User not found', 'error')
    else:
        flash('Invalid role', 'error')
    
    return redirect(url_for('team'))

@app.route('/move_member_to_team', methods=['POST'])
def move_member_to_team():
    """Move a team member to a different team (administrator only)"""
    current_user = data_manager.get_current_user()
    if not current_user or not current_user.is_administrator:
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('team'))
    
    user_id = request.form.get('user_id')
    team_id = request.form.get('team_id')
    
    if user_id and team_id:
        user = data_manager.get_user(user_id)
        team = data_manager.get_team(team_id)
        
        if user and team:
            # Update user's team
            data_manager.update_user(user_id, team_id=int(team_id))
            flash(f'{user.username} moved to {team.name} successfully', 'success')
        else:
            flash('User or team not found', 'error')
    else:
        flash('Please select both user and team', 'error')
    
    return redirect(url_for('team'))

@app.route('/add_team_member', methods=['POST'])
def add_team_member():
    """Add a new team member (administrator only)"""
    current_user = data_manager.get_current_user()
    if not current_user or not current_user.is_administrator:
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('team'))
    
    username = request.form.get('username')
    email = request.form.get('email')
    team_id = request.form.get('team_id')
    role = request.form.get('role', 'analyst')
    
    # Validate required fields based on role
    if not username or not email:
        flash('Username and email are required', 'error')
        return redirect(url_for('team'))
    
    # Directors and Admins don't require team assignment
    if role in ['analyst', 'manager'] and not team_id:
        flash('Team assignment is required for Analysts and Managers', 'error')
        return redirect(url_for('team'))
    
    if username and email:
        # Check if user already exists by username
        existing_user = data_manager.get_user_by_username(username)
        if existing_user:
            flash(f'Username {username} already exists', 'error')
            return redirect(url_for('team'))
        
        # Check if email already exists
        existing_users = data_manager.get_all_users()
        for user in existing_users:
            if user.email.lower() == email.lower():
                flash(f'Email {email} already exists', 'error')
                return redirect(url_for('team'))
        
        try:
            # Create new user
            user = data_manager.create_user(username, email, role)
            if user:
                # Assign to team only if role requires it and team_id is provided
                if team_id and role in ['analyst', 'manager']:
                    data_manager.update_user(str(user.id), team_id=int(team_id))
                    team = data_manager.get_team(team_id)
                    team_name = team.name if team else "team"
                    flash(f'User {username} added to {team_name} successfully', 'success')
                else:
                    flash(f'User {username} created successfully', 'success')
            else:
                flash('Failed to create user', 'error')
        except Exception as e:
            flash('Email or username already exists', 'error')
    else:
        flash('Please fill in all required fields', 'error')
    
    return redirect(url_for('team'))

@app.route('/create_team', methods=['POST'])
def create_team():
    """Create a new team (administrator only)"""
    current_user = data_manager.get_current_user()
    if not current_user or not current_user.is_administrator:
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('team'))
    
    team_name = request.form.get('team_name')
    team_description = request.form.get('team_description', '')
    
    if team_name:
        try:
            team = Team(name=team_name, description=team_description)
            db.session.add(team)
            db.session.commit()
            flash(f'Team "{team_name}" created successfully', 'success')
        except Exception as e:
            flash('Team name already exists', 'error')
    else:
        flash('Team name is required', 'error')
    
    return redirect(url_for('team'))

@app.route('/edit_team/<team_id>', methods=['POST'])
def edit_team(team_id):
    """Edit team details (administrator only)"""
    current_user = data_manager.get_current_user()
    if not current_user or not current_user.is_administrator:
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('team'))
    
    team = data_manager.get_team(team_id)
    if not team:
        flash('Team not found', 'error')
        return redirect(url_for('team'))
    
    new_name = request.form.get('team_name')
    new_description = request.form.get('team_description', '')
    
    if new_name:
        try:
            team.name = new_name
            team.description = new_description
            db.session.commit()
            flash(f'Team updated successfully', 'success')
        except Exception as e:
            flash('Team name already exists', 'error')
    else:
        flash('Team name is required', 'error')
    
    return redirect(url_for('team'))

@app.route('/delete_user/<user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete a user (administrator only)"""
    current_user = data_manager.get_current_user()
    if not current_user or not current_user.is_administrator:
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('team'))
    
    # Prevent self-deletion
    if str(current_user.id) == user_id:
        flash('Cannot delete your own account', 'error')
        return redirect(url_for('team'))
    
    user = data_manager.get_user(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('team'))
    
    try:
        # Reassign tasks created by this user to current admin
        from models import Task
        created_tasks = Task.query.filter_by(created_by=int(user_id)).all()
        for task in created_tasks:
            task.created_by = current_user.id
        
        # Unassign tasks assigned to this user
        assigned_tasks = Task.query.filter_by(assignee_id=int(user_id)).all()
        for task in assigned_tasks:
            task.assignee_id = None
        
        # Delete time logs
        from models import TimeLog
        TimeLog.query.filter_by(user_id=int(user_id)).delete()
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        flash(f'User {user.username} deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting user. Please try again.', 'error')
    
    return redirect(url_for('team'))

@app.route('/toggle_user_status/<user_id>', methods=['POST'])
def toggle_user_status(user_id):
    """Toggle user active status (administrator only)"""
    current_user = data_manager.get_current_user()
    if not current_user or not current_user.is_administrator:
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('team'))
    
    # Prevent self-deactivation
    if str(current_user.id) == user_id:
        flash('Cannot deactivate your own account', 'error')
        return redirect(url_for('team'))
    
    user = data_manager.get_user(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('team'))
    
    try:
        user.is_active = not user.is_active
        db.session.commit()
        
        status = "activated" if user.is_active else "deactivated"
        flash(f'User {user.username} {status} successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating user status. Please try again.', 'error')
    
    return redirect(url_for('team'))

@app.route('/delete_team/<team_id>', methods=['POST'])
def delete_team(team_id):
    """Delete a team (administrator only)"""
    current_user = data_manager.get_current_user()
    if not current_user or not current_user.is_administrator:
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('team'))
    
    team = data_manager.get_team(team_id)
    if not team:
        flash('Team not found', 'error')
        return redirect(url_for('team'))
    
    # Check if team has members
    team_members = data_manager.get_users_by_team(team_id)
    if team_members:
        flash(f'Cannot delete team with {len(team_members)} members. Move members first.', 'error')
        return redirect(url_for('team'))
    
    try:
        # Delete team tasks
        from models import Task
        Task.query.filter_by(team_id=int(team_id)).delete()
        
        # Delete the team
        db.session.delete(team)
        db.session.commit()
        
        flash(f'Team {team.name} deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting team. Please try again.', 'error')
    
    return redirect(url_for('team'))

@app.route('/toggle_team_status/<team_id>', methods=['POST'])
def toggle_team_status(team_id):
    """Toggle team active status (administrator only)"""
    current_user = data_manager.get_current_user()
    if not current_user or not current_user.is_administrator:
        flash('Access denied. Administrator privileges required.', 'error')
        return redirect(url_for('team'))
    
    team = data_manager.get_team(team_id)
    if not team:
        flash('Team not found', 'error')
        return redirect(url_for('team'))
    
    try:
        team.is_active = not team.is_active
        db.session.commit()
        
        status = "activated" if team.is_active else "deactivated"
        flash(f'Team {team.name} {status} successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error updating team status. Please try again.', 'error')
    
    return redirect(url_for('team'))

# Time tracking routes
@app.route('/time/start/<task_id>', methods=['POST'])
def start_time_tracking(task_id):
    """Start time tracking for a task"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify({'error': 'Not logged in'}), 401
    
    description = request.form.get('description', '')
    time_log = data_manager.start_time_tracking(task_id, str(current_user.id), description)
    
    if time_log:
        return jsonify({
            'success': True,
            'time_log_id': str(time_log.id),
            'message': 'Time tracking started'
        })
    else:
        return jsonify({'error': 'Failed to start time tracking'}), 400

@app.route('/time/stop/<time_log_id>', methods=['POST'])
def stop_time_tracking(time_log_id):
    """Stop time tracking"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify({'error': 'Not logged in'}), 401
    
    time_log = data_manager.stop_time_tracking(time_log_id)
    
    if time_log:
        return jsonify({
            'success': True,
            'duration_hours': time_log.duration_hours,
            'message': f'Time tracking stopped. Duration: {time_log.duration_hours:.2f} hours'
        })
    else:
        return jsonify({'error': 'Failed to stop time tracking'}), 400

@app.route('/time/active')
def get_active_time_log():
    """Get active time log for current user"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify({'error': 'Not logged in'}), 401
    
    active_log = data_manager.get_active_time_log(str(current_user.id))
    
    if active_log:
        return jsonify({
            'active': True,
            'time_log': active_log.to_dict()
        })
    else:
        return jsonify({'active': False})

@app.route('/time/report')
def time_report():
    """Time tracking report page"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    # Get date range from query parameters
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    team_id = request.args.get('team_id')
    
    start_date = None
    end_date = None
    
    if start_date_str:
        try:
            from datetime import datetime
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid start date format', 'error')
    
    if end_date_str:
        try:
            from datetime import datetime
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid end date format', 'error')
    
    # Provide default dates if not specified
    if start_date is None or end_date is None:
        from datetime import datetime, timedelta
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
    
    # Handle team_id parameter - data_manager expects a string, use empty string if None
    team_filter = team_id if team_id else ""
    
    report_data = data_manager.get_time_report_data(team_filter, start_date, end_date)
    teams = data_manager.get_all_teams()
    
    return render_template('time_report.html', 
                         report_data=report_data,
                         teams=teams,
                         current_user=current_user,
                         selected_team_id=team_id,
                         start_date=start_date_str,
                         end_date=end_date_str)

@app.route('/task/estimate/<task_id>', methods=['POST'])
def update_task_estimate(task_id):
    """Update task time estimate"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify({'error': 'Not logged in'}), 401
    
    estimated_hours = request.form.get('estimated_hours')
    try:
        estimated_hours = float(estimated_hours) if estimated_hours is not None else 0.0
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid hours format'}), 400
    
    task = data_manager.update_task_estimate(task_id, estimated_hours)
    
    if task:
        return jsonify({
            'success': True,
            'estimated_hours': task.estimated_hours,
            'message': 'Task estimate updated'
        })
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/update_task_priority/<task_id>', methods=['POST'])
def update_task_priority(task_id):
    """Update task priority"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Check if user can edit priority 
    task = data_manager.get_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Allow editing if:
    # - User is administrator
    # - User is assigned to the task  
    # - User is manager/director and task is in their team
    can_edit = (current_user.is_administrator or 
                (task.assignee_id and task.assignee_id == current_user.id) or
                (current_user.role in ['manager', 'director'] and 
                 task.team_id == current_user.team_id))
    
    if not can_edit:
        return jsonify({'error': 'Permission denied'}), 403
    
    new_priority = request.form.get('priority')
    if new_priority not in ['low', 'medium', 'high', 'urgent']:
        return jsonify({'error': 'Invalid priority'}), 400
    
    # Update task priority
    updated_task = data_manager.update_task(task_id, priority=new_priority)
    
    if updated_task:
        return jsonify({
            'success': True,
            'priority': new_priority,
            'message': f'Priority updated to {new_priority}'
        })
    else:
        return jsonify({'error': 'Failed to update priority'}), 500

# Template context processors
@app.route('/task/<int:task_id>/detail')
def task_detail(task_id):
    """Display detailed task view with comments and history"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    task = data_manager.get_task(str(task_id))
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('index'))
    
    # Check if user can view this task (same team or admin)
    can_view = (current_user.is_administrator or 
                task.team_id == current_user.team_id or
                task.assignee_id == current_user.id or
                task.created_by == current_user.id)
    
    if not can_view:
        flash('You do not have permission to view this task', 'error')
        return redirect(url_for('index'))
    
    # Get team users for assignee dropdown
    team_users = []
    supervisors = []
    
    if task.team_id:
        team_users = data_manager.get_team_users(str(task.team_id))
        # Get potential supervisors (managers and directors from the team)
        supervisors = [u for u in team_users if u.role in ['manager', 'director']]
    
    return render_template('task_detail.html', 
                         task=task, 
                         current_user=current_user,
                         team_users=team_users,
                         supervisors=supervisors)

@app.route('/task/<int:task_id>/comment', methods=['POST'])
def add_task_comment(task_id):
    """Add a comment to a task"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    task = data_manager.get_task(str(task_id))
    if not task:
        flash('Task not found', 'error')
        return redirect(url_for('index'))
    
    content = request.form.get('content', '').strip()
    if not content:
        flash('Comment cannot be empty', 'error')
        return redirect(url_for('task_detail', task_id=task_id))
    
    # Add comment via data manager
    comment = data_manager.add_task_comment(str(task_id), str(current_user.id), content)
    
    if comment:
        flash('Comment added successfully', 'success')
    else:
        flash('Failed to add comment', 'error')
    
    return redirect(url_for('task_detail', task_id=task_id))

@app.route('/task/<int:task_id>/update', methods=['POST'])
def update_task_detail(task_id):
    """Update task details from the detail page"""
    current_user = data_manager.get_current_user()
    if not current_user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Unauthorized'}), 401
        return redirect(url_for('login'))
    
    task = data_manager.get_task(str(task_id))
    if not task:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Task not found'}), 404
        flash('Task not found', 'error')
        return redirect(url_for('index'))
    
    # Check permissions
    can_edit = (current_user.is_administrator or 
                task.assignee_id == current_user.id or 
                task.created_by == current_user.id or
                (current_user.role in ['manager', 'director'] and task.team_id == current_user.team_id))
    
    if not can_edit:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Permission denied'}), 403
        flash('You do not have permission to edit this task', 'error')
        return redirect(url_for('task_detail', task_id=task_id))
    
    # Get form data
    status = request.form.get('status')
    priority = request.form.get('priority')
    complexity = request.form.get('complexity')
    assignee_id = request.form.get('assignee_id')
    supervisor_id = request.form.get('supervisor_id')
    
    # Track changes for history
    changes = []
    
    # Update fields and track changes
    if status and status != task.status:
        changes.append(('status', task.status, status))
        task.status = status
        if status == 'completed':
            task.completed_at = datetime.utcnow()
        elif status == 'in_progress' and not task.started_at:
            task.started_at = datetime.utcnow()
    
    if priority and priority != task.priority:
        changes.append(('priority', task.priority, priority))
        task.priority = priority
    
    if complexity and complexity != task.complexity:
        changes.append(('complexity', task.complexity, complexity))
        task.complexity = complexity
    
    # Handle assignee change
    new_assignee_id = int(assignee_id) if assignee_id else None
    if new_assignee_id != task.assignee_id:
        old_assignee_user = User.query.get(task.assignee_id) if task.assignee_id else None
        old_assignee = old_assignee_user.display_name or old_assignee_user.username if old_assignee_user else 'Unassigned'
        new_assignee_user = data_manager.get_user(assignee_id) if assignee_id else None
        new_assignee = new_assignee_user.display_name or new_assignee_user.username if new_assignee_user else 'Unassigned'
        changes.append(('assignee', old_assignee, new_assignee))
        task.assignee_id = new_assignee_id
    
    # Handle supervisor change (only for managers/directors/admins)
    if current_user.role in ['manager', 'director'] or current_user.is_administrator:
        new_supervisor_id = int(supervisor_id) if supervisor_id else None
        if new_supervisor_id != task.supervisor_id:
            old_supervisor_user = User.query.get(task.supervisor_id) if task.supervisor_id else None
            old_supervisor = old_supervisor_user.display_name or old_supervisor_user.username if old_supervisor_user else 'No supervisor'
            new_supervisor_user = data_manager.get_user(supervisor_id) if supervisor_id else None
            new_supervisor = new_supervisor_user.display_name or new_supervisor_user.username if new_supervisor_user else 'No supervisor'
            changes.append(('supervisor', old_supervisor, new_supervisor))
            task.supervisor_id = new_supervisor_id
    
    try:
        # Update timestamp
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Add history entries for each change
        for field_name, old_value, new_value in changes:
            data_manager.add_task_history(
                str(task_id), 
                str(current_user.id), 
                'updated', 
                field_name=field_name,
                old_value=old_value, 
                new_value=new_value
            )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': True, 'message': 'Task updated successfully'})
        
        flash('Task updated successfully', 'success')
        return redirect(url_for('task_detail', task_id=task_id))
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating task: {e}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': 'Failed to update task'}), 500
        
        flash('Failed to update task', 'error')
        return redirect(url_for('task_detail', task_id=task_id))

@app.route('/user/<int:user_id>/update', methods=['POST'])
def update_user_inline(user_id):
    """Update user details via inline editing"""
    current_user = data_manager.get_current_user()
    if not current_user or not current_user.is_administrator:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = data_manager.get_user(str(user_id))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get the field being updated
    display_name = request.form.get('display_name')
    email = request.form.get('email')
    
    try:
        if display_name is not None:
            data_manager.update_user(str(user_id), display_name=display_name)
        elif email is not None:
            # Check if email is already taken by another user
            existing_user = data_manager.get_user_by_email(email)
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'Email already in use'}), 400
            data_manager.update_user(str(user_id), email=email)
        
        return jsonify({'success': True}), 200
    except Exception as e:
        logging.error(f"Error updating user {user_id}: {e}")
        return jsonify({'error': 'Update failed'}), 500

@app.route('/edit_team/<int:team_id>', methods=['POST'])
def edit_team_inline(team_id):
    """Update team details via inline editing"""
    current_user = data_manager.get_current_user()
    if not current_user or not current_user.is_administrator:
        return jsonify({'error': 'Unauthorized'}), 403
    
    team = data_manager.get_team(str(team_id))
    if not team:
        return jsonify({'error': 'Team not found'}), 404
    
    # Get the field being updated
    name = request.form.get('name')
    description = request.form.get('description')
    
    try:
        if name is not None:
            # Check if team name is already taken
            existing_teams = data_manager.get_all_teams()
            if any(t.name == name and t.id != team.id for t in existing_teams):
                return jsonify({'error': 'Team name already exists'}), 400
            
            team.name = name
        elif description is not None:
            team.description = description
        
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        logging.error(f"Error updating team {team_id}: {e}")
        db.session.rollback()
        return jsonify({'error': 'Update failed'}), 500

@app.route('/api/team-users')
def api_team_users():
    """API endpoint to get team users for autocomplete"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify([]), 401
    
    # Get users from the same team (or all users for administrators)
    if current_user.is_administrator:
        users = data_manager.get_all_users()
    else:
        users = data_manager.get_users_by_team(str(current_user.team_id)) if current_user.team_id else []
    
    # Format users for autocomplete
    users_data = []
    for user in users:
        if user.is_active:  # Only include active users
            users_data.append({
                'id': user.id,
                'username': user.username,
                'display_name': user.display_name,
                'role': user.role
            })
    
    return jsonify(users_data)

@app.context_processor
def inject_current_user():
    """Make current user available in all templates"""
    return dict(current_user=data_manager.get_current_user())



# If no current user, redirect to login
@app.before_request
def require_login():
    allowed_endpoints = ['login', 'static', 'time_report', 'download_file', 'upload_file', 'delete_file']
    if request.endpoint not in allowed_endpoints and not data_manager.get_current_user():
        return redirect(url_for('login'))

# File upload configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 
    'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z', 'csv'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_icon(file_type):
    """Get appropriate icon for file type"""
    if file_type:
        if file_type.startswith('image/'):
            return 'image'
        elif file_type.startswith('text/') or file_type == 'application/pdf':
            return 'file-text'
        elif 'word' in file_type or 'document' in file_type:
            return 'file'
        elif 'excel' in file_type or 'spreadsheet' in file_type:
            return 'file'
        elif 'powerpoint' in file_type or 'presentation' in file_type:
            return 'file'
        elif 'zip' in file_type or 'compressed' in file_type:
            return 'archive'
    return 'file'

@app.route('/upload_file/<task_id>', methods=['POST'])
def upload_file(task_id):
    """Upload file attachment to task"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Check if task exists and user has permission
    task = data_manager.get_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Check if user can access this task (team-based access)
    if not current_user.is_administrator and current_user.team_id != task.team_id:
        return jsonify({'error': 'Access denied'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Create uploads directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Generate secure filename
    original_filename = secure_filename(file.filename) if file.filename else "unknown"
    file_extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}" if file_extension else uuid.uuid4().hex
    
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    
    try:
        # Save file
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        # Check file size
        if file_size > MAX_FILE_SIZE:
            os.remove(file_path)
            return jsonify({'error': 'File too large (max 16MB)'}), 400
        
        # Create attachment record
        attachment = TaskAttachment(
            task_id=int(task_id),
            filename=unique_filename,
            original_filename=original_filename,
            file_size=file_size,
            file_type=file.content_type,
            uploaded_by=current_user.id
        )
        
        db.session.add(attachment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'attachment': attachment.to_dict(),
            'message': f'File "{original_filename}" uploaded successfully'
        })
        
    except Exception as e:
        # Clean up file if database insert fails
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/download_file/<attachment_id>')
def download_file(attachment_id):
    """Download file attachment"""
    current_user = data_manager.get_current_user()
    if not current_user:
        flash('Authentication required', 'error')
        return redirect(url_for('login'))
    
    attachment = TaskAttachment.query.get_or_404(attachment_id)
    task = attachment.task
    
    # Check if user can access this task (team-based access)
    if not current_user.is_administrator and current_user.team_id != task.team_id:
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    file_path = os.path.join(UPLOAD_FOLDER, attachment.filename)
    
    if not os.path.exists(file_path):
        flash('File not found', 'error')
        return redirect(url_for('index'))
    
    return send_file(file_path, as_attachment=True, download_name=attachment.original_filename)

@app.route('/delete_file/<attachment_id>', methods=['POST'])
def delete_file(attachment_id):
    """Delete file attachment"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify({'error': 'Authentication required'}), 401
    
    attachment = TaskAttachment.query.get_or_404(attachment_id)
    task = attachment.task
    
    # Check if user can delete this file (uploader or admin/manager)
    can_delete = (
        current_user.id == attachment.uploaded_by or
        current_user.is_administrator or
        current_user.role in ['manager', 'director']
    )
    
    if not can_delete:
        return jsonify({'error': 'Permission denied'}), 403
    
    try:
        # Remove file from filesystem
        file_path = os.path.join(UPLOAD_FOLDER, attachment.filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Remove database record
        db.session.delete(attachment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'File "{attachment.original_filename}" deleted successfully'
        })
        
    except Exception as e:
        return jsonify({'error': f'Delete failed: {str(e)}'}), 500

@app.route('/api/task/<task_id>/attachments')
def get_task_attachments(task_id):
    """Get task attachments"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return jsonify({'error': 'Authentication required'}), 401
    
    task = data_manager.get_task(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Check if user can access this task (team-based access)
    if not current_user.is_administrator and current_user.team_id != task.team_id:
        return jsonify({'error': 'Access denied'}), 403
    
    attachments = TaskAttachment.query.filter_by(task_id=task_id).all()
    
    return jsonify({
        'success': True,
        'attachments': [attachment.to_dict() for attachment in attachments]
    })


