"""
FastAPI Web Application for Task Manager

This module provides HTTP endpoints for the task management system.
It uses the existing Manager class from logic.py without any modifications.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from logic import Manager
from model import TaskSchema, OperationResponse, TaskListResponse

app = FastAPI(title="Task Manager API", description="REST API for managing tasks")
manager = Manager()

@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    pass  # Manager.__init__ already creates tables

@app.post("/tasks/", response_model=OperationResponse)
def create_task(name: str, content: str, session: Session = Depends(get_session)):
    """Create a new task."""
    try:
        return manager.add_task(name, content, session)
    except Exception as e:
        return OperationResponse(success=False, message=str(e))

@app.get("/tasks/", response_model=TaskListResponse)
def get_all_tasks(session: Session = Depends(get_session)):
    """Get all tasks."""
    try:
        return manager.get_all_tasks(session)
    except Exception as e:
        return TaskListResponse(success=False, message=str(e))

@app.get("/tasks/{task_id}", response_model=OperationResponse)
def get_task(task_id: int, session: Session = Depends(get_session)):
    """Get a specific task by ID."""
    task = manager.search_by_id(task_id, session)
    if not task:
        return OperationResponse(success=False, message="Task not found")
    return OperationResponse(success=True, data=TaskSchema.from_orm(task))

@app.put("/tasks/{task_id}", response_model=OperationResponse)
def update_task(task_id: int, name: str = None, content: str = None, session: Session = Depends(get_session)):
    """Update a task."""
    return manager.update_task(task_id, name, content, session)

@app.delete("/tasks/{task_id}", response_model=OperationResponse)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Delete a task."""
    return manager.delete_task(task_id, session)

@app.patch("/tasks/{task_id}/complete", response_model=OperationResponse)
def mark_task_completed(task_id: int, session: Session = Depends(get_session)):
    """Mark a task as completed."""
    return manager.mark_completed(task_id, session)

@app.patch("/tasks/{task_id}/todo", response_model=OperationResponse)
def mark_task_todo(task_id: int, session: Session = Depends(get_session)):
    """Mark a task as to-do."""
    return manager.mark_todo(task_id, session)

@app.get("/tasks/completed/", response_model=TaskListResponse)
def get_completed_tasks(session: Session = Depends(get_session)):
    """Get all completed tasks."""
    return manager.get_completed_tasks(session)

@app.get("/tasks/todo/", response_model=TaskListResponse)
def get_todo_tasks(session: Session = Depends(get_session)):
    """Get all to-do tasks."""
    return manager.get_todo_tasks(session)

@app.get("/tasks/by-name/{name}", response_model=TaskListResponse)
def get_tasks_by_name(name: str, session: Session = Depends(get_session)):
    """Get tasks by name."""
    tasks = manager.search_by_name(name, session)
    tasks_data = [TaskSchema.from_orm(t) for t in tasks]
    return TaskListResponse(success=True, message="Tasks retrieved", data=tasks_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
