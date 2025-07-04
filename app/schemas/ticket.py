from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime



class TicketCreate(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=1000)
    subject: Optional[str] = Field(None, min_length=1, max_length=200)
    body: Optional[str] = Field(None, min_length=1, max_length=2000)

    # Validate that at least one of them is present
    def validate(self):
        if not self.text and not (self.subject and self.body):
            raise ValueError("Must provide either 'text' or both 'subject' and 'body'")
        return self

class TicketResponseNoAI(BaseModel):
    id: str
    subject: Optional[str] = None
    body: Optional[str] = None
    text: Optional[str] = None
    queue: Optional[str] = None
    priority: Optional[str] = None
    language: Optional[str] = None
    tags: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class TicketResponse(BaseModel):
    id: str
    subject: Optional[str] = None
    body: Optional[str] = None
    text: Optional[str]
    summary: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

class TicketStats(BaseModel):
    category: str
    count: int