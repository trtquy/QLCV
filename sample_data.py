"""
Sample data for TaskFlow - Banking and Financial Risk Management
"""
from app import app, db
from models import User, Task, Team
from data_manager import data_manager

def create_sample_data():
    """Create sample users and tasks for banking/financial risk management"""
    
    with app.app_context():
        # Clear existing data if any
        db.session.query(Task).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Load real user data from Excel file
        import pandas as pd
        df = pd.read_excel('attached_assets/Book2_1749633149254.xlsx')
        
        # Create admin user first
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@bidv.com.vn',
                'role': 'admin'
            }
        ]
        
        # Add real users from Excel
        for _, row in df.iterrows():
            users_data.append({
                'username': str(row['Username']),
                'email': str(row['Email']), 
                'role': str(row['Class']).lower(),
                'team_name': str(row['Team.1'])  # Using Team.1 column which has the actual team names
            })
        
        # Create teams based on real data from Excel
        unique_teams = df['Team.1'].unique()
        teams_data = []
        team_descriptions = {
            'Chính sách tín dụng': 'Credit policy development and implementation',
            'Quản lý danh mục': 'Portfolio management and analysis',
            'Giám sát tín dụng': 'Credit monitoring and supervision',
            'Quản lý rủi ro tích hợp': 'Integrated risk management'
        }
        
        for team_name in unique_teams:
            teams_data.append({
                'name': team_name,
                'description': team_descriptions.get(team_name, 'Banking operations team')
            })
        
        created_teams = []
        for team_data in teams_data:
            team = Team(**team_data)
            db.session.add(team)
            created_teams.append(team)
        
        db.session.commit()
        
        # Create users and assign to teams
        created_users = []
        for i, user_data in enumerate(users_data):
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                role=user_data['role']
            )
            # Set password to '123' for all users
            user.set_password('123')
            
            # Admin and Directors don't need team assignments
            if user_data['role'] in ['admin', 'director']:
                user.team_id = None
            # Assign sarah_chen (manager) to Risk Assessment Team
            elif user_data['username'] == 'sarah_chen':
                user.team_id = created_teams[0].id
            # Assign analysts to teams
            elif user_data['role'] == 'analyst':
                if i <= 3:  # mike_rodriguez, emily_watson to Risk Assessment
                    user.team_id = created_teams[0].id
                else:  # jennifer_lopez to other teams
                    user.team_id = created_teams[1].id
                
            db.session.add(user)
            created_users.append(user)
        
        db.session.commit()
        
        # Create sample tasks
        tasks_data = [
            {
                'title': 'Credit Risk Assessment - Q4 Portfolio Review',
                'description': 'Conduct comprehensive credit risk analysis for Q4 commercial lending portfolio. Review default probabilities and update risk ratings for major accounts.',
                'status': 'in_progress',
                'priority': 'high',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[1].id  # mike_rodriguez
            },
            {
                'title': 'Regulatory Compliance - Basel III Implementation',
                'description': 'Update capital adequacy calculations according to Basel III requirements. Ensure all documentation is ready for regulatory submission.',
                'status': 'todo',
                'priority': 'urgent',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[2].id  # emily_watson
            },
            {
                'title': 'Market Risk Dashboard - Real-time Monitoring',
                'description': 'Develop automated dashboard for real-time market risk monitoring. Include VaR calculations and stress testing scenarios.',
                'status': 'in_progress',
                'priority': 'medium',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[3].id  # david_kim
            },
            {
                'title': 'Operational Risk - Cyber Security Assessment',
                'description': 'Complete annual cybersecurity risk assessment. Identify vulnerabilities and recommend mitigation strategies.',
                'status': 'completed',
                'priority': 'high',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[4].id  # jennifer_lopez
            },
            {
                'title': 'Liquidity Risk Analysis - Stress Testing',
                'description': 'Perform liquidity stress testing scenarios under adverse market conditions. Update contingency funding plans.',
                'status': 'todo',
                'priority': 'medium',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[1].id  # mike_rodriguez
            },
            {
                'title': 'Anti-Money Laundering (AML) Review',
                'description': 'Review suspicious transaction reports and update AML monitoring procedures. Ensure compliance with regulatory requirements.',
                'status': 'in_progress',
                'priority': 'urgent',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[2].id  # emily_watson
            },
            {
                'title': 'Interest Rate Risk Modeling',
                'description': 'Update interest rate risk models for asset-liability management. Include sensitivity analysis for rate changes.',
                'status': 'completed',
                'priority': 'medium',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[3].id  # david_kim
            },
            {
                'title': 'Fraud Detection System Enhancement',
                'description': 'Enhance machine learning algorithms for fraud detection. Reduce false positives while maintaining detection accuracy.',
                'status': 'todo',
                'priority': 'high',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[4].id  # jennifer_lopez
            },
            {
                'title': 'ESG Risk Framework Development',
                'description': 'Develop comprehensive Environmental, Social, and Governance (ESG) risk assessment framework for investment decisions.',
                'status': 'in_progress',
                'priority': 'medium',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[1].id  # mike_rodriguez
            },
            {
                'title': 'Counterparty Risk - Credit Exposure Analysis',
                'description': 'Analyze counterparty credit exposure across derivatives portfolio. Update credit limits and collateral requirements.',
                'status': 'completed',
                'priority': 'high',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[2].id  # emily_watson
            },
            {
                'title': 'Risk Appetite Statement Update',
                'description': 'Annual review and update of enterprise risk appetite statement. Align with business strategy and regulatory expectations.',
                'status': 'todo',
                'priority': 'low',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[3].id  # david_kim
            },
            {
                'title': 'Concentration Risk Assessment',
                'description': 'Assess concentration risk across geographic regions, industries, and individual borrowers. Recommend diversification strategies.',
                'status': 'in_progress',
                'priority': 'medium',
                'created_by': created_users[0].id,  # sarah_chen
                'assignee_id': created_users[4].id  # jennifer_lopez
            }
        ]
        
        # Create tasks and assign to teams
        for task_data in tasks_data:
            task = Task(**task_data)
            # Assign tasks to the Risk Assessment Team (sarah_chen's team)
            task.team_id = created_teams[0].id
            db.session.add(task)
        
        db.session.commit()
        
        print("Sample data created successfully!")
        print(f"Created {len(created_teams)} teams, {len(created_users)} users and {len(tasks_data)} tasks")
        print("Manager sarah_chen assigned to Risk Assessment Team with team members")

if __name__ == '__main__':
    create_sample_data()