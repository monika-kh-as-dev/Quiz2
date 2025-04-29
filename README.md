# Employee Analytics

## Setup
```bash
git clone <your-repo-url>
cd employee_data_analytics
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

pip install psycopg2-binary 

python manage.py migrate

### command to run generate fake data and create super user 
python manage.py employee_data

python manage.py runserver
```

## API
- Visit `/swagger/` for interactive API documentation
- Visit `/admin/` for Super Admin
- Visit `/dashboard/` for Employee Data visualizations ( No Auth required )
- Auth required (basic/session)


## Models
- Employee
- Attendance
- Performance

## Features
- RESTful CRUD
- Sample data generation
- Employee data visualizations
- Swagger UI
- DRF Throttling
- Pagination support
