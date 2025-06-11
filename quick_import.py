#!/usr/bin/env python3
"""
Quick import of Excel tasks with proper error handling
"""

import pandas as pd
from app import app, db
from models import User, Task, Team
from data_manager import DataManager
import random

def quick_import():
    with app.app_context():
        dm = DataManager()
        
        # Read Excel file
        df = pd.read_excel('attached_assets/Book4_1749639551792.xlsx')
        print(f"Importing {len(df)} tasks...")
        
        # Create teams from unique team names
        unique_teams = df['Team'].dropna().unique()
        team_map = {}
        
        for team_name in unique_teams:
            # Check if team already exists
            existing_teams = dm.get_all_teams()
            existing_team = None
            for t in existing_teams:
                if t.name == str(team_name):
                    existing_team = t
                    break
            
            if existing_team:
                team_map[team_name] = existing_team.id
            else:
                team = Team(name=str(team_name), description=f"Banking team: {team_name}")
                db.session.add(team)
                db.session.flush()
                team_map[team_name] = team.id
        
        # Create users from unique assignees
        unique_assignees = df['Assignee'].dropna().unique()
        user_map = {}
        
        for assignee in unique_assignees:
            # Check if user already exists
            existing_user = dm.get_user_by_username(str(assignee))
            if existing_user:
                user_map[assignee] = existing_user.id
            else:
                user = dm.create_user(
                    username=str(assignee),
                    email=f"{assignee}@bidv.com.vn",
                    role='analyst'
                )
                user_map[assignee] = user.id
        
        db.session.commit()
        
        # Complexity mapping
        complexity_map = {
            'Very Simple': 'very_simple',
            'Simple': 'simple',
            'Medium': 'medium', 
            'Complex': 'complex',
            'Very Complex': 'very_complex'
        }
        
        # Priority mapping
        priority_map = {
            'Low': 'low',
            'Medium': 'medium',
            'High': 'high', 
            'Urgent': 'urgent'
        }
        
        # Get admin user for creator
        admin_user = dm.get_user_by_username('quytt2')
        creator_id = admin_user.id if admin_user else 1
        
        # Status distribution
        statuses = ['todo', 'in_progress', 'completed']
        
        imported = 0
        
        for idx, row in df.iterrows():
            try:
                # Get values safely
                title = str(row['Summary'])[:200] if pd.notna(row['Summary']) else f"Task {idx+1}"
                description = str(row['Description']) if pd.notna(row['Description']) else ""
                
                complexity = complexity_map.get(str(row['Complexity']), 'medium')
                priority = priority_map.get(str(row['Priority']), 'medium')
                
                # Assign team and user
                team_id = None
                if pd.notna(row['Team']) and row['Team'] in team_map:
                    team_id = team_map[row['Team']]
                
                assignee_id = None
                if pd.notna(row['Assignee']) and row['Assignee'] in user_map:
                    assignee_id = user_map[row['Assignee']]
                
                # Random status (40% todo, 35% in_progress, 25% completed)
                status = random.choices(statuses, weights=[0.4, 0.35, 0.25])[0]
                
                # Create task
                task = dm.create_task(
                    title=title,
                    description=description,
                    created_by=str(creator_id),
                    assignee_id=str(assignee_id) if assignee_id else None,
                    priority=priority,
                    complexity=complexity
                )
                
                # Update additional fields
                task.status = status
                if team_id:
                    task.team_id = team_id
                
                # Set estimated hours based on complexity
                hours_map = {
                    'very_simple': random.uniform(1, 3),
                    'simple': random.uniform(2, 6),
                    'medium': random.uniform(4, 12),
                    'complex': random.uniform(8, 24),
                    'very_complex': random.uniform(16, 40)
                }
                task.estimated_hours = hours_map.get(complexity, 8)
                
                imported += 1
                
                if imported % 20 == 0:
                    print(f"Imported {imported} tasks...")
                    db.session.commit()
                
            except Exception as e:
                print(f"Error importing row {idx}: {e}")
                continue
        
        db.session.commit()
        print(f"\nCompleted! Imported {imported} tasks with {len(team_map)} teams and {len(user_map)} users")

if __name__ == "__main__":
    quick_import()