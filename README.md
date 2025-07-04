# Customer Support ML

A FastAPI-based customer support ticketing system with machine learning integration for ticket classification and summarization.  
Includes Celery for background AI tasks, PostgreSQL for storage, Redis for task brokering, and Docker Compose for easy setup.

---

## Features

- **REST API** for ticket creation, retrieval, and listing
- **Celery** for asynchronous AI processing (classification & summarization)
- **PostgreSQL** database (via SQLAlchemy ORM)
- **Redis** as Celery broker and result backend
- **ML Integration** using HuggingFace Transformers
- **Docker Compose** for local development
- **Testing** with pytest and FastAPI TestClient

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/customer-support-ml.git
cd customer-support-ml
```

---

### 2. Environment Variables

Copy `.env.example` to `.env` and adjust as needed, or use the provided `.env`:

```env
DATABASE_URL=postgresql://admin:password@localhost/support_db
REDIS_URL=redis://redis:6379/0 # For Docker

# For local development, you can use:
REDIS_URL=redis://localhost:6379/0
```

---

### 3. Start Database and Redis (Docker Compose)

Make sure Docker is running, then:

```sh
docker-compose up -d db csml_redis
```

This will start:
- **PostgreSQL** on port 5432
- **Redis** on port 6379

---

### 4. Database Migration

Run Alembic migrations to create tables:

```sh
alembic upgrade head
```

---

### 5. Install Python Dependencies

It’s recommended to use a virtual environment:

```sh
#### Using `venv` + `pip`

```sh
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Linux/Mac

pip install -r requirements.txt
```

#### Or using `pipenv`

```sh
pip install pipenv
pipenv install --dev
pipenv shell
```
```

---

### 6. Start the FastAPI Server

```sh
uvicorn main:app --reload
```

The API will be available at [http://localhost:8000](http://localhost:8000).

---

### 7. Start Celery Worker

In a new terminal (with the virtual environment activated):

```sh
celery -A app.routes.ticket.celery_app worker --pool=threads --loglevel=info
```
OR you can also run the dockerized Celery worker:

```sh
docker-compose up -d csml_worker
```

---

### 8. Run Tests

```sh
pytest
```

- Make sure your environment variables are set and the database/Redis are running.
- Tests include core logic, ML integration (mocked), API endpoints, and dataset accuracy.

---

## Project Structure

| Path/Directory         | Description                                         |
|------------------------|-----------------------------------------------------|
| `app/models/`          | SQLAlchemy DB models                                |
| `app/schemas/`         | Pydantic validation models                          |
| `app/services/`        | AI pipelines (classification & summarization)       |
| `app/routes/`          | API endpoints (POST /requests, GET /requests)       |
| `app/utils/`           | Utility functions (e.g., logger)                    |
| `scripts/`             | Dataset ingestion script                            |
| `tests/`               | Pytest test cases                                   |
| `alembic/`             | DB migration files                                  |
| `logs/`                | Logs directory for AI/DB errors                     |
| `main.py`              | FastAPI app entry                                   |
| `Dockerfile`           | Docker build instructions for the app               |
| `docker-compose.yml`   | Redis, Postgres, Celery, FastAPI stack              |
| `.env`                 | DB + secret config                                  |
| `requirements.txt`     | Dependencies                                        |

---

## Useful Commands

- **Run migrations:** `alembic upgrade head`
- **Start API server:** `uvicorn main:app --reload`
- **Start Celery worker:** `celery -A app.routes.ticket.celery_app worker --pool=threads --loglevel=info`
- **Run tests:** `pytest`

---

## Notes

- For local development, ensure `PYTHONPATH` is set to the project root if you encounter import errors:
  ```sh
  set PYTHONPATH=%CD%  # Windows
  export PYTHONPATH=$(pwd)  # Linux/Mac
  ```
- Adjust `.env` variables if running services in Docker vs. locally.
- For production, configure secure credentials and proper environment separation.

---

## License

MIT License

---