# Flask Auth App

A full-stack user authentication web application built with Python, Flask, SQLAlchemy, and Flask-Login. Supports user registration, login, session management, and a protected dashboard.

## Features

- User registration with duplicate username/email detection
- Secure password hashing (Werkzeug PBKDF2-SHA256)
- Session-based login with "remember me" support
- Protected dashboard route — redirect to login if unauthenticated
- Open-redirect protection on the `next` parameter
- Environment-based configuration — no hard-coded secrets
- SQLite locally, configurable via `DATABASE_URL`

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.12 · Flask 3.1 |
| ORM | SQLAlchemy 2.0 · Flask-SQLAlchemy |
| Auth | Flask-Login · Werkzeug password hashing |
| Database | SQLite (local) · configurable via env |
| Deployment | Vercel (serverless) · Render (gunicorn) |

## Local Development

### Prerequisites
- Python 3.12+

### Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd flask-auth-app

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env — set SECRET_KEY to a long random string

# 5. Run the application
flask run --port 5001
# or
python app.py
```

The app will be available at [http://127.0.0.1:5001](http://127.0.0.1:5001).

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ Yes | Long random string for session signing |
| `DATABASE_URL` | No | SQLAlchemy DB URI (default: `sqlite:///database.db`) |
| `FLASK_DEBUG` | No | Set to `1` to enable debug mode (development only) |

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## Deployment

### Vercel
Set `SECRET_KEY` in your Vercel project environment variables. The app uses `/tmp/database.db` on Vercel (ephemeral — resets on redeploy). For production persistence, set `DATABASE_URL` to a managed PostgreSQL instance.

### Render
Configure `SECRET_KEY` and optionally `DATABASE_URL` in Render's environment section. The `render.yaml` uses gunicorn as the production WSGI server.

## Security Notes

- `SECRET_KEY` is required at startup — the app will not run without it.
- Debug mode is disabled by default. Enable only in development.
- Session cookies are set with `HttpOnly` and `SameSite=Lax`.
- The `next` redirect parameter is validated to prevent open redirects.
- Passwords are stored as hashed values only (PBKDF2-SHA256 via Werkzeug).

## Project Structure

```
flask-auth-app/
├── app.py              # Application factory and routes
├── models.py           # SQLAlchemy User model
├── requirements.txt
├── .env.example        # Template for environment variables
├── render.yaml         # Render deployment config
├── vercel.json         # Vercel deployment config
├── tests/
│   └── test_auth.py    # Pytest test suite
├── static/css/
│   └── style.css
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── signup.html
    └── dashboard.html
```
