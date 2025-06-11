#!/usr/bin/env python3
import pandas as pd
import random

# Read Excel data
df = pd.read_excel('attached_assets/Book4_1749639551792.xlsx')

# Complexity and priority mappings
complexity_map = {
    'Very Simple': 'very_simple',
    'Simple': 'simple', 
    'Medium': 'medium',
    'Complex': 'complex',
    'Very Complex': 'very_complex'
}

priority_map = {
    'Low': 'low',
    'Medium': 'medium',
    'High': 'high',
    'Urgent': 'urgent'
}

# Generate SQL for teams
print("-- Creating teams")
teams = df['Team'].dropna().unique()
for i, team in enumerate(teams, 1):
    safe_name = str(team).replace("'", "''")
    print(f"INSERT INTO teams (name, description, is_active, created_at) VALUES ('{safe_name}', 'Banking team: {safe_name}', true, NOW()) ON CONFLICT (name) DO NOTHING;")

print("\n-- Creating users")
users = df['Assignee'].dropna().unique()
for user in users:
    safe_user = str(user).replace("'", "''")
    print(f"INSERT INTO users (username, email, password_hash, role, is_administrator, is_active, created_at) VALUES ('{safe_user}', '{safe_user}@bidv.com.vn', 'pbkdf2:sha256:600000$salt$hash', 'analyst', false, true, NOW()) ON CONFLICT (username) DO NOTHING;")

print("\n-- Creating tasks")
statuses = ['todo', 'in_progress', 'completed']

for idx, row in df.iterrows():
    # Safe string handling
    title = str(row['Summary']).replace("'", "''")[:200] if pd.notna(row['Summary']) else f"Task {idx+1}"
    description = str(row['Description']).replace("'", "''") if pd.notna(row['Description']) else ""
    
    complexity = complexity_map.get(str(row['Complexity']), 'medium')
    priority = priority_map.get(str(row['Priority']), 'medium')
    status = random.choices(statuses, weights=[0.4, 0.35, 0.25])[0]
    
    # Team assignment
    team_clause = "NULL"
    if pd.notna(row['Team']):
        team_name = str(row['Team']).replace("'", "''")
        team_clause = f"(SELECT id FROM teams WHERE name = '{team_name}')"
    
    # User assignment  
    assignee_clause = "NULL"
    if pd.notna(row['Assignee']):
        assignee_name = str(row['Assignee']).replace("'", "''") 
        assignee_clause = f"(SELECT id FROM users WHERE username = '{assignee_name}')"
    
    hours = round(random.uniform(2, 20), 1)
    
    sql = f"""INSERT INTO tasks (title, description, status, priority, complexity, created_at, updated_at, estimated_hours, actual_hours, created_by, assignee_id, team_id) 
VALUES ('{title}', '{description}', '{status}', '{priority}', '{complexity}', NOW(), NOW(), {hours}, 0.0, 
(SELECT id FROM users WHERE is_administrator = true LIMIT 1), {assignee_clause}, {team_clause});"""
    
    print(sql)

print(f"\n-- Successfully generated SQL for {len(df)} tasks")