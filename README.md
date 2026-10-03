# Flask Secret Notes — User Authentication + CRUD

A mini Flask app demonstrating **User Authentication** (Flask-Login + password hashing)
combined with a **CRUD application** — a personal notes vault where each user
saves private notes/reminders only they can see.

## Features
- User registration & login (passwords hashed with Werkzeug, never stored in plain text)
- Session-based authentication via Flask-Login
- Each user only sees and manages their own notes
- Full CRUD on notes (add, list, edit, delete)
- Optional category tag (Personal, Work, Ideas, Reminder, ...) and a "pin to top" toggle
- Notes auto-sort: pinned first, then most recently updated
- Flask-WTF forms with validation
- Flask-SQLAlchemy models (tables auto-created with `db.create_all()`)
- Jinja2 templates with template inheritance (`base.html`)
- Custom CSS (no external framework)

## Project structure
```
flask_auth_app/
├── app.py          # routes
├── models.py       # User + Note models
├── forms.py        # WTForms
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── note_form.html
└── static/
    └── style.css
```

## Setup & run
```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

python app.py
```
The database (`users.db`) and its tables are created automatically the first time you run the app.

Visit http://127.0.0.1:5000, register an account, then log in to start saving notes.
