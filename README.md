# 🖋️ TATRACK — Tattoo Artist CRM

A full-stack micro-CRM for tattoo artists. Never lose a client again.

## Tech Stack
- **Backend**: Flask 3, SQLAlchemy, Flask-Login, Flask-Migrate
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Frontend**: Jinja2 templates, vanilla JS, custom CSS design system

## Quick Start

### 1. Install dependencies
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment (optional)
```bash
cp .env.example .env
# Edit .env with your DATABASE_URL and SECRET_KEY
```

### 3. Run (SQLite — no setup needed)
```bash
python run.py
```
Visit: http://localhost:5000

### 4. PostgreSQL setup
```bash
# Set in .env:
DATABASE_URL=postgresql://user:pass@localhost/tatrack
SECRET_KEY=your-secret-key

flask db init
flask db migrate -m "initial"
flask db upgrade
python run.py
```

## Features
- ✦ **Inquiry Pipeline** — Kanban board with 6 status columns
- ◉ **Reminders** — Auto-set follow-ups, overdue alerts
- ◈ **Sessions** — Booking management with deposit tracking
- ◇ **Payments** — Deposit/balance/revenue tracking
- ⬡ **Dashboard** — Live stats and today's schedule

## API Endpoints
| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/register | Register artist |
| POST | /api/login | Login |
| GET/POST | /api/inquiries | List / Create |
| PUT/DELETE | /api/inquiries/:id | Update / Delete |
| GET/POST | /api/reminders | List / Create |
| PUT | /api/reminders/:id/complete | Mark done |
| GET/POST | /api/sessions | List / Book |
| PUT | /api/sessions/:id | Update |
| GET/POST | /api/payments | List / Record |
| PUT | /api/payments/:id | Update |
| GET | /api/dashboard/stats | Dashboard data |
