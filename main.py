import sqlite3
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

app = FastAPI()

#function to initialize the database and table
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    #Create tasks table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN DEFAULT 0
    )
""")

    #Seed three example tasks only if the table is empty
    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("INSERT INTO tasks (title,done) VALUES (?,?)", ("Buy Milk", 0))
        cursor.execute("INSERT INTO tasks (title,done) VALUES (?,?)", ("Pay Bills", 1))
        cursor.execute("INSERT INTO tasks (title,done) VALUES (?,?)", ("Learn FastAPI",0))
        conn.commit()
    conn.close()

#Run Initialization on startup
init_db()

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


# Get all tasks
@app.get("/tasks")
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row    #accessing columns by names
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close

    #convert database rows into dictionaries and normalize 'done' to boolean
    tasks_list = []
    for row in rows:
        tasks_list.append({
            "id":row["id"],
            "title":row["title"],
            "done":bool(row["done"])
        })
    return tasks_list

# Get single task by ID
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    
    return {
        "id":row["id"],
        "title":row["title"],
        "done":bool(row["done"])
    }

#Stage 3: Create — POST a New Task

class TaskCreate(BaseModel):
    title: str

# Create task endpoint
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    #validate title for empty and whitespace
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail={"error":"Title cannot be empty"})

    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    #Insert task in sqlite using parameterized query
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?,?)", (task.title.strip(), 0))
    conn.commit()

    #Get the auto assigned id of new task
    new_task_id = cursor.lastrowid

    #Fetch the new created row to return it
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (new_task_id,))
    row = cursor.fetchone()
    conn.close()

    return {
        "id": row["id"],
        "title": row["title"],
        "done":bool(row["done"])
    }

# #Stage 4: Update & Delete

# class TaskUpdate(BaseModel):
#     pass

# # Update endpoint
# @app.put("/tasks/{task_id}")
# def update_task(task_id: int, task_data: TaskUpdate):
#     pass

# # Delete endpoint
# @app.delete("/tasks/{task_id}", status_code=204)
# def delete_task(task_id: int):
#     pass