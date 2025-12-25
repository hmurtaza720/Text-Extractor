# from .celery_app import celery_app
from .database import SessionLocal
from .models import Document
import time
import os
import requests

# CONFIGURATION: N8N Webhook URL
# Replace this with your actual N8N Webhook URL (POST)
# Example: "http://localhost:5678/webhook/process-document"
N8N_WEBHOOK_URL = "https://interpretive-dwana-electromechanical.ngrok-free.dev/webhook/91860155-7198-4368-af12-fb0a311da427"
APP_BASE_URL = "https://reprobative-beverlee-irrelative.ngrok-free.dev" # Updated to Ngrok URL

# @celery_app.task(bind=True)
def process_document_task(doc_id: int):
    # self argument removed since it's no longer a bound task
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            return "Document not found"
        
        # Construct the file URL so N8N can download it
        # Assuming filename is stored or derived from path
        filename = os.path.basename(doc.original_path)
        file_download_url = f"{APP_BASE_URL}/{doc.original_path.replace(os.sep, '/')}"
        
        print(f"Triggering N8N for Doc ID: {doc_id} | URL: {file_download_url}")

        payload = {
            "doc_id": doc.id,
            "filename": doc.filename,
            "file_url": file_download_url,
            "original_path": doc.original_path
        }

        try:
            # Send Webhook to N8N
            response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=5)
            
            if response.status_code >= 200 and response.status_code < 300:
                doc.status = "Sending to N8N..."
                print(f"N8N Triggered Successfully: {response.text}")
            else:
                 doc.status = f"N8N Error: {response.status_code}"
                 print(f"N8N Webhook Failed: {response.status_code} - {response.text}")

        except Exception as we:
            print(f"Failed to connect to N8N: {we}")
            doc.status = "N8N Connection Failed"
            
            # Fallback/Debug note: If N8N is not running, we just leave it.
            # You can retry later or process manually.

        db.commit()
    except Exception as e:
        if doc:
            doc.status = "Error"
            db.commit()
        print(f"Error processing document {doc_id}: {e}")
    finally:
        db.close()
