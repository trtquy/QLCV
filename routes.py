from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app
from data_manager import data_manager
from datetime import datetime
import logging

@app.route('/')
def index():
    """Main kanban board page"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    tasks = data_manager.get_all_tasks()
    users = data_manager.get_all_users()
    
    # Organize tasks by status
    todo_tasks = [t for t in tasks if t.status == 'todo']
    in_progress_tasks = [t for t in tasks if t.status == 'in_progress']
    completed_tasks = [t for t in tasks if t.status == 'completed']
    
    # Convert to dictionaries for JSON serialization
    tasks_dict = [t.to_dict() for t in tasks]
    users_dict = [u.to_dict() for u in users]
    
    return render_template('index.html', 
                         todo_tasks=todo_tasks,
                         in_progress_tasks=in_progress_tasks,
                         completed_tasks=completed_tasks,
                         users=users,
                         current_user=current_user,
                         tasks_dict=tasks_dict,
                         users_dict=users_dict)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            user = data_manager.get_user_by_username(username)
            if not user:
                # Create new user if doesn't exist
                email = request.form.get('email', f"{username}@company.com")
                role = request.form.get('role', 'member')
                user = data_manager.create_user(username, email, role)
                flash(f'Welcome {username}! New account created.', 'success')
            else:
                flash(f'Welcome back, {username}!', 'success')
            
            data_manager.set_current_user(user.id)
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            flash('Please enter a username', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout current user"""
    data_manager.logout_current_user()
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/create_task', methods=['POST'])
def create_task():
    """Create a new task"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    title = request.form.get('title')
    description = request.form.get('description', '')
    assignee_id = request.form.get('assignee_id') or None
    priority = request.form.get('priority', 'medium')
    
    if title:
        task = data_manager.create_task(
            title=title,
            description=description,
            created_by=current_user.id,
            assignee_id=assignee_id,
            priority=priority
        )
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
    
    # Handle status update (for drag and drop)
    if 'status' in request.form:
        new_status = request.form.get('status')
        task = data_manager.update_task(task_id, status=new_status)
        if task:
            return jsonify({'success': True, 'task_id': task_id, 'new_status': new_status})
        else:
            return jsonify({'success': False, 'error': 'Task not found'})
    
    # Handle full task update
    title = request.form.get('title')
    description = request.form.get('description', '')
    assignee_id = request.form.get('assignee_id') or None
    priority = request.form.get('priority', 'medium')
    status = request.form.get('task_status', 'todo')
    
    if title:
        task = data_manager.update_task(
            task_id,
            title=title,
            description=description,
            assignee_id=assignee_id,
            priority=priority,
            status=status
        )
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
    
    tasks = data_manager.get_all_tasks()
    users = data_manager.get_all_users()
    
    # Calculate metrics
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.status == 'completed'])
    in_progress_tasks = len([t for t in tasks if t.status == 'in_progress'])
    todo_tasks = len([t for t in tasks if t.status == 'todo'])
    
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # User performance
    user_stats = {}
    for user in users:
        user_tasks = [t for t in tasks if t.assignee_id == user.id]
        user_completed = len([t for t in user_tasks if t.status == 'completed'])
        user_total = len(user_tasks)
        user_stats[str(user.id)] = {
            'user': user.to_dict(),
            'total_tasks': user_total,
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
    
    return render_template('team.html',
                         current_user=current_user,
                         users=users,
                         tasks=tasks)

@app.route('/update_user_role/<user_id>', methods=['POST'])
def update_user_role(user_id):
    """Update user role (manager only)"""
    current_user = data_manager.get_current_user()
    if not current_user or current_user.role != 'manager':
        flash('Access denied. Manager role required.', 'error')
        return redirect(url_for('team'))
    
    new_role = request.form.get('role')
    if new_role in ['member', 'manager']:
        user = data_manager.update_user(user_id, role=new_role)
        if user:
            flash(f'User role updated successfully!', 'success')
        else:
            flash('User not found', 'error')
    else:
        flash('Invalid role', 'error')
    
    return redirect(url_for('team'))

# Template context processors
@app.context_processor
def inject_current_user():
    """Make current user available in all templates"""
    return dict(current_user=data_manager.get_current_user())



# If no current user, redirect to login
@app.before_request
def require_login():
    allowed_endpoints = ['login', 'static']
    if request.endpoint not in allowed_endpoints and not data_manager.get_current_user():
        return redirect(url_for('login'))
