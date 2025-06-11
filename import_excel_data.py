#!/usr/bin/env python3
"""
Import tasks from Excel file into the task management system
"""

import pandas as pd
from app import app, db
from models import User, Task, Team
from data_manager import DataManager
import random

def import_excel_tasks():
    """Import tasks from the Excel file"""
    
    with app.app_context():
        dm = DataManager()
        
        # Read the Excel file
        df = pd.read_excel('attached_assets/Book4_1749639551792.xlsx')
        
        print(f"Found {len(df)} tasks in Excel file")
        
        # Create teams mapping
        team_mapping = {}
        unique_teams = df['Team'].unique()
        
        for team_name in unique_teams:
            if pd.notna(team_name):
                # Check if team exists
                existing_teams = dm.get_all_teams()
                team = None
                for t in existing_teams:
                    if t.name == team_name:
                        team = t
                        break
                
                if not team:
                    # Create new team
                    team = Team(name=team_name, description=f"Team for {team_name}")
                    db.session.add(team)
                    db.session.commit()
                    print(f"Created team: {team_name}")
                
                team_mapping[team_name] = team.id
        
        # Create users mapping
        user_mapping = {}
        unique_assignees = df['Assignee'].unique()
        
        for assignee in unique_assignees:
            if pd.notna(assignee):
                # Check if user exists
                existing_user = dm.get_user_by_username(assignee)
                
                if not existing_user:
                    # Create new user
                    user = dm.create_user(
                        username=assignee,
                        email=f"{assignee}@bidv.com.vn",
                        role='analyst'
                    )
                    print(f"Created user: {assignee}")
                    user_mapping[assignee] = user.id
                else:
                    user_mapping[assignee] = existing_user.id
        
        # Map complexity and priority values
        complexity_mapping = {
            'Very Simple': 'very_simple',
            'Simple': 'simple', 
            'Medium': 'medium',
            'Complex': 'complex',
            'Very Complex': 'very_complex'
        }
        
        priority_mapping = {
            'Low': 'low',
            'Medium': 'medium',
            'High': 'high',
            'Urgent': 'urgent'
        }
        
        status_options = ['todo', 'in_progress', 'completed']
        
        # Import tasks
        imported_count = 0
        
        for index, row in df.iterrows():
            try:
                # Get team ID
                team_id = None
                if pd.notna(row['Team']) and row['Team'] in team_mapping:
                    team_id = team_mapping[row['Team']]
                
                # Get assignee ID
                assignee_id = None
                if pd.notna(row['Assignee']) and row['Assignee'] in user_mapping:
                    assignee_id = user_mapping[row['Assignee']]
                
                # Map complexity and priority
                complexity = complexity_mapping.get(row['Complexity'], 'medium')
                priority = priority_mapping.get(row['Priority'], 'medium')
                
                # Even distribution across statuses (40% todo, 35% in_progress, 25% completed)
                status_weights = [0.40, 0.35, 0.25]
                status = random.choices(status_options, weights=status_weights)[0]
                
                # Get creator (use first admin user)
                admin_users = [u for u in dm.get_all_users() if u.is_administrator]
                creator_id = admin_users[0].id if admin_users else 1
                
                # Create task
                task = dm.create_task(
                    title=row['Summary'][:200],  # Limit title length
                    description=row['Description'] if pd.notna(row['Description']) else '',
                    created_by=str(creator_id),
                    assignee_id=str(assignee_id) if assignee_id else None,
                    priority=priority,
                    complexity=complexity
                )
                
                # Update team assignment and status
                if team_id:
                    task.team_id = team_id
                task.status = status
                
                # Add estimated hours based on complexity
                complexity_hours = {
                    'very_simple': random.uniform(1, 3),
                    'simple': random.uniform(2, 6),
                    'medium': random.uniform(4, 12),
                    'complex': random.uniform(8, 24),
                    'very_complex': random.uniform(16, 40)
                }
                task.estimated_hours = complexity_hours.get(complexity, 8)
                
                db.session.commit()
                imported_count += 1
                
                if imported_count % 10 == 0:
                    print(f"Imported {imported_count} tasks...")
                    
            except Exception as e:
                print(f"Error importing task {index + 1}: {e}")
                db.session.rollback()
                continue
        
        print(f"\nSuccessfully imported {imported_count} tasks")
        print(f"Created {len(team_mapping)} teams")
        print(f"Created {len([u for u in user_mapping.keys() if pd.notna(u)])} users")

if __name__ == "__main__":
    import_excel_tasks()