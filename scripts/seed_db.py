from datasets import load_dataset
from sqlalchemy.orm import Session
from app.models.database import SessionLocal, engine
from app.models.ticket import SupportTicket, Base, AIResult
from dotenv import load_dotenv
import os
from uuid import uuid4

from app.utils.mylogger import log_error


load_dotenv()

# 1. Load Hugging Face dataset
dataset = load_dataset("tobi-bueck/customer-support-tickets", split="train")

# 2. Map queue to category
def map_category(queue):
    try:
        if "technical" in queue.lower() or "it support" in queue.lower():
            return "technical"
        elif "billing" in queue.lower() or "payments" in queue.lower():
            return "billing"
        else:
            return "general"
    except Exception as e:
        log_error("CATEGORY_MAPPING_ERROR", str(e), "map_category")
        return "general"

# 3. Map priority to confidence score
def map_confidence(priority):
    mapping = {"Critical": 0.9, "Medium": 0.6, "Low": 0.3}
    return mapping.get(priority, 0.5)

# 4. Filter and process data
def prepare_data(entry):
    try:
        if not entry.get("subject") and not entry.get("body"):
            log_error("EMPTY_TICKET_ERROR", "Ticket has no subject or body", "prepare_data")
            return None
        subject = entry.get("subject") or ""
        body = entry.get("body") or ""
        text = f"{subject.strip()}. {body.strip()}" if subject else body.strip()

        return SupportTicket(
            id=str(uuid4()),
            subject=subject,
            body=body,
            text=text,
            queue=entry.get("queue"),
            priority=entry.get("priority"),
            language=entry.get("language", "en"),
        )
    except Exception as e:
        log_error("TICKET_PREPARATION_ERROR", str(e), "prepare_data")
        return None

def seed_airesults(entry, ticket_id):
    try:
        return AIResult(
            id=str(uuid4()),
            ticket_id=ticket_id,
        category=map_category(entry.get("queue", "")),
        confidence=map_confidence(entry.get("priority", "")),
        summary=entry.get("answers", "")
        )
    except Exception as e:
        log_error("AI_RESULT_PREPARATION_ERROR", str(e), "seed_airesults")
        return None

# 5. Connect to DB and add entries
def seed_database():
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        db: Session = SessionLocal()

        print("Seeding database with English tickets...")

        for entry in dataset:
            if entry.get("language") != "en":
                continue
            ticket = prepare_data(entry)
            db.add(ticket)
            db.flush()
            
            ai_results = seed_airesults(entry, ticket.id)
            db.add(ai_results)

        db.commit()
        db.close()
        print("Seeding completed.")
    except Exception as e:
        log_error("DATABASE_SEEDING_ERROR", str(e), "seed_database")
        raise e

if __name__ == "__main__":
    seed_database()
