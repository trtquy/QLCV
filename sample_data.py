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
        
        # Create sample users
        users_data = [
            {
                'username': 'sarah_chen',
                'email': 'sarah.chen@globalbank.com',
                'role': 'manager'
            },
            {
                'username': 'mike_rodriguez',
                'email': 'mike.rodriguez@globalbank.com',
                'role': 'member'
            },
            {
                'username': 'emily_watson',
                'email': 'emily.watson@globalbank.com',
                'role': 'member'
            },
            {
                'username': 'david_kim',
                'email': 'david.kim@globalbank.com',
                'role': 'member'
            },
            {
                'username': 'jennifer_lopez',
                'email': 'jennifer.lopez@globalbank.com',
                'role': 'member'
            }
        ]
        
        # Create users
        created_users = []
        for user_data in users_data:
            user = User(**user_data)
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
        
        # Create tasks
        for task_data in tasks_data:
            task = Task(**task_data)
            db.session.add(task)
        
        db.session.commit()
        
        print("Sample data created successfully!")
        print(f"Created {len(created_users)} users and {len(tasks_data)} tasks")

if __name__ == '__main__':
    create_sample_data()