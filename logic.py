"""
Task Management Business Logic

This module contains the Manager class which handles all CRUD operations
for tasks. It provides clean business logic separated from UI concerns.

The Manager uses Pydantic response models for all return values:
- OperationResponse: Single task operations
- TaskListResponse: List operations

This design makes it easy to integrate with FastAPI or other frameworks.
"""

from model import task, OperationResponse, TaskListResponse, TaskSchema
from validators import name_check, content_check, validate_id
from database import TaskDB, get_session, create_db_and_tables
from sqlmodel import select, Session


class Manager:
    """
    Task management service - handles all business logic.
    
    Responsibilities:
    - Store and manage tasks in memory (self.storage)
    - Provide CRUD operations (Create, Read, Update, Delete)
    - Validate input data
    - Return structured Pydantic responses
    
    Pure business logic - no input/output or UI concerns.
    """

    def __init__(self):
        """
        Initialize the Manager.
        
        Sets up database connection and creates tables if needed.
        """
        # Initialize database on first run
        create_db_and_tables()

    # ===== SEARCH METHODS =====
    
    def search_by_id(self, task_id, session: Session):
        """
        Search for a task by its ID in database.
        
        Args:
            task_id (int): Task ID to search for
            session (Session): Database session
            
        Returns:
            TaskDB: Task object if found, None otherwise
        """
        task = session.get(TaskDB, task_id)
        return task

    def search_by_name(self, name, session: Session):
        """
        Search for tasks by name in database.
        
        Args:
            name (str): Task name to search for (exact match)
            session (Session): Database session
            
        Returns:
            list: List of TaskDB objects matching the name
        """
        tasks = session.exec(select(TaskDB).where(TaskDB.name == name)).all()
        return tasks

    # ===== CRUD METHODS =====
    
    def add_task(self, name, content, session: Session):
        """
        Create and add a new task to database.
        
        Validates name and content before creation.
        Auto-increments task ID via database.
        
        Args:
            name (str): Task name (1-50 characters)
            content (str): Task description (1-500 characters)
            session (Session): Database session
            
        Returns:
            OperationResponse: 
                - success=True with created TaskSchema if successful
                - success=False with error message if validation fails
        """
        name_validation = name_check(name)
        if not name_validation.success:
            return OperationResponse(success=False, message=name_validation.message)
        
        content_validation = content_check(content)
        if not content_validation.success:
            return OperationResponse(success=False, message=content_validation.message)
        
        # Database operation
        new_task = TaskDB(name=name, content=content, status="Todo")
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        
        task_schema = TaskSchema(id=new_task.id, name=new_task.name, content=new_task.content, status=new_task.status)
        return OperationResponse(success=True, message="Task added successfully", data=task_schema)

    def get_all_tasks(self, session: Session):
        """
        Retrieve all tasks from database.
        
        Args:
            session (Session): Database session
            
        Returns:
            TaskListResponse: Always succeeds, returns all tasks (empty list if none)
        """
        tasks = session.exec(select(TaskDB)).all()
        tasks_data = [TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status) for t in tasks]
        return TaskListResponse(success=True, message="Tasks retrieved", data=tasks_data)

    def update_task(self, task_id, new_name=None, new_content=None, session: Session = None):
        """
        Update an existing task's name and/or content in database.
        
        Validates new values before updating.
        At least one of new_name or new_content must be provided.
        
        Args:
            task_id (int): ID of task to update
            new_name (Optional[str]): New task name
            new_content (Optional[str]): New task content
            session (Session): Database session
            
        Returns:
            OperationResponse:
                - success=True with updated TaskSchema if successful
                - success=False with error message if task not found or validation fails
        """
        task = session.get(TaskDB, task_id)
        if task is None:
            return OperationResponse(success=False, message="Task not found")
        
        if new_name:
            name_validation = name_check(new_name)
            if not name_validation.success:
                return OperationResponse(success=False, message=name_validation.message)
            task.name = new_name
        
        if new_content:
            content_validation = content_check(new_content)
            if not content_validation.success:
                return OperationResponse(success=False, message=content_validation.message)
            task.content = new_content
        
        session.commit()
        session.refresh(task)
        
        task_schema = TaskSchema(id=task.id, name=task.name, content=task.content, status=task.status)
        return OperationResponse(success=True, message="Task updated successfully", data=task_schema)

    def mark_completed(self, task_id, session: Session):
        """
        Mark a task as completed in database.
        
        Args:
            task_id (int): ID of task to mark as completed
            session (Session): Database session
            
        Returns:
            OperationResponse:
                - success=True with updated TaskSchema if successful
                - success=False with error message if task not found or already completed
        """
        task = session.get(TaskDB, task_id)
        if task is None:
            return OperationResponse(success=False, message="Task not found")
        if task.status == "Completed":
            return OperationResponse(success=False, message="Task is already completed")
        
        task.status = "Completed"
        session.commit()
        session.refresh(task)
        
        task_schema = TaskSchema(id=task.id, name=task.name, content=task.content, status=task.status)
        return OperationResponse(success=True, message="Task marked as completed", data=task_schema)

    def mark_todo(self, task_id, session: Session):
        """
        Mark a task as to-do in database.
        
        Args:
            task_id (int): ID of task to mark as to-do
            session (Session): Database session
            
        Returns:
            OperationResponse:
                - success=True with updated TaskSchema if successful
                - success=False with error message if task not found or already to-do
        """
        task = session.get(TaskDB, task_id)
        if task is None:
            return OperationResponse(success=False, message="Task not found")
        if task.status == "Todo":
            return OperationResponse(success=False, message="Task is already marked as to-do")
        
        task.status = "Todo"
        session.commit()
        session.refresh(task)
        
        task_schema = TaskSchema(id=task.id, name=task.name, content=task.content, status=task.status)
        return OperationResponse(success=True, message="Task marked as to-do", data=task_schema)

    def delete_task(self, task_id, session: Session):
        """
        Delete a task by ID from database.
        
        Args:
            task_id (int): ID of task to delete
            session (Session): Database session
            
        Returns:
            OperationResponse:
                - success=True if deletion successful
                - success=False with error message if task not found
        """
        task = session.get(TaskDB, task_id)
        if task is None:
            return OperationResponse(success=False, message="Task not found")
        
        session.delete(task)
        session.commit()
        return OperationResponse(success=True, message="Task deleted successfully")

    def get_completed_tasks(self, session: Session):
        """
        Retrieve all completed tasks from database.
        
        Args:
            session (Session): Database session
            
        Returns:
            TaskListResponse: List of all tasks with status "Completed"
        """
        tasks = session.exec(select(TaskDB).where(TaskDB.status == "Completed")).all()
        tasks_data = [TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status) for t in tasks]
        if not tasks_data:
            return TaskListResponse(success=True, message="No completed tasks found", data=[])
        return TaskListResponse(success=True, message="Completed tasks retrieved", data=tasks_data)

    def get_todo_tasks(self, session: Session):
        """
        Retrieve all to-do tasks from database.
        
        Args:
            session (Session): Database session
            
        Returns:
            TaskListResponse: List of all tasks with status "Todo"
        """
        tasks = session.exec(select(TaskDB).where(TaskDB.status == "Todo")).all()
        tasks_data = [TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status) for t in tasks]
        if not tasks_data:
            return TaskListResponse(success=True, message="No to-do tasks found", data=[])
        return TaskListResponse(success=True, message="To-do tasks retrieved", data=tasks_data)

    
