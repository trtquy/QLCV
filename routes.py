from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app
from data_manager import data_manager
from datetime import datetime, timedelta
import logging

@app.route('/')
def index():
    """Main kanban board page"""
    current_user = data_manager.get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    tasks = data_manager.get_all_tasks()
    users = data_manager.get_all_users()
    teams = data_manager.get_all_teams()
    
    # Filter by team if specified
    team_filter = request.args.get('team')
    if team_filter:
        tasks = [t for t in tasks if str(t.team_id) == team_filter]
    
    # Organize tasks by status
    todo_tasks = [t for t in tasks if t.status == 'todo']
    in_progress_tasks = [t for t in tasks if t.status == 'in_progress']
    completed_tasks = [t for t in tasks if t.status == 'completed']
    
    return render_template('index.html', 
                         todo_tasks=todo_tasks,
                         in_progress_tasks=in_progress_tasks,
                         completed_tasks=completed_tasks,
                         users=users,
                         teams=teams,
                         current_user=current_user,
                         selected_team=team_filter)

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
    priority = request.form.get('priority', 'medium')
    complexity = request.form.get('complexity', 'medium')
    estimated_hours = request.form.get('estimated_hours')
    
    if title:
        task = data_manager.create_task(
            title=title,
            description=description,
            created_by=current_user.id,
            assignee_id=assignee_id,
            priority=priority,
            complexity=complexity
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
    complexity = request.form.get('complexity', 'medium')
    status = request.form.get('task_status', 'todo')
    team_id = request.form.get('team_id') or None
    estimated_hours = request.form.get('estimated_hours')
    
    if title:
        task = data_manager.update_task(
            task_id,
            title=title,
            description=description,
            assignee_id=assignee_id,
            priority=priority,
            complexity=complexity,
            status=status,
            team_id=team_id
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
    teams = data_manager.get_all_teams()
    
    return render_template('team.html',
                         current_user=current_user,
                         users=users,
                         tasks=tasks,
                         teams=teams)

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

@app.route('/move_member_to_team', methods=['POST'])
def move_member_to_team():
    """Move a team member to a different team (manager only)"""
    current_user = data_manager.get_current_user()
    if not current_user or current_user.role not in ['manager', 'admin']:
        flash('Only managers and admins can move team members', 'error')
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
    """Add a new team member (manager only)"""
    current_user = data_manager.get_current_user()
    if not current_user or current_user.role not in ['manager', 'admin']:
        flash('Only managers and admins can add team members', 'error')
        return redirect(url_for('team'))
    
    username = request.form.get('username')
    email = request.form.get('email')
    team_id = request.form.get('team_id')
    role = request.form.get('role', 'member')
    
    if username and email and team_id:
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
                # Assign to team
                data_manager.update_user(str(user.id), team_id=int(team_id))
                team = data_manager.get_team(team_id)
                flash(f'User {username} added to {team.name if team else "team"} successfully', 'success')
            else:
                flash('Failed to create user', 'error')
        except Exception as e:
            flash('Email or username already exists', 'error')
    else:
        flash('Please fill in all required fields', 'error')
    
    return redirect(url_for('team'))

@app.route('/create_team', methods=['POST'])
def create_team():
    """Create a new team (admin only)"""
    current_user = data_manager.get_current_user()
    if not current_user or current_user.role != 'admin':
        flash('Only admins can create teams', 'error')
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
    """Edit team details (admin only)"""
    current_user = data_manager.get_current_user()
    if not current_user or current_user.role != 'admin':
        flash('Only admins can edit teams', 'error')
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
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid start date format', 'error')
    
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            flash('Invalid end date format', 'error')
    
    report_data = data_manager.get_time_report_data(team_id, start_date, end_date)
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
        estimated_hours = float(estimated_hours)
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

# Template context processors
@app.context_processor
def inject_current_user():
    """Make current user available in all templates"""
    return dict(current_user=data_manager.get_current_user())



# If no current user, redirect to login
@app.before_request
def require_login():
    allowed_endpoints = ['login', 'static', 'time_report']
    if request.endpoint not in allowed_endpoints and not data_manager.get_current_user():
        return redirect(url_for('login'))
