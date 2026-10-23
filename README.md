# InternTrack

A full-stack Django app for tracking internship and job applications.
Users sign up, log in, and manage their own applications (company, role, status, date, link, notes).
Every user sees only their own data, in both the web UI and the REST API.

## Features
- Django class-based views: list with search, status filter, pagination and status counts; create, edit, delete
- Authentication: sign up, log in, log out (Django auth)
- Ownership-based authorization: all queries are scoped to `request.user`
- REST API with Django REST Framework (`/api/applications/`) using a ModelViewSet and router
- Bootstrap 5 responsive templates
- PostgreSQL or SQLite (switch with environment variables)
- Automated tests (`python manage.py test`)

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations tracker
python manage.py migrate
python manage.py createsuperuser # optional, for /admin/
python manage.py runserver
```
Open http://127.0.0.1:8000/

## API
Log in through the site first (session auth), then:

| Method | URL | Purpose |
|---|---|---|
| GET | `/api/applications/?status=applied` | List your applications |
| POST | `/api/applications/` | Create one |
| GET/PUT/PATCH/DELETE | `/api/applications/<id>/` | Read, update, delete |

## Tests
```bash
python manage.py test
```

## Deploy (Render or similar)
Build: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py makemigrations tracker && python manage.py migrate`
Start: `gunicorn config.wsgi`
Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `DJANGO_ALLOWED_HOSTS=<your-domain>`, `DJANGO_CSRF_ORIGINS=https://<your-domain>`.
