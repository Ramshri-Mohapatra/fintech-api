# Fintech API — Personal Finance Tracker
![CI](https://github.com/Ramshri-Mohapatra/fintech-api/actions/workflows/ci.yml/badge.svg)
**Live API:** https://fintech-api-n3ds.onrender.com/docs

A production-ready REST API for personal finance tracking, built with FastAPI, PostgreSQL, JWT authentication, Docker, and CI/CD via GitHub Actions.

## Motivation

Most people manage their finances reactively, checking their bank balance when worried rather than when planning. This project is a production-ready backend API for a personal finance tracker that gives users a structured way to log, categorise, and analyse their transactions over time.

Built to demonstrate backend engineering skills directly relevant to fintech — JWT authentication, PostgreSQL data modelling, RESTful API design, Docker containerisation, and automated testing with CI/CD. These are the core skills used by engineering teams at companies like Revolut, Monzo, and Wise to build financial infrastructure at scale.

## Tech Stack

- **FastAPI** — high-performance Python web framework
- **PostgreSQL** — relational database for persistent storage
- **SQLAlchemy** — ORM for database modelling and queries
- **Alembic** — database migrations
- **JWT (python-jose)** — secure token-based authentication
- **bcrypt (passlib)** — password hashing
- **Docker** — containerisation
- **GitHub Actions** — CI/CD pipeline
- **pytest + httpx** — automated testing

## Project Structure
fintech-api/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic request/response schemas
│   ├── database.py      # Database connection and session
│   ├── auth.py          # JWT token logic and password hashing
│   └── routers/
│       ├── users.py     # Register and login endpoints
│       └── transactions.py  # CRUD transaction endpoints
├── tests/
│   ├── test_auth.py         # Auth endpoint tests
│   └── test_transactions.py # Transaction endpoint tests
├── .env                 # Environment variables (not committed)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Container build instructions
└── docker-compose.yml   # Multi-container setup

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /register | No | Create a new user account |
| POST | /login | No | Authenticate and receive JWT token |
| POST | /transactions | Yes | Log a new transaction |
| GET | /transactions | Yes | List transactions with filters |
| PUT | /transactions/{id} | Yes | Update a transaction |
| DELETE | /transactions/{id} | Yes | Delete a transaction |

## Getting Started

```bash
git clone https://github.com/Ramshri-Mohapatra/fintech-api.git
cd fintech-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Live Documentation

API docs available at `/docs` once running.