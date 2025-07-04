from fastapi import APIRouter, HTTPException, Query, Path, Body, status, Depends
from typing import Optional, List, Dict
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from sqlalchemy.orm import Session
from celery import Celery
from redis import Redis
from dotenv import load_dotenv
import os

from app.models.database import get_db
from app.utils.mylogger import log_error
from app.schemas.ticket import TicketResponse, TicketCreate, TicketStats, TicketResponseNoAI
from app.models.ticket import SupportTicket, AIResult
from app.models.database import SessionLocal
from app.services.ai import classify_text, generate_summary

load_dotenv()

# CELERY

REDIS_URL = "redis://localhost:6379/0"
# os.getenv('REDIS_URL', 'redis://localhost:6379/0')
BACKEND_REDIS_URL = "redis://localhost:6379/1"
# os.getenv('BACKEND_REDIS_URL', 'redis://localhost:6379/0')


# print(f"REDIS_URL: {REDIS_URL}")

celery_app = Celery(
    "csml",
    broker=REDIS_URL,
    backend=BACKEND_REDIS_URL,
)


celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_always_eager=False,
    worker_concurrency=1,
    worker_enable_asyncio=True,

)

@celery_app.task(name='ai_pipeline.trigger_ai_pipeline')
def trigger_ai_pipeline(ticket_text: str, ticket_id: str):
    try:
        if not ticket_text or not ticket_id:
            raise ValueError("Ticket text and ID must be provided")
        db: Session = next(get_db())
        ai_result = classify_text(ticket_text)
        ai_summary = generate_summary(ticket_text)
        ai_result_ticket = AIResult(
            id=str(uuid4()),
            ticket_id=ticket_id,
            category=ai_result['category'],
            confidence=ai_result['confidence'],
            summary=ai_summary,
        )
        db.add(ai_result_ticket)
        db.commit()
        db.refresh(ai_result_ticket)

        return {"result": ai_result, "summary": ai_summary}
    except Exception as e:
        log_error("AI_PIPELINE_ERROR", str(e), "trigger_ai_pipeline")
        raise e


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/requests", response_model=TicketResponse, status_code=status.HTTP_201_CREATED, description="Accepts new ticket, validates input, stores it, triggers AI pipeline")
def create_ticket(ticket_in: TicketCreate, db: Session = Depends(get_db)):
    try:
        ticket_id = str(uuid4())
        ticket_in.validate()

        subject = ticket_in.subject or ""
        body = ticket_in.body or ""
        text = f"{subject.strip()}. {body.strip()}"

        now = datetime.now(timezone.utc)

        ticket = SupportTicket(
            id=ticket_id,
            text=(ticket_in.text if ticket_in.text else text),
            subject=(ticket_in.subject if ticket_in.subject else ""),
            body=(ticket_in.body if ticket_in.body else ""),
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        print(f"Ticket created with ID: {ticket.id}")
        
        # AI processing
        ai_result = trigger_ai_pipeline.delay(ticket.text, ticket.id)

        return TicketResponse(
            id=ticket.id,
            text=ticket.text,
            subject=ticket.subject,
            body=ticket.body,
            created_at=ticket.created_at,
        )
    except Exception as e:
        log_error("TICKET_CREATION_ERROR", str(e), "create_ticket")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/requests/{ticket_id}", response_model=TicketResponse, description="Retrieve ticket by ID with AI fields")
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Fetch AI fields if available
    ai_result = db.query(AIResult).filter(AIResult.ticket_id == ticket_id).first()

    ai_summary = ai_result.summary if ai_result else None
    ai_category = ai_result.category if ai_result else None

    # Pass through the TicketResponse schema
    ticket_response = TicketResponse(
        id=ticket.id,
        text=ticket.text,
        subject=ticket.subject,
        body=ticket.body,
        summary=ai_summary,
        category=ai_category,
        confidence=ai_result.confidence,
        created_at=ticket.created_at
    )
    return ticket_response
   
@router.get("/requests", response_model=List[TicketResponseNoAI], description="List all tickets with optional category filter")
def list_tickets(category: Optional[str] = Query(None, description="Filter by category"), db: Session = Depends(get_db)):
    try:
        query = db.query(SupportTicket).join(AIResult, SupportTicket.id == AIResult.ticket_id)
        if category:
            query = query.filter(SupportTicket.queue == category)
        return query.limit(50).all()
    except Exception as e:
        log_error("TICKET_LISTING_ERROR", str(e), "list_tickets")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/stats", response_model=List[TicketStats])
def get_stats(db: Session = Depends(get_db)):
    try:
        now = datetime.now(timezone.utc)
        week_ago = now - timedelta(days=7)
        counts = {}
        for ticket in db.query(SupportTicket).all():
            created_at = ticket.created_at
            if created_at is not None and created_at.tzinfo is None:
                # Assume naive datetimes are in UTC
                created_at = created_at.replace(tzinfo=timezone.utc)
            if created_at and created_at >= week_ago:
                cat = ticket.queue or "uncategorized"
                counts[cat] = counts.get(cat, 0) + 1
        return [TicketStats(category=cat, count=count) for cat, count in counts.items()]
    except Exception as e:
        log_error("TICKET_STATS_ERROR", str(e), "get_stats")
        raise HTTPException(status_code=500, detail="Internal Server Error")