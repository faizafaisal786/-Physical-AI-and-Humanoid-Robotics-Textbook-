"""
Authentication routes (signup, login, logout, refresh, etc.)
Following modern authentication patterns similar to BetterAuth
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from database import get_db
from models import User, Session as DBSession
from schemas import (
    UserCreate, UserLogin, UserResponse, AuthResponse,
    TokenResponse, TokenRefresh, AccessTokenResponse,
    MessageResponse, PasswordChange, UserUpdate
)
from auth_utils import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    verify_refresh_token, get_token_expiration,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_client_info(request: Request) -> tuple[Optional[str], Optional[str]]:
    """Extract client IP and user agent from request"""
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent", None)
    return ip_address, user_agent


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account with email and password"
)
async def signup(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db)
) -> AuthResponse:
    """
    Register a new user with email and password

    **Requirements:**
    - Unique email address
    - Password: min 8 chars, 1 uppercase, 1 lowercase, 1 digit

    **Returns:**
    - User profile
    - Access token (30 min expiry)
    - Refresh token (30 days expiry)
    """

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check username uniqueness if provided
    if user_data.username:
        existing_username = db.query(User).filter(User.username == user_data.username).first()
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

    # Create new user
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_pwd,
        created_at=datetime.utcnow(),
        last_login=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate tokens
    token_data = {"sub": str(new_user.id), "email": new_user.email}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"sub": str(new_user.id)})

    # Create session
    ip_address, user_agent = get_client_info(request)
    session = DBSession(
        user_id=new_user.id,
        refresh_token=refresh_token,
        ip_address=ip_address,
        user_agent=user_agent,
        expires_at=get_token_expiration("refresh")
    )

    db.add(session)
    db.commit()

    # Build response
    return AuthResponse(
        user=UserResponse.model_validate(new_user),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
        message="Account created successfully"
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login user",
    description="Authenticate user with email and password"
)
async def login(
    credentials: UserLogin,
    request: Request,
    db: Session = Depends(get_db)
) -> AuthResponse:
    """
    Login with email and password

    **Returns:**
    - User profile
    - Access token (30 min expiry)
    - Refresh token (30 days expiry)
    """

    # Find user by email
    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )

    # Update last login
    user.last_login = datetime.utcnow()

    # Generate tokens
    token_data = {"sub": str(user.id), "email": user.email}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"sub": str(user.id)})

    # Create new session
    ip_address, user_agent = get_client_info(request)
    session = DBSession(
        user_id=user.id,
        refresh_token=refresh_token,
        ip_address=ip_address,
        user_agent=user_agent,
        expires_at=get_token_expiration("refresh")
    )

    db.add(session)
    db.commit()

    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        ),
        message="Login successful"
    )


@router.post(
    "/refresh",
    response_model=AccessTokenResponse,
    summary="Refresh access token",
    description="Get new access token using refresh token"
)
async def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
) -> AccessTokenResponse:
    """
    Refresh access token using refresh token

    **Requirements:**
    - Valid refresh token

    **Returns:**
    - New access token
    """

    # Verify refresh token
    payload = verify_refresh_token(token_data.refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )

    # Check if session exists and is active
    session = db.query(DBSession).filter(
        DBSession.refresh_token == token_data.refresh_token,
        DBSession.is_active == True
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session not found or inactive"
        )

    # Check if session is expired
    if session.expires_at < datetime.utcnow():
        session.is_active = False
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )

    # Get user
    user = db.query(User).filter(User.id == session.user_id).first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    # Update session last used
    session.last_used = datetime.utcnow()
    db.commit()

    # Generate new access token
    token_data = {"sub": str(user.id), "email": user.email}
    access_token = create_access_token(token_data)

    return AccessTokenResponse(
        access_token=access_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout user",
    description="Invalidate current session and refresh token"
)
async def logout(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
) -> MessageResponse:
    """
    Logout user by invalidating the session

    **Requirements:**
    - Valid refresh token

    **Returns:**
    - Success message
    """

    # Find and deactivate session
    session = db.query(DBSession).filter(
        DBSession.refresh_token == token_data.refresh_token
    ).first()

    if session:
        session.is_active = False
        db.commit()

    return MessageResponse(
        message="Logged out successfully",
        success=True
    )


@router.post(
    "/logout-all",
    response_model=MessageResponse,
    summary="Logout from all devices",
    description="Invalidate all sessions for the user"
)
async def logout_all(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
) -> MessageResponse:
    """
    Logout from all devices by invalidating all user sessions

    **Requirements:**
    - Valid refresh token

    **Returns:**
    - Success message
    """

    # Verify token and get user
    payload = verify_refresh_token(token_data.refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = int(payload.get("sub"))

    # Deactivate all user sessions
    db.query(DBSession).filter(DBSession.user_id == user_id).update({"is_active": False})
    db.commit()

    return MessageResponse(
        message="Logged out from all devices successfully",
        success=True
    )


@router.get(
    "/sessions",
    summary="Get active sessions",
    description="List all active sessions for the authenticated user"
)
async def get_sessions(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """Get all active sessions for the user"""

    payload = verify_refresh_token(token_data.refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = int(payload.get("sub"))

    sessions = db.query(DBSession).filter(
        DBSession.user_id == user_id,
        DBSession.is_active == True
    ).all()

    return {
        "sessions": [
            {
                "id": s.id,
                "ip_address": s.ip_address,
                "user_agent": s.user_agent,
                "created_at": s.created_at,
                "last_used": s.last_used,
                "expires_at": s.expires_at
            }
            for s in sessions
        ]
    }
