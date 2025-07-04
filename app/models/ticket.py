from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from app.models.database import Base
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import relationship

class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    subject = Column(String, nullable=True)
    body = Column(Text, nullable=False)
    text = Column(Text, nullable=True)
    queue = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    language = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    ai_results = relationship("AIResult", backref="ticket", cascade="all, delete-orphan")

    created_at = Column(DateTime, nullable=True, default=lambda: datetime.now(timezone.utc))



class AIResult(Base):
    __tablename__ = "ai_results"

    id = Column(String, primary_key=True, index=True, default=str(uuid4()))
    ticket_id = Column(String, ForeignKey("support_tickets.id"), nullable=True)
    category = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=True, default=lambda: datetime.now(timezone.utc))

