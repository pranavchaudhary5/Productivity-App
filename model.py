"""
Task Management Data Models

This module contains:
- Task: Legacy task model (will be migrated to Pydantic)
- Pydantic response models for API responses:
  - TaskSchema: Represents task data
  - ValidationResponse: Response from validation operations
  - OperationResponse: Response from CRUD operations
  - TaskListResponse: Response from list operations
"""

from pydantic import BaseModel
from typing import Optional, List


class task:
    """
    Legacy Task model - represents a single task.
    
    Attributes:
        id (int): Unique identifier for the task
        name (str): Task name
        content (str): Task description
        status (str): Current status ("Todo" or "Completed")
    """
    def __init__(self):
        self.id = None
        self.name = None
        self.content = None
        self.status = None

    def set(self, num, name, content):
        """
        Initialize task with values.
        
        Args:
            num (int): Task ID
            name (str): Task name
            content (str): Task description
        """
        self.id = num
        self.name = name
        self.content = content
        self.status = "Todo"

    def __repr__(self):
        return f"Task(id={self.id}, name={self.name!r}, status={self.status!r} content={self.content!r})"

    def __str__(self):
        return f"{self.name} [{self.id}]"


# ===== PYDANTIC RESPONSE MODELS =====

class TaskSchema(BaseModel):
    """
    Pydantic model for task data serialization.
    
    Used for:
    - API responses
    - JSON serialization
    - Type validation
    
    Attributes:
        id (Optional[int]): Task unique identifier
        name (str): Task name (required)
        content (str): Task description (required)
        status (str): Task status - "Todo" or "Completed" (default: "Todo")
    """
    id: Optional[int] = None
    name: str
    content: str
    status: str = "Todo"

    class Config:
        from_attributes = True


class ValidationResponse(BaseModel):
    """
    Response model for validation operations.
    
    Used by validators module to indicate validation success/failure.
    
    Attributes:
        success (bool): Whether validation passed
        message (Optional[str]): Error message if validation failed
        data (Optional): Validated data (e.g., parsed ID)
    """
    success: bool
    message: Optional[str] = None
    data: Optional[int] = None


class OperationResponse(BaseModel):
    """
    Response model for single-task operations (CRUD).
    
    Used by Manager methods to return operation status and resulting task data.
    
    Attributes:
        success (bool): Whether operation succeeded
        message (str): Operation result message
        data (Optional[TaskSchema]): Resulting task data if successful
    """
    success: bool
    message: str
    data: Optional[TaskSchema] = None


class TaskListResponse(BaseModel):
    """
    Response model for list operations.
    
    Used by Manager methods that return multiple tasks (get_all, get_completed, etc).
    
    Attributes:
        success (bool): Whether operation succeeded
        message (str): Operation result message
        data (List[TaskSchema]): List of tasks (empty if none found)
    """
    success: bool
    message: str
    data: List[TaskSchema] = []
