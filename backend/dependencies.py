"""
FastAPI dependencies for authentication and authorization
Use these to protect routes and get current user
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models import User
from auth_utils import verify_access_token

# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token

    **Usage:**
    ```python
    @app.get("/protected")
    async def protected_route(current_user: User = Depends(get_current_user)):
        return {"user_id": current_user.id}
    ```

    **Args:**
        credentials: HTTP Bearer token from Authorization header
        db: Database session

    **Returns:**
        Current authenticated user

    **Raises:**
        HTTPException 401: If token is invalid or user not found
    """

    # Extract token from credentials
    token = credentials.credentials

    # Verify token
    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Get user ID from token
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Get user from database
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current active user

    **Usage:**
    ```python
    @app.get("/protected")
    async def protected_route(user: User = Depends(get_current_active_user)):
        return {"user": user.email}
    ```
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current verified user (email verified)

    **Usage:**
    ```python
    @app.post("/sensitive-action")
    async def sensitive_action(user: User = Depends(get_current_verified_user)):
        # Only verified users can access
        return {"status": "ok"}
    ```
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email verification required"
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current admin user

    **Usage:**
    ```python
    @app.delete("/admin/users/{user_id}")
    async def delete_user(
        user_id: int,
        admin: User = Depends(get_current_admin_user)
    ):
        # Only admins can access
        return {"deleted": user_id}
    ```
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to optionally get current user (doesn't fail if no token)

    **Usage:**
    ```python
    @app.get("/public-or-private")
    async def mixed_route(user: Optional[User] = Depends(get_optional_current_user)):
        if user:
            return {"message": f"Hello {user.email}"}
        return {"message": "Hello guest"}
    ```
    """
    if not credentials:
        return None

    token = credentials.credentials
    payload = verify_access_token(token)

    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user or not user.is_active:
        return None

    return user
