"""
Input Validation Module

This module provides validation functions for task inputs:
- name_check: Validates task name length and format
- content_check: Validates task content/description length and format
- validate_id: Validates and converts task ID to integer

All functions return ValidationResponse Pydantic models.
"""

from model import ValidationResponse


def name_check(text):
    """
    Validate task name.
    
    Rules:
    - Must be between 1 and 50 characters
    - Cannot be empty
    
    Args:
        text (str): Task name to validate
        
    Returns:
        ValidationResponse: success=True if valid, False with error message otherwise
    """
    if len(text) > 50 or len(text) < 1 or not text:
        return ValidationResponse(success=False, message="Error: Task name must be between 1 and 50 characters.")
    return ValidationResponse(success=True)


def content_check(text):
    """
    Validate task content/description.
    
    Rules:
    - Must be between 1 and 500 characters
    - Cannot be empty
    
    Args:
        text (str): Task content to validate
        
    Returns:
        ValidationResponse: success=True if valid, False with error message otherwise
    """
    if len(text) > 500 or len(text) < 1 or not text:
        return ValidationResponse(success=False, message="Error: Description must be between 1 and 500 characters.")
    return ValidationResponse(success=True)


def validate_id(u):
    """
    Validate and parse task ID.
    
    Rules:
    - Must be convertible to integer
    
    Args:
        u (str): Task ID string to validate and parse
        
    Returns:
        ValidationResponse: success=True with parsed ID in data field, 
                           False with error message if invalid format
    """
    try:
        userid = int(u)
        return ValidationResponse(success=True, data=userid)
    except (ValueError, TypeError):
        return ValidationResponse(success=False, message="Error: Invalid ID format. Please enter a valid numeric ID.")
