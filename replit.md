# TaskFlow - Team Task Management System

## Overview
TaskFlow is a comprehensive team task management system built with Flask, designed specifically for banking and financial risk management teams. The application features a Kanban-style board interface with role-based access control, time tracking, and team collaboration tools.

## System Architecture

### Frontend Architecture
- **Templates**: Jinja2 templating with Bootstrap 5 for responsive UI
- **Static Assets**: CSS (custom styles + Bootstrap), JavaScript (vanilla JS with Chart.js)
- **UI Components**: 
  - Kanban board with drag-and-drop functionality
  - Dashboard with charts and metrics
  - Team management interface
  - Time tracking system
  - Role-based access controls

### Backend Architecture
- **Framework**: Flask web framework with SQLAlchemy ORM
- **Database**: SQLite for development (with PostgreSQL support via DATABASE_URL)
- **Authentication**: Session-based authentication with password hashing
- **Authorization**: Role-based access control (analyst, manager, director, administrator)
- **Data Management**: Centralized DataManager class for business logic

### Database Schema
- **Users**: Authentication, roles, team assignments
- **Tasks**: Task management with status tracking, priorities, complexity levels
- **Teams**: Team organization and membership
- **TimeLog**: Time tracking for tasks (referenced but not fully implemented)

## Key Components

### Models (models.py)
- **User Model**: Handles authentication, roles, and team relationships
- **Task Model**: Task management with status, priority, complexity tracking
- **Team Model**: Team organization and management

### Data Management (data_manager.py)
- Centralized business logic layer
- User authentication and management
- Task operations and queries
- Team management functions

### Routes (routes.py)
- Main kanban board view with team-based filtering
- Authentication endpoints
- Role-based access control implementation
- Task management endpoints

### Sample Data Management
- Excel import functionality for bulk task creation
- Banking-specific sample data generation
- User and team creation from Excel files

## Data Flow

### Authentication Flow
1. User logs in via login form
2. Credentials validated against database
3. Session established with user ID
4. Role-based permissions applied

### Task Management Flow
1. Tasks displayed on Kanban board filtered by team/role
2. Drag-and-drop status updates
3. Priority and complexity management
4. Time tracking integration
5. Role-based editing permissions

### Team Access Control
- Administrators: Full access to all tasks and teams
- Regular users: Access limited to their team's tasks
- Managers/Directors: Enhanced permissions within their team

## External Dependencies

### Frontend Libraries
- **Bootstrap 5**: UI framework and responsive design
- **Feather Icons**: Icon library for consistent iconography
- **Chart.js**: Dashboard analytics and visualization
- **Google Fonts**: Inter font family for typography

### Backend Libraries
- **Flask**: Web framework
- **SQLAlchemy**: ORM and database abstraction
- **Werkzeug**: Security utilities (password hashing, proxy handling)
- **Pandas**: Excel file processing and data import

## Deployment Strategy

### Development Environment
- SQLite database for local development
- Flask development server
- Debug mode enabled
- Session secret key from environment variable

### Production Considerations
- PostgreSQL database via DATABASE_URL environment variable
- ProxyFix middleware for reverse proxy deployment
- Connection pooling and engine optimization
- Secure session management

## Changelog
- July 07, 2025. Initial setup
- July 07, 2025. Fixed dashboard status badges to display with status-appropriate colors:
  - To Do tasks: Grey badges (bg-secondary)
  - In Progress tasks: Yellow badges (bg-warning)
  - In Review tasks: Blue badges (bg-info)
  - Completed tasks: Green badges (bg-success)
  - Updated backend to provide detailed status counts per user
  - Improved template rendering to show only non-zero status counts

## User Preferences
Preferred communication style: Simple, everyday language.