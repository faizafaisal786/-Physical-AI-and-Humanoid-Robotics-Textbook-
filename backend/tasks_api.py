"""
Task Management API Routes
Provides CRUD operations for user tasks and AI-powered task generation
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import Optional, List
import json

from database import get_db
from models import Task, User, TaskType, TaskStatus, TaskPriority
from schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    AITaskGenerateRequest, AITaskGenerateResponse, ProgressResponse,
    MessageResponse
)
from dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task"
)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Create a new task for the authenticated user

    **Requirements:**
    - Valid authentication token
    - Task title (required)

    **Returns:**
    - Created task object
    """
    # Convert task_type string to enum
    task_type = TaskType[task_data.task_type.upper()]
    priority = TaskPriority[task_data.priority.upper()]

    # Create new task
    new_task = Task(
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        task_type=task_type,
        priority=priority,
        chapter_id=task_data.chapter_id,
        topic=task_data.topic,
        tags=json.dumps(task_data.tags) if task_data.tags else None,
        due_date=task_data.due_date,
        estimated_duration=task_data.estimated_duration,
        status=TaskStatus.PENDING
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Convert back to response format
    return _task_to_response(new_task)


@router.get(
    "/",
    response_model=TaskListResponse,
    summary="Get all tasks for user"
)
async def get_tasks(
    status_filter: Optional[str] = Query(None, pattern="^(pending|in_progress|completed|cancelled)$"),
    task_type: Optional[str] = Query(None, pattern="^(study|exercise|quiz|review|reading|practice)$"),
    chapter_id: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TaskListResponse:
    """
    Get all tasks for the authenticated user with optional filtering

    **Query Parameters:**
    - status_filter: Filter by task status
    - task_type: Filter by task type
    - chapter_id: Filter by chapter
    - limit: Max number of results (default: 100)
    - offset: Pagination offset (default: 0)

    **Returns:**
    - List of tasks with statistics
    """
    # Build query
    query = db.query(Task).filter(Task.user_id == current_user.id)

    if status_filter:
        query = query.filter(Task.status == TaskStatus[status_filter.upper()])

    if task_type:
        query = query.filter(Task.task_type == TaskType[task_type.upper()])

    if chapter_id:
        query = query.filter(Task.chapter_id == chapter_id)

    # Get total count
    total = query.count()

    # Get statistics
    completed = query.filter(Task.status == TaskStatus.COMPLETED).count()
    pending = query.filter(Task.status == TaskStatus.PENDING).count()
    in_progress = query.filter(Task.status == TaskStatus.IN_PROGRESS).count()

    # Get paginated tasks
    tasks = query.order_by(Task.created_at.desc()).offset(offset).limit(limit).all()

    return TaskListResponse(
        tasks=[_task_to_response(task) for task in tasks],
        total=total,
        completed=completed,
        pending=pending,
        in_progress=in_progress
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID"
)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Get a specific task by ID

    **Requirements:**
    - Task must belong to authenticated user

    **Returns:**
    - Task object
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return _task_to_response(task)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update task"
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TaskResponse:
    """
    Update a task

    **Requirements:**
    - Task must belong to authenticated user

    **Returns:**
    - Updated task object
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update fields
    update_data = task_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        if field == "task_type" and value:
            setattr(task, field, TaskType[value.upper()])
        elif field == "status" and value:
            setattr(task, field, TaskStatus[value.upper()])
            # Set completed_at if status is completed
            if value.upper() == "COMPLETED" and not task.completed_at:
                task.completed_at = datetime.utcnow()
        elif field == "priority" and value:
            setattr(task, field, TaskPriority[value.upper()])
        elif field == "tags" and value:
            setattr(task, field, json.dumps(value))
        else:
            setattr(task, field, value)

    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)

    return _task_to_response(task)


@router.delete(
    "/{task_id}",
    response_model=MessageResponse,
    summary="Delete task"
)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> MessageResponse:
    """
    Delete a task

    **Requirements:**
    - Task must belong to authenticated user

    **Returns:**
    - Success message
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return MessageResponse(
        message="Task deleted successfully",
        success=True
    )


@router.post(
    "/ai-generate",
    response_model=AITaskGenerateResponse,
    summary="Generate tasks using AI"
)
async def generate_ai_tasks(
    request: AITaskGenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> AITaskGenerateResponse:
    """
    Generate study tasks using AI based on topic/chapter

    **Requirements:**
    - Valid authentication token
    - Topic or chapter_id

    **Returns:**
    - List of generated tasks
    """
    from enhanced_rag import generate_study_tasks

    try:
        # Generate tasks using AI
        generated_tasks_data = await generate_study_tasks(
            topic=request.topic,
            chapter_id=request.chapter_id,
            difficulty=request.difficulty,
            count=request.count,
            task_types=request.task_types
        )

        # Create tasks in database
        created_tasks = []
        for task_data in generated_tasks_data:
            task = Task(
                user_id=current_user.id,
                title=task_data["title"],
                description=task_data.get("description"),
                task_type=TaskType[task_data.get("task_type", "STUDY").upper()],
                priority=TaskPriority[task_data.get("priority", "MEDIUM").upper()],
                chapter_id=request.chapter_id,
                topic=request.topic,
                estimated_duration=task_data.get("estimated_duration"),
                status=TaskStatus.PENDING,
                is_ai_generated=True,
                ai_context=json.dumps({
                    "difficulty": request.difficulty,
                    "generation_date": datetime.utcnow().isoformat()
                })
            )
            db.add(task)
            created_tasks.append(task)

        db.commit()

        # Refresh all tasks
        for task in created_tasks:
            db.refresh(task)

        return AITaskGenerateResponse(
            tasks=[_task_to_response(task) for task in created_tasks],
            count=len(created_tasks),
            message=f"Successfully generated {len(created_tasks)} AI-powered study tasks"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate tasks: {str(e)}"
        )


@router.get(
    "/progress/overview",
    response_model=ProgressResponse,
    summary="Get learning progress overview"
)
async def get_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ProgressResponse:
    """
    Get comprehensive learning progress overview

    **Returns:**
    - Statistics about tasks and learning progress
    """
    # Get all tasks
    all_tasks = db.query(Task).filter(Task.user_id == current_user.id).all()

    total_tasks = len(all_tasks)
    completed_tasks = len([t for t in all_tasks if t.status == TaskStatus.COMPLETED])

    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0

    # Tasks by type
    tasks_by_type = {}
    for task_type in TaskType:
        count = len([t for t in all_tasks if t.task_type == task_type])
        tasks_by_type[task_type.value] = count

    # Tasks by status
    tasks_by_status = {}
    for task_status in TaskStatus:
        count = len([t for t in all_tasks if t.status == task_status])
        tasks_by_status[task_status.value] = count

    # Recent completions (last 5)
    recent_completions = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status == TaskStatus.COMPLETED
    ).order_by(Task.completed_at.desc()).limit(5).all()

    # Upcoming tasks (next 5 by due date)
    upcoming_tasks = db.query(Task).filter(
        Task.user_id == current_user.id,
        Task.status.in_([TaskStatus.PENDING, TaskStatus.IN_PROGRESS]),
        Task.due_date.isnot(None)
    ).order_by(Task.due_date.asc()).limit(5).all()

    return ProgressResponse(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        completion_percentage=round(completion_percentage, 2),
        tasks_by_type=tasks_by_type,
        tasks_by_status=tasks_by_status,
        recent_completions=[_task_to_response(t) for t in recent_completions],
        upcoming_tasks=[_task_to_response(t) for t in upcoming_tasks]
    )


# Helper function to convert Task model to TaskResponse
def _task_to_response(task: Task) -> TaskResponse:
    """Convert Task model to TaskResponse schema"""
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        task_type=task.task_type.value,
        status=task.status.value,
        priority=task.priority.value,
        chapter_id=task.chapter_id,
        topic=task.topic,
        tags=json.loads(task.tags) if task.tags else None,
        due_date=task.due_date,
        estimated_duration=task.estimated_duration,
        is_ai_generated=task.is_ai_generated,
        completed_at=task.completed_at,
        completion_notes=task.completion_notes,
        created_at=task.created_at,
        updated_at=task.updated_at
    )
