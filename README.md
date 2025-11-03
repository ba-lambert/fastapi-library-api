# Library Management API (FastAPI)

A production-leaning REST API for a small library system built with FastAPI, SQLAlchemy, and PostgreSQL. It supports user sign-up/login with JWT, role-based access control, book catalog management, stock tracking, borrowing flow, and a background scheduler that can import books from Google Books.

## Features
- FastAPI-based HTTP API with automatic OpenAPI docs
- PostgreSQL + SQLAlchemy ORM models & Alembic migrations
- JWT auth (HTTP Bearer) with role-based guards (guest, librarian, admin)
- Books: list, fetch from Google Books, create (librarian only)
- Stock: add or increase stock, view stock by book
- Borrow: borrow a book, decrements stock
- Background job (APScheduler) to periodically import books

Note: The scheduler in `app/utils/book_scheduler.py` uses a hard-coded user ID for `BOK_USER_ID`. Update it to a real user in your DB or disable the job during development to avoid integrity errors on startup.

## Tech Stack
- Python, FastAPI, Pydantic
- SQLAlchemy, Alembic
- PostgreSQL (psycopg2)
- JWT (PyJWT), pwdlib for secure hashing
- APScheduler for background tasks

## Project layout
```
app/
  main.py                     # FastAPI app & routers
  database/db.py              # DB engine & session
  models/                     # SQLAlchemy models
  schemas/                    # Pydantic request/response models
  services/                   # Business logic
  routes/                     # API endpoints
  utils/                      # JWT, scheduler, external APIs
alembic/                      # Alembic migrations
alembic.ini                   # Alembic config (sqlalchemy.url)
requirements.txt
```

## Prerequisites
- Python 3.11+ (3.14 shown in __pycache__ but target 3.11/3.12 is recommended)
- PostgreSQL running locally
- Windows shell commands below assume `cmd.exe`

## Quick start
1) Clone repo and create a virtual environment
```
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2) Configure environment
- Copy `.env.example` to `.env` and update `DATABASE_URL` as needed.
- Ensure Alembic URL in `alembic.ini` matches your database or update it.

3) Create database schema
```
alembic upgrade head
```

4) Run the API server
```
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

5) Explore docs
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Authentication
- Sign up at `POST /user/signup`
- Log in at `POST /user/login` using the same `username` (or email) and `password`
- Use the returned `token` as a Bearer token in the `Authorization` header: `Authorization: Bearer <token>`

The default token expiry and secret are hard-coded in `app/utils/security_utils.py`. For production, move them to environment variables.

## API overview
Base URL prefix: none (routers mount under /user, /books, /stock, /borrow)

- User
  - POST `/user/signup` — create an account
    - body: `{ username, full_name?, email, gender: male|female, password }`
  - POST `/user/login` — returns `{ token, user }`
  - PUT `/user/assign-role/{id}?role=admin|guest|librarian` — change role (no guard in code; protect externally or extend)

- Books
  - GET `/books/external?q=programming&start_index=0&max_results=10` — fetch from Google Books
  - GET `/books/{id}` — get by ID
  - GET `/books?offset=0&limit=10` — list
  - POST `/books` — create book (requires role librarian)
    - body: `{ title, author, published_year, isbn, description (<=200 words), cover_url, publisher }`

- Stock
  - POST `/stock` — add/increase stock for a book
    - body: `{ book_id, quantity }`
  - GET `/stock/{book_id}` — get stock for a book

- Borrow
  - POST `/borrow` — borrow a book (auth required)
    - body: `{ book_id, quantity, borrowed_at, will_return_at }`

Notes:
- Borrow decreases `STK_QUANTITY` if sufficient quantity is available, otherwise 400.
- `book_scheduler.py` starts a background job on app startup that fetches and stores books every 24h.

## Environment variables
- DATABASE_URL (required by `app/database/db.py`)
  - Example: `postgresql://admin:admin123@localhost/library-db`
- Alembic also uses the URL in `alembic.ini` (keep in sync)

## Running migration commands
- Create a new revision (autogenerate):
```
alembic revision --autogenerate -m "your message"
```
- Apply latest:
```
alembic upgrade head
```
- Rollback one:
```
alembic downgrade -1
```

## Development tips
- Use a dedicated DB per developer to avoid conflicts.
- Keep `requirements.txt` in sync; `pwdlib` is required for password hashing.
- Prefer environment variables for secrets; avoid hard-coding.
- Return models directly works with FastAPI thanks to Pydantic `from_attributes=True` or use explicit response models.

## Testing the flow quickly
1) Sign up
```
POST /user/signup
{
  "username": "alice",
  "full_name": "Alice Doe",
  "email": "alice@example.com",
  "gender": "female",
  "password": "Str0ngP@ss"
}
```
2) Login and copy token
```
POST /user/login
{
  "username": "alice",
  "password": "Str0ngP@ss"
}
```
3) Create a book (as librarian)
- First, give the user the librarian role using the assign-role endpoint with the user's UUID returned from signup or via DB.
4) Add stock for the created book
5) Borrow with the token in Authorization header

## Production notes
- Run Uvicorn with workers (e.g., gunicorn + uvicorn workers on Linux) and a persistent scheduler strategy or move scheduled job to a separate process.
- Use HTTPS and rotate JWT secret keys.
- Apply DB migrations during deployments.

## License
MIT
