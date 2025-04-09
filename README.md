# Inventory Management System

A simple and efficient inventory management system built with Django.

## Features
- User authentication and authorization
- Product management (CRUD operations)
- Stock tracking and management
- Low stock alerts
- REST API endpoints
- Basic reporting

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

Admin creds:  darshan.p Inventory@123$
