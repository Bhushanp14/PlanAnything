# PlanAnything - Visual Daily Planner

## Overview
PlanAnything is a Django-based visual daily planner web application that helps users organize tasks across multiple plans with interactive calendar views. Users can create separate plans (e.g., Work, Fitness, Study) and manage daily tasks with visual status tracking.

## Project Architecture

### Technology Stack
- **Backend**: Django 5.2.7 (Python 3.11)
- **Frontend**: HTML, JavaScript, TailwindCSS (via CDN)
- **Database**: SQLite
- **Dependencies**: Pillow (image handling), python-dateutil (date calculations)

### Project Structure
```
plananything/
├── plananything/          # Main project settings
│   ├── settings.py       # Django configuration
│   ├── urls.py           # Root URL routing
│   └── wsgi.py
├── planner/              # Main application
│   ├── models.py         # Plan and Task models
│   ├── views.py          # View logic
│   ├── forms.py          # Django forms
│   ├── urls.py           # App URL routing
│   ├── admin.py          # Admin configuration
│   ├── templates/        # HTML templates
│   │   └── planner/
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── dashboard.html
│   │       ├── plan_detail.html
│   │       ├── plan_form.html
│   │       ├── task_form.html
│   │       └── ...
│   └── templatetags/     # Custom template filters
├── static/               # Static files (CSS, JS)
├── media/                # User uploaded files
└── manage.py
```

### Database Models
1. **Plan**
   - User (ForeignKey to Django User)
   - Title, Description
   - Color (for visual identification)
   - Start Date, End Date (optional)
   - Timestamps

2. **Task**
   - Plan (ForeignKey to Plan)
   - Title, Description
   - Photo (optional ImageField)
   - Status (Pending/Completed)
   - Task Date
   - Timestamps

## Features Implemented

### Authentication
- User registration with Django's built-in auth
- Login/Logout functionality
- Protected routes requiring authentication

### Dashboard
- Landing page for new users with call-to-action
- Plan cards showing:
  - Plan title and description
  - Color tag indicator
  - Task completion statistics (X/Y Completed with percentage)
  - Visual progress bar

### Plan Management
- Create new plans with title, description, color, start/end dates
- Edit existing plans
- Delete plans (with confirmation)
- Each plan has its own calendar view

### Calendar View
- Interactive monthly calendar display
- Color-coded task visualization:
  - Green: Completed tasks
  - Red: Overdue tasks
  - Blue: Pending tasks
- Quick task creation by clicking on dates
- Navigation between months
- Today's date highlighted

### Task Management
- Create tasks with title, description, photo, status, and date
- Edit existing tasks
- Delete tasks (with confirmation)
- Photo upload support
- Visual status indicators on calendar

### UI/UX
- Clean, modern design with TailwindCSS
- Responsive layout
- Inter font family
- Consistent color scheme
- User-friendly navigation
- Form validation and error display
- Success/error messages

## Development Setup

### Running the Application
The server is configured to run on port 5000:
```bash
python manage.py runserver 0.0.0.0:5000
```

### Test Credentials
- Username: testuser
- Password: testpass123

### Creating Admin User
```bash
python manage.py createsuperuser
```

### Making Database Changes
```bash
python manage.py makemigrations
python manage.py migrate
```

## Security & Production Configuration

### Environment Variables
The application uses environment variables for security-sensitive settings:
- `SESSION_SECRET`: Django secret key (uses SESSION_SECRET from Replit secrets, falls back to development key only for local dev)
- `DEBUG`: Debug mode (default: True for development, set to 'False' string for production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts (REQUIRED when DEBUG=False)

**Production Security**: 
- The app will refuse to start if DEBUG is False and SESSION_SECRET is not set or is using the development default
- The app will refuse to start if DEBUG is False and ALLOWED_HOSTS is not set
- Warning displayed if DEBUG is True in a deployed environment
- These startup checks prevent accidental insecure deployments

### File Upload Security
- Image uploads limited to 5MB maximum file size
- File type validation (images only)
- Secure file storage in media directory

### Deployment
The application is configured for deployment with:
- Gunicorn WSGI server for production
- Autoscale deployment target
- Environment-based configuration management

## Recent Changes
- Initial project setup (October 9, 2025)
- Implemented complete CRUD operations for Plans and Tasks
- Created interactive calendar view with color-coded task status
- Added user authentication system
- Implemented responsive UI with TailwindCSS
- Added photo upload functionality for tasks with 5MB file size validation
- Created landing page for new users
- Fixed security issues (externalized SECRET_KEY, DEBUG, ALLOWED_HOSTS)
- Fixed calendar navigation query parameters
- Added deployment configuration with Gunicorn

## User Workflow
1. Register/Login to account
2. Create first plan from landing page
3. View plan calendar
4. Click on any date to add tasks
5. Tasks appear color-coded on calendar
6. Click tasks to edit/delete
7. Track progress on dashboard

## Future Enhancements
- Weekly calendar view option
- Task filtering and search
- Task categories/tags within plans
- Reminder notifications
- Data export (PDF/CSV)
- Dark mode
- Mobile app
- Recurring tasks
- Task priorities
