# Workspace & Task Management API

A RESTful API for workspace and task management built with FastAPI and SQLite.

## Overview

This project provides a lightweight backend for managing users, workspaces, and tasks. It includes user assignment to workspaces, task tracking, and summary statistics.

### Features
- User and workspace management
- User-to-workspace assignment
- Task creation and status tracking
- Task filtering by workspace
- Summary statistics dashboard
- Input validation and error handling
- Auto-generated API documentation (Swagger UI)

## Tech Stack
- **FastAPI** — Web framework
- **SQLModel** — ORM (SQLAlchemy + Pydantic)
- **SQLite** — Database
- **Uvicorn** — ASGI server

## Project Structure

```
workspace-api/
├── main.py              # API endpoints and business logic
├── models.py            # Database models and schemas
├── workspace.db         # SQLite database (auto-generated)
├── venv/                # Virtual environment
├── requirements.txt     # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.12 or higher
- pip

### Installation

1. Navigate to the project directory:
```bash
cd workspace-api
```

2. Create a virtual environment:

**Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn main:app --reload
```

5. Access the API:
   - **Interactive Documentation**: http://127.0.0.1:8000/docs
   - **API Base URL**: http://127.0.0.1:8000

## API Endpoints

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users` | Create a user |
| GET | `/users` | List all users |

### Workspaces
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workspaces` | Create a workspace |
| GET | `/workspaces` | List all workspaces |
| POST | `/workspaces/{workspace_id}/users` | Assign user to workspace |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a task |
| GET | `/tasks?workspaceId={id}` | Get tasks by workspace |
| PATCH | `/tasks/{task_id}` | Mark task as complete |

### Summary
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/summary` | Get system statistics |

## Usage Examples

**Create a User**
```bash
POST http://127.0.0.1:8000/users
Content-Type: application/json

{
  "name": "Alice Johnson",
  "email": "alice@example.com"
}
```

**Create a Workspace**
```bash
POST http://127.0.0.1:8000/workspaces
Content-Type: application/json

{
  "name": "Marketing Team",
  "description": "Marketing campaigns and content creation"
}
```

**Assign User to Workspace**
```bash
POST http://127.0.0.1:8000/workspaces/1/users?workspace_id=1&user_id=1
```

**Create a Task**
```bash
POST http://127.0.0.1:8000/tasks
Content-Type: application/json

{
  "title": "Design new logo",
  "description": "Create 3 logo variations",
  "workspace_id": 1,
  "completed": false
}
```

**Get Tasks by Workspace**
```bash
GET http://127.0.0.1:8000/tasks?workspaceId=1
```

**Mark Task as Complete**
```bash
PATCH http://127.0.0.1:8000/tasks/1
```

**Get Summary**
```bash
GET http://127.0.0.1:8000/summary
```

## Testing

Use the interactive Swagger UI for testing:

1. Start the server
2. Open http://127.0.0.1:8000/docs
3. Expand an endpoint and click "Try it out"
4. Enter parameters and click "Execute"

## Database Schema

| Table | Columns |
|-------|---------|
| **User** | id, name, email |
| **Workspace** | id, name, description |
| **WorkspaceUser** | id, workspace_id, user_id |
| **Task** | id, title, description, workspace_id, completed |

## Error Handling

The API returns standard HTTP status codes:

- **400 Bad Request** — Validation error
- **404 Not Found** — Resource not found
- **422 Unprocessable Entity** — Schema validation failure

Example error response:
```json
{
  "detail": "Workspace not found"
}
```

## Implementation Status

User management  
Workspace management  
Task management  
Summary dashboard  
Input validation  
Error handling  

## Design Notes

- **Multi-tenant**: Workspaces operate independently
- **Normalized schema**: Junction table prevents data duplication
- **RESTful**: Follows REST conventions
- **SQLite**: File-based for simplicity; easily upgradeable to PostgreSQL

## Troubleshooting

**Server won't start**
- Verify virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (requires 3.12+)

**"Module not found" error**
- Activate the virtual environment
- Run: `pip install -r requirements.txt`

**Database errors**
- Delete `workspace.db` and restart the server (tables recreate automatically)

## Author

Dalee Kumawat  
February 5, 2026