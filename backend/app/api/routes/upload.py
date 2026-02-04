# backend/app/api/routes/upload.py
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from app.ingestion.pageindex_loader import PageIndexLoader
from app.db.session import get_db
from app.llm.client import get_llm_client

router = APIRouter()

@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save file temporarily
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Trigger async ingestion
    loader = PageIndexLoader(db, get_llm_client())
    
    # Option 1: Synchronous for small docs
    doc = await loader.ingest_document(temp_path, file.filename)
    
    # Option 2: Background task for large docs (recommended)
    # background_tasks.add_task(loader.ingest_document, temp_path, file.filename)
    
    return {
        "document_id": doc.id,
        "status": "processing" if background_tasks else "completed",
        "message": "Document structure extracted via PageIndex, content being embedded"
    }