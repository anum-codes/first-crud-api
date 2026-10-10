# Task API - FlyRank Backend Internship (Week 2)

A lightweight, robust CRUD (Create, Read, Update, Delete) REST API built using **Python** and **FastAPI**, featuring in-memory data storage, automatic Pydantic request validation, and interactive documentation via Swagger UI.

---

## 🛠️ How to Install and Run

Make sure you have Python 3.10+ installed on your system.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn pydantic
   ```

4. **Run the server:**
   *(Note: Replace `main` with your actual file name if it differs, e.g., `firstcrudapi:app`)*
   ```bash
   uvicorn main:app --reload
   ```

5. Open your browser and navigate to **`http://localhost:8000/docs`** to view and test the Swagger UI interface.

---

## 🧭 API Endpoints

| HTTP Method | Endpoint Path | Description | Status Codes |
| :--- | :--- | :--- | :--- |
| **GET** | `/` | Returns general API information and available endpoints | `200 OK` |
| **GET** | `/health` | Server health check endpoint | `200 OK` |
| **GET** | `/tasks` | Retrieves all tasks stored in memory | `200 OK` |
| **GET** | `/tasks/{id}` | Retrieves a single specific task by its ID | `200 OK`, `404 Not Found` |
| **POST** | `/tasks` | Creates a new task with validation | `201 Created`, `422 Unprocessable Entity` |
| **PUT** | `/tasks/{id}` | Updates an existing task's title and completion status | `200 OK`, `404 Not Found` |
| **DELETE** | `/tasks/{id}` | Deletes a task by its ID | `204 No Content`, `404 Not Found` |

---

## 💻 Sample `curl -i` Output

Testing the root endpoint (`GET /`):

```bash
curl.exe -i "http://localhost:8000/"
```

**Response:**
```http
HTTP/1.1 200 OK
date: Sat, 10 Oct 2026 21:25:00 GMT
server: uvicorn
content-type: application/json
content-length: 74

{
  "name": "Task API",
  "version": "1.0",
  "endpoints": ["/tasks"]
}
```

---

## 📸 Swagger UI Screenshot

Below is an interactive view of the API documentation generated automatically by FastAPI at `/docs`:

![Swagger UI Screenshot](./docs/swagger-screenshot.png)
*(Tip: Replace `./docs/swagger-screenshot.png` with the actual path to your saved screenshot file in your repo!)*

---

## 💡 Notes on In-Memory Storage
As per the assignment requirements, data is stored strictly in memory via Python lists and dictionaries. Restarting the FastAPI server will reset the dataset back to its default pre-filled example tasks.