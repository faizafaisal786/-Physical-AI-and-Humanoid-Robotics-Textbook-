"""
Pydantic schemas for authentication requests and responses
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response (without sensitive data)"""
    id: int
    is_active: bool
    is_verified: bool
    is_admin: bool
    created_at: datetime
    last_login: Optional[datetime]

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    username: Optional[str] = None
    full_name: Optional[str] = None


class PasswordChange(BaseModel):
    """Schema for password change"""
    old_password: str
    new_password: str = Field(..., min_length=8)

    @field_validator('new_password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


# Token schemas
class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenRefresh(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str


class AccessTokenResponse(BaseModel):
    """Schema for access token only response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Authentication response schemas
class AuthResponse(BaseModel):
    """Schema for authentication response (login/signup)"""
    user: UserResponse
    tokens: TokenResponse
    message: str


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    error_code: Optional[str] = None


# Product schemas
class Product(BaseModel):
    """Product model"""
    id: int
    name: str
    price: float = Field(gt=0, description="Price must be positive")
    category: str
    created_at: str
    in_stock: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Laptop",
                "price": 999.99,
                "category": "Electronics",
                "created_at": "2025-01-15T10:30:00Z",
                "in_stock": True
            }
        }


class PaginationMetadata(BaseModel):
    """Pagination metadata for cursor-based navigation"""
    limit: int
    next_cursor: Optional[str] = None
    has_next: bool
    count: int = Field(description="Number of items in current response")


class ProductsResponse(BaseModel):
    """Paginated products response"""
    data: List[Product]
    pagination: PaginationMetadata


# Task schemas
class TaskBase(BaseModel):
    """Base task schema"""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    task_type: str = Field(default="study", pattern="^(study|exercise|quiz|review|reading|practice)$")
    priority: str = Field(default="medium", pattern="^(low|medium|high|urgent)$")
    chapter_id: Optional[str] = None
    topic: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    estimated_duration: Optional[int] = Field(None, gt=0, description="Duration in minutes")


class TaskCreate(TaskBase):
    """Schema for creating a task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    task_type: Optional[str] = Field(None, pattern="^(study|exercise|quiz|review|reading|practice)$")
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|completed|cancelled)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|urgent)$")
    chapter_id: Optional[str] = None
    topic: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    estimated_duration: Optional[int] = Field(None, gt=0)
    completion_notes: Optional[str] = None


class TaskResponse(TaskBase):
    """Schema for task response"""
    id: int
    user_id: int
    status: str
    is_ai_generated: bool
    completed_at: Optional[datetime]
    completion_notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for list of tasks"""
    tasks: List[TaskResponse]
    total: int
    completed: int
    pending: int
    in_progress: int


class AITaskGenerateRequest(BaseModel):
    """Schema for AI task generation request"""
    topic: Optional[str] = None
    chapter_id: Optional[str] = None
    difficulty: str = Field(default="medium", pattern="^(easy|medium|hard)$")
    count: int = Field(default=3, ge=1, le=10)
    task_types: Optional[List[str]] = None


class AITaskGenerateResponse(BaseModel):
    """Schema for AI task generation response"""
    tasks: List[TaskResponse]
    count: int
    message: str


class ProgressResponse(BaseModel):
    """Schema for learning progress response"""
    total_tasks: int
    completed_tasks: int
    completion_percentage: float
    tasks_by_type: dict
    tasks_by_status: dict
    recent_completions: List[TaskResponse]
    upcoming_tasks: List[TaskResponse]
