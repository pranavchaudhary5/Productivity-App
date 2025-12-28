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
        
        Attributes:
            storage (list): In-memory storage of task objects
            i (int): Counter for generating task IDs
        """
        self.storage = []
        self.i = 0

    # ===== SEARCH METHODS =====
    
    def search_by_id(self, u):
        """
        Search for a task by its ID.
        
        Args:
            u (int): Task ID to search for
            
        Returns:
            task: Task object if found, None otherwise
        """
        for tt in self.storage:
            if tt.id == u:
                return tt
        return None

    def search_by_name(self, name):
        """
        Search for tasks by name.
        
        Args:
            name (str): Task name to search for (exact match)
            
        Returns:
            list: List of task objects matching the name
        """
        byname = []
        for t in self.storage:
            if t.name == name:
                byname.append(t)
        return byname

    # ===== CRUD METHODS =====
    
    def add_task(self, name, content):
        """
        Create and add a new task.
        
        Validates name and content before creation.
        Auto-increments task ID.
        
        Args:
            name (str): Task name (1-50 characters)
            content (str): Task description (1-500 characters)
            
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
        
        self.i = self.i + 1
        new_task = task()
        new_task.set(self.i, name, content)
        self.storage.append(new_task)
        
        task_schema = TaskSchema(id=new_task.id, name=new_task.name, content=new_task.content, status=new_task.status)
        return OperationResponse(success=True, message="Task added successfully", data=task_schema)

    def get_all_tasks(self):
        """
        Retrieve all tasks.
        
        Returns:
            TaskListResponse: Always succeeds, returns all tasks (empty list if none)
        """
        tasks_data = [TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status) for t in self.storage]
        return TaskListResponse(success=True, message="Tasks retrieved", data=tasks_data)

    def update_task(self, task_id, new_name=None, new_content=None):
        """
        Update an existing task's name and/or content.
        
        Validates new values before updating.
        At least one of new_name or new_content must be provided.
        
        Args:
            task_id (int): ID of task to update
            new_name (Optional[str]): New task name
            new_content (Optional[str]): New task content
            
        Returns:
            OperationResponse:
                - success=True with updated TaskSchema if successful
                - success=False with error message if task not found or validation fails
        """
        t = self.search_by_id(task_id)
        if t is None:
            return OperationResponse(success=False, message="Task not found")
        
        if new_name:
            name_validation = name_check(new_name)
            if not name_validation.success:
                return OperationResponse(success=False, message=name_validation.message)
            t.name = new_name
        
        if new_content:
            content_validation = content_check(new_content)
            if not content_validation.success:
                return OperationResponse(success=False, message=content_validation.message)
            t.content = new_content
        
        task_schema = TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status)
        return OperationResponse(success=True, message="Task updated successfully", data=task_schema)

    def mark_completed(self, task_id):
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of task to mark as completed
            
        Returns:
            OperationResponse:
                - success=True with updated TaskSchema if successful
                - success=False with error message if task not found or already completed
        """
        t = self.search_by_id(task_id)
        if t is None:
            return OperationResponse(success=False, message="Task not found")
        if t.status == "Completed":
            return OperationResponse(success=False, message="Task is already completed")
        t.status = "Completed"
        task_schema = TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status)
        return OperationResponse(success=True, message="Task marked as completed", data=task_schema)

    def mark_todo(self, task_id):
        """
        Mark a task as to-do.
        
        Args:
            task_id (int): ID of task to mark as to-do
            
        Returns:
            OperationResponse:
                - success=True with updated TaskSchema if successful
                - success=False with error message if task not found or already to-do
        """
        t = self.search_by_id(task_id)
        if t is None:
            return OperationResponse(success=False, message="Task not found")
        if t.status == "Todo":
            return OperationResponse(success=False, message="Task is already marked as to-do")
        t.status = "Todo"
        task_schema = TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status)
        return OperationResponse(success=True, message="Task marked as to-do", data=task_schema)

    def delete_task(self, task_id):
        """
        Delete a task by ID.
        
        Args:
            task_id (int): ID of task to delete
            
        Returns:
            OperationResponse:
                - success=True if deletion successful
                - success=False with error message if task not found
        """
        t = self.search_by_id(task_id)
        if t is None:
            return OperationResponse(success=False, message="Task not found")
        self.storage.remove(t)
        return OperationResponse(success=True, message="Task deleted successfully")

    def get_completed_tasks(self):
        """
        Retrieve all completed tasks.
        
        Returns:
            TaskListResponse: List of all tasks with status "Completed"
        """
        completed = [t for t in self.storage if t.status == "Completed"]
        tasks_data = [TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status) for t in completed]
        if not tasks_data:
            return TaskListResponse(success=True, message="No completed tasks found", data=[])
        return TaskListResponse(success=True, message="Completed tasks retrieved", data=tasks_data)

    def get_todo_tasks(self):
        """
        Retrieve all to-do tasks.
        
        Returns:
            TaskListResponse: List of all tasks with status "Todo"
        """
        todo = [t for t in self.storage if t.status == "Todo"]
        tasks_data = [TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status) for t in todo]
        if not tasks_data:
            return TaskListResponse(success=True, message="No to-do tasks found", data=[])
        return TaskListResponse(success=True, message="To-do tasks retrieved", data=tasks_data)

    def __init__(self):
        self.storage = []
        self.i = 0

    # ===== SEARCH METHODS =====
    def search_by_id(self, u):
        for tt in self.storage:
            if tt.id == u:
                return tt
        return None

    def search_by_name(self, name):
        """Search for tasks by name, returns list of matching tasks"""
        byname = []
        for t in self.storage:
            if t.name == name:
                byname.append(t)
        return byname

    # ===== CRUD METHODS =====
    def add_task(self, name, content):
        """Add a new task. Returns OperationResponse"""
        name_validation = name_check(name)
        if not name_validation.success:
            return OperationResponse(success=False, message=name_validation.message)
        
        content_validation = content_check(content)
        if not content_validation.success:
            return OperationResponse(success=False, message=content_validation.message)
        
        self.i = self.i + 1
        new_task = task()
        new_task.set(self.i, name, content)
        self.storage.append(new_task)
        
        task_schema = TaskSchema(id=new_task.id, name=new_task.name, content=new_task.content, status=new_task.status)
        return OperationResponse(success=True, message="Task added successfully", data=task_schema)

    def get_all_tasks(self):
        """Return all tasks as TaskListResponse"""
        tasks_data = [TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status) for t in self.storage]
        return TaskListResponse(success=True, message="Tasks retrieved", data=tasks_data)

    def update_task(self, task_id, new_name=None, new_content=None):
        """Update task name and/or content. Returns OperationResponse"""
        t = self.search_by_id(task_id)
        if t is None:
            return OperationResponse(success=False, message="Task not found")
        
        if new_name:
            name_validation = name_check(new_name)
            if not name_validation.success:
                return OperationResponse(success=False, message=name_validation.message)
            t.name = new_name
        
        if new_content:
            content_validation = content_check(new_content)
            if not content_validation.success:
                return OperationResponse(success=False, message=content_validation.message)
            t.content = new_content
        
        task_schema = TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status)
        return OperationResponse(success=True, message="Task updated successfully", data=task_schema)

    def mark_completed(self, task_id):
        """Mark task as completed. Returns OperationResponse"""
        t = self.search_by_id(task_id)
        if t is None:
            return OperationResponse(success=False, message="Task not found")
        if t.status == "Completed":
            return OperationResponse(success=False, message="Task is already completed")
        t.status = "Completed"
        task_schema = TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status)
        return OperationResponse(success=True, message="Task marked as completed", data=task_schema)

    def mark_todo(self, task_id):
        """Mark task as to-do. Returns OperationResponse"""
        t = self.search_by_id(task_id)
        if t is None:
            return OperationResponse(success=False, message="Task not found")
        if t.status == "Todo":
            return OperationResponse(success=False, message="Task is already marked as to-do")
        t.status = "Todo"
        task_schema = TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status)
        return OperationResponse(success=True, message="Task marked as to-do", data=task_schema)

    def delete_task(self, task_id):
        """Delete task by ID. Returns OperationResponse"""
        t = self.search_by_id(task_id)
        if t is None:
            return OperationResponse(success=False, message="Task not found")
        self.storage.remove(t)
        return OperationResponse(success=True, message="Task deleted successfully")

    def get_completed_tasks(self):
        """Return all completed tasks as TaskListResponse"""
        completed = [t for t in self.storage if t.status == "Completed"]
        tasks_data = [TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status) for t in completed]
        if not tasks_data:
            return TaskListResponse(success=True, message="No completed tasks found", data=[])
        return TaskListResponse(success=True, message="Completed tasks retrieved", data=tasks_data)

    def get_todo_tasks(self):
        """Return all to-do tasks as TaskListResponse"""
        todo = [t for t in self.storage if t.status == "Todo"]
        tasks_data = [TaskSchema(id=t.id, name=t.name, content=t.content, status=t.status) for t in todo]
        if not tasks_data:
            return TaskListResponse(success=True, message="No to-do tasks found", data=[])
        return TaskListResponse(success=True, message="To-do tasks retrieved", data=tasks_data)
