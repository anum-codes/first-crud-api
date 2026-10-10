from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

app = FastAPI()

# Stage 1: Root & Health Endpoints
@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}