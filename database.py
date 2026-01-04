"""
Database module for PostgreSQL connection and table management.

This module handles:
- Database connection setup
- Table creation
- Session management
"""

from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

class TaskDB(SQLModel, table=True):
    """
    Database model for Task table.
    
    This maps to the 'taskdb' table in PostgreSQL.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    content: str
    status: str = "Todo"

# Database connection - update with your PostgreSQL credentials
DATABASE_URL = "postgresql://postgres:1980@localhost/taskmanager"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a database session for FastAPI dependency injection."""
    with Session(engine) as session:
        yield session

def get_session_context():
    """Get a database session for CLI context manager usage."""
    return Session(engine)
