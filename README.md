# PharmaGuard

Django + MySQL pharmacy management system with role-based admin/staff access.

## Features

- Home, login and staff signup
- Django authentication and sessions
- Admin/staff role separation
- Medicine CRUD (admin)
- Manufacturer management (admin)
- Batch/expiry tracking
- Purchases with automatic stock increase
- Sales with automatic stock decrease
- Prevents sales above available stock
- Prevents sales of expired medicines
- Low-stock, near-expiry and expired alerts
- Dashboard statistics and recent activity
- Django admin integration
- Responsive Bootstrap UI

## Run locally

Activate your virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies if needed:

```powershell
python -m pip install django mysqlclient
```

Make sure MySQL has the `pharmaguard_db` database and that `config/settings.py` contains your local MySQL credentials.

Then:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py check
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Important

Public signup creates **staff accounts only**. Create the admin/superuser using:

```powershell
python manage.py createsuperuser
```

The custom admin dashboard is `/admin-dashboard/` and Django's built-in administration is `/django-admin/`.
