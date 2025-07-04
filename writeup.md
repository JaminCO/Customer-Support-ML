
# 🧠 Levels AI Assessment

## AI-Powered Support Ticket Backend

**Candidate:** _Jamin Onuegbu_  

---

## 🚀 Project Overview

This backend system automates customer support ticket handling using **FastAPI** and **Hugging Face Transformers**. It classifies incoming support messages (technical, billing, general), summarizes them, and exposes results via a REST API. The project demonstrates clean code structure, AI integration, and production-readiness with Docker, Redis, and Celery.

---

## 🏗️ Architecture & Design

### Code Structure

```
.
├── app/
│   ├── models/         # SQLAlchemy DB models
│   ├── schemas/        # Pydantic validation models
│   ├── services/       # AI pipelines (classification & summarization)
│   ├── routes/         # API endpoints (POST /requests, GET /requests)
├── scripts/            # Dataset ingestion script
├── tests/              # Pytest test cases
├── alembic/            # DB migration files
├── logs/               # Logs directory for AI/DB errors
├── main.py             # FastAPI app entry
├── docker-compose.yml  # Redis, Postgres, Celery, FastAPI stack
├── .env                # DB + secret config
├── requirements.txt    # Dependencies
```

> **Why this architecture?**  
> Modular design for clarity, scalability, and separation of concerns.

### ⚙️ Background Processing

- **Celery** offloads AI classification and summarization from the main thread.
- **Redis** serves as the Celery broker, managed via Docker Compose.
- All services are containerized for consistent, easy startup.


### API Endpoints

- **POST /requests**: Validates and stores a support ticket, triggers async AI classification and summarization.
- **GET /requests/{id}**: Retrieves a ticket with AI-generated fields.
- **GET /requests?category=...**: Lists tickets filtered by category.
- **GET /stats**: Returns ticket counts per category for the past 7 days.

### Data Models

- **SupportTicket**: Stores ticket text, subject, body, and metadata.
- **AIResult**: Stores AI-generated category, confidence, and summary, linked to tickets.

---

## 🔐 Security Approach

- **Input validation:** Pydantic ensures valid payloads.
- **Secrets:** Stored in `.env` and loaded securely.
- **SQL injection:** Prevented via SQLAlchemy ORM.
- **Language filtering:** Only English tickets processed to reduce model drift.
- **Production hardening:** JWT auth, rate limiting, and HTTPS recommended.
- **Background Worker:** Celery tasks for async processing of AI requests.


---

## 🧠 AI/ML Integration

### Models Used

| Task           | Model                      | Reason                                                               |
|----------------|----------------------------|----------------------------------------------------------------------|
| Classification | `facebook/bart-large-mnli` | Pretrained on NLI (MNLI), ideal for zero-shot classification         |
| Summarization  | `facebook/bart-large-cnn`  | Fine-tuned for news summarization (great for long support texts)     |

> _BART-MNLI evaluates candidate categories (“technical”, “billing”, “general”) as hypotheses against the ticket text._

### Planned Improvements

- Fine-tune models with real data.
- Add fallback heuristics for low-confidence predictions.
- Use async batching or queueing for AI calls under load.

---

## 🧪 Testing Strategy

- **Integration:** `pytest` and FastAPI `TestClient`.
- **Validation:** Input format and AI output consistency.
- **Unit tests:** Mock external models and test Celery workers independently.

---

## ⏳ Trade-Offs & Next Steps

### Skipped (for now):

- Auth and role-based access.
- Full model fine-tuning.
- Complete unit test coverage for Celery workers.

### Next Features:

- Multilingual support (language detection).
- Model latency optimization (on-device hosting).
- Monitoring (Prometheus + Grafana).

---

### CI-Ready
- Uses `pytest` for all tests, ensuring easy integration with CI/CD pipelines.
- All tests run with a single `pytest` command.

### Assumptions

- Only English tickets are relevant.
- AI results are not required to be real-time (async processing is acceptable).


## 📦 Deployment & Setup

### Requirements

```bash
pip install -r requirements.txt
```

### Docker Setup

```bash
docker-compose up --build
```

- Services: FastAPI, PostgreSQL, Redis, Celery
- Logs: `/logs/error_log.txt`

### Run Locally

```bash
uvicorn main:app --reload
```

- Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### Run Tests

```bash
pytest
```

---

## 🧾 Submission Notes

- ✅ Fully original work
- 📊 Dataset from Hugging Face used for AI training/testing
- 📝 Documentation provided in `README.md` and this writeup


## 🤖 AI Assistant Usage

- Used GitHub Copilot for code suggestions, boilerplate, and test scaffolding.
- All logic, architecture, and integration decisions were made independently.
- ChatGPT used for structuring and best practices


---

## ⚡ Special Setup Notes

- Requires Python 3.10+ (tested), PostgreSQL, and Redis.
- Hugging Face models are downloaded at runtime; ensure internet access for first run.
- Set `PYTHONPATH` to project root if import errors occur during testing.

---
