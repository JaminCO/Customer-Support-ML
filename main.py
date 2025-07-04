from fastapi import FastAPI
from app.routes.ticket import router as router
from app.models.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Support Ticket Backend",
    description="AI-powered automation workflow for customer support tickets",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")