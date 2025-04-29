# Employee Analytics

## Setup
```bash
git clone <your-repo-url>
cd employee_analytics
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

## API
- Visit `/swagger/` for interactive API documentation
- Auth required (basic/session)

## Models
- Employee
- Attendance
- Performance

## Features
- RESTful CRUD
- Sample data generation
- Swagger UI
- DRF Throttling
- Pagination support
