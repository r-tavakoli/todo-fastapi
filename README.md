# 📝 To-Do API with FastAPI

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-336791.svg)](https://www.postgresql.org/)
[![Status](https://img.shields.io/badge/Status-In_Progress-orange.svg)]()

> ⚠️ **Project Status**: This project is currently **in progress** and is being built purely for **educational and practice purposes** to master backend development patterns with FastAPI.

---

## ⚡ Features

* **Full CRUD Operations**: Create, read, update, and delete to-do items.
* **Data Validation**: Powered by Pydantic for strict input validation and explicit error handling.
* **Automatic Documentation**: Interactive API documentation generated instantly via Swagger UI and scalar-fastapi.
* **SQL Database Integration**: Configured with SQLAlchemy for ORM capability.

---

## 🛠️ Tech Stack

* **Backend Framework**: FastAPI
* **Database**: Postgres
* **Data Validation**: Pydantic v2

---

## 📁 Project Structure

```text
simple_todo_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                 # App entry point, creates FastAPI instance
│   ├── config.py               # Settings via pydantic-settings
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py     # Shared dependencies (auth, db session)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py       # Aggregates all v1 routers
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── tasks.py
│   │           └── users.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py          # SQLAlchemy engine & session
│   │
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── tasks.py
│   │
│   ├── schemas/                # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── tasks.py
│   │
│   └── services/               # Business logic layer
│       ├── __init__.py
│       └── users_service.py
│
├── .env
├── .gitignore
└── requirements.txt
