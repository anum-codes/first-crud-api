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

# Stage 2: In-memory "database" pre-filled with 3 example tasks
tasks = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Complete Stage 2", "done": True},
    {"id": 3, "title": "Learn FastAPI", "done": False},
]

# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks

# Get single task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})