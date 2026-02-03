from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from models import User, Workspace, WorkspaceUser, Task, create_db_and_tables, get_session, engine
from typing import List

app = FastAPI(title="Workspace API")

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ========== USER ENDPOINTS ==========

@app.post("/users", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    """Create a new user"""
    if not user.name or len(user.name.strip()) < 2:
        raise HTTPException(
            status_code=400, 
            detail="Name must be at least 2 characters long"
        )
    
    if not user.email or '@' not in user.email:
        raise HTTPException(
            status_code=400, 
            detail="Invalid email format"
        )
    
    # Clean the data
    user.name = user.name.strip()
    user.email = user.email.strip()

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users", response_model=List[User])
def get_users(session: Session = Depends(get_session)):
    """Get all users"""
    users = session.exec(select(User)).all()
    return users

# ========== WORKSPACE ENDPOINTS ==========

@app.post("/workspaces", response_model=Workspace)
def create_workspace(workspace: Workspace, session: Session = Depends(get_session)):
    """Create a new workspace"""
    if not workspace.name or len(workspace.name.strip()) < 2:
        raise HTTPException(
            status_code=400, 
            detail="Workspace name must be at least 2 characters long"
        )
    
    # Clean the data
    workspace.name = workspace.name.strip()
    if workspace.description:
        workspace.description = workspace.description.strip()

    session.add(workspace)
    session.commit()
    session.refresh(workspace)
    return workspace

@app.get("/workspaces", response_model=List[Workspace])
def get_workspaces(session: Session = Depends(get_session)):
    """Get all workspaces"""
    workspaces = session.exec(select(Workspace)).all()
    return workspaces

@app.post("/workspaces/{workspace_id}/users")
def assign_user_to_workspace(
    workspace_id: int, 
    user_id: int,
    session: Session = Depends(get_session)
):
    """Assign a user to a workspace"""
    # Check if workspace exists
    workspace = session.get(Workspace, workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    # Check if user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already assigned
    existing = session.exec(
        select(WorkspaceUser).where(
            WorkspaceUser.workspace_id == workspace_id,
            WorkspaceUser.user_id == user_id
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="User already assigned to workspace")
    
    # Create assignment
    workspace_user = WorkspaceUser(workspace_id=workspace_id, user_id=user_id)
    session.add(workspace_user)
    session.commit()
    
    return {"message": "User assigned to workspace successfully"}

# ========== TASK ENDPOINTS ==========

@app.post("/tasks", response_model=Task)
def create_task(task: Task, session: Session = Depends(get_session)):
    """Create a new task"""
    # Verify workspace exists
    workspace = session.get(Workspace, task.workspace_id)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    if not task.title or len(task.title.strip()) < 3:
        raise HTTPException(
            status_code=400, 
            detail="Task title must be at least 3 characters long"
        )
    
    # Clean the data
    task.title = task.title.strip()
    if task.description:
        task.description = task.description.strip()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.get("/tasks", response_model=List[Task])
def get_tasks(workspaceId: int, session: Session = Depends(get_session)):
    """Get tasks for a specific workspace"""
    tasks = session.exec(
        select(Task).where(Task.workspace_id == workspaceId)
    ).all()
    return tasks

@app.patch("/tasks/{task_id}")
def mark_task_complete(task_id: int, session: Session = Depends(get_session)):
    """Mark a task as completed"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.completed = True
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

# ========== SUMMARY ENDPOINT ==========

@app.get("/summary")
def get_summary(session: Session = Depends(get_session)):
    """Get summary of users, workspaces, and tasks"""
    # Count users
    users_count = len(session.exec(select(User)).all())
    
    # Count workspaces
    workspaces_count = len(session.exec(select(Workspace)).all())
    
    # Count tasks
    all_tasks = session.exec(select(Task)).all()
    total_tasks = len(all_tasks)
    completed_tasks = sum(1 for task in all_tasks if task.completed)
    pending_tasks = total_tasks - completed_tasks
    
    return {
        "users": users_count,
        "workspaces": workspaces_count,
        "tasks": {
            "total": total_tasks,
            "completed": completed_tasks,
            "pending": pending_tasks
        }
    }