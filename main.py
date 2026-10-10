from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

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

#Stage 3: Create — POST a New Task

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)

# Create task endpoint
@app.post("/tasks", status_code=201)
def create_task(task_data: TaskCreate):
    # Calculate next ID cleanly
    new_id = max([t["id"] for t in tasks], default=0) + 1
    new_task = {
        "id": new_id,
        "title": task_data.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

#Stage 4: Update & Delete

class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    done: bool

# Update endpoint
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = task_data.title
            task["done"] = task_data.done
            return task
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})

# Delete endpoint
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404, detail={"error": f"Task {task_id} not found"})