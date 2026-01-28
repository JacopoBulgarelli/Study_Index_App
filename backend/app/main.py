from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth, upload, query, quiz, flashcards, history
from app.core.config import settings
from app.db.session import engine
from app.db.models import Base

app = FastAPI(title="StudyIndex API", version="1.0.0")

# Create database tables
Base.metadata.create_all(bind=engine)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(query.router, prefix="/api/query", tags=["query"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["quiz"])
app.include_router(flashcards.router, prefix="/api/flashcards", tags=["flashcards"])
app.include_router(history.router, prefix="/api/history", tags=["history"])

@app.get("/")
def read_root():
    return {"message": "StudyIndex API is running."}