from typing import Optional
from sqlmodel import SQLModel, Field, create_engine, Session
from pydantic import field_validator

# User Model with strict validation
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v:
            raise ValueError('Name is required')
        v = v.strip()
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters long')
        if len(v) > 100:
            raise ValueError('Name must not exceed 100 characters')
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email is required')
        v = v.strip()
        if '@' not in v or '.' not in v:
            raise ValueError('Invalid email format')
        if len(v) > 100:
            raise ValueError('Email must not exceed 100 characters')
        return v

# Workspace Model with strict validation
class Workspace(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v:
            raise ValueError('Workspace name is required')
        v = v.strip()
        if len(v) < 2:
            raise ValueError('Workspace name must be at least 2 characters long')
        if len(v) > 100:
            raise ValueError('Workspace name must not exceed 100 characters')
        return v
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v and len(v) > 500:
            raise ValueError('Description must not exceed 500 characters')
        return v

# WorkspaceUser Model (for assigning users to workspaces)
class WorkspaceUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    workspace_id: int = Field(foreign_key="workspace.id")
    user_id: int = Field(foreign_key="user.id")

# Task Model with strict validation
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    workspace_id: int = Field(foreign_key="workspace.id")
    completed: bool = False
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        if not v:
            raise ValueError('Task title is required')
        v = v.strip()
        if len(v) < 3:
            raise ValueError('Task title must be at least 3 characters long')
        if len(v) > 200:
            raise ValueError('Task title must not exceed 200 characters')
        return v
    
    @field_validator('description')
    @classmethod
    def validate_description(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must not exceed 1000 characters')
        return v

# Database setup
SQLITE_URL = "sqlite:///workspace.db"
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session