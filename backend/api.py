import os
import asyncio
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from dotenv import load_dotenv
import logging
import jwt
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the existing RAG agent functionality
from agent import RAGAgent

# Create FastAPI app
app = FastAPI(
    title="RAG Agent API",
    description="API for RAG Agent with document retrieval and question answering",
    version="1.0.0"
)

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET", "fallback-secret-change-this")
JWT_ALGORITHM = "HS256"

def verify_token(token: str = None):
    """Verify JWT token and return user info if valid"""
    if not token:
        return None

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token has expired")
        return None
    except jwt.InvalidTokenError:
        logger.warning("Invalid token")
        return None

async def get_current_user(request: Request):
    """Get current user from request headers"""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    token = auth_header.replace("Bearer ", "")
    user = verify_token(token)
    return user

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: Add custom authentication middleware to work with BetterAuth
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Middleware to check authentication status from BetterAuth"""
    # Check if user is authenticated via BetterAuth session
    session_cookie = request.cookies.get("better-auth.session_token")
    if session_cookie:
        # In a real implementation, you'd verify this token with BetterAuth API
        # For now, we'll just add a placeholder for authenticated user
        request.state.user = {"id": "authenticated_user", "email": "user@example.com"}
    else:
        request.state.user = None

    response = await call_next(request)
    return response

# Pydantic models
class QueryRequest(BaseModel):
    query: str

class MatchedChunk(BaseModel):
    content: str
    url: str
    position: int
    similarity_score: float

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    matched_chunks: List[MatchedChunk]
    error: Optional[str] = None
    status: str  # "success", "error", "empty"
    query_time_ms: Optional[float] = None
    confidence: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str

# Global RAG agent instance
rag_agent = None

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG agent on startup"""
    global rag_agent
    logger.info("Initializing RAG Agent...")
    try:
        rag_agent = RAGAgent()
        logger.info("RAG Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize RAG Agent: {e}")
        raise

@app.post("/ask", response_model=QueryResponse)
async def ask_rag(request: QueryRequest, current_user=Depends(get_current_user)):
    """
    Process a user query through the RAG agent and return the response
    """
    # Check if user is authenticated (for premium features)
    is_authenticated = current_user is not None

    logger.info(f"Processing query (authenticated: {is_authenticated}): {request.query[:50]}...")

    try:
        # Validate input
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if len(request.query) > 2000:
            raise HTTPException(status_code=400, detail="Query too long, maximum 2000 characters")

        # Optional: Different behavior for authenticated users
        if not is_authenticated:
            logger.info("Unauthenticated user - may have limited access in production")

        # Process query through RAG agent
        response = rag_agent.query_agent(request.query)

        # Format response
        formatted_response = QueryResponse(
            answer=response.get("answer", ""),
            sources=response.get("sources", []),
            matched_chunks=[
                MatchedChunk(
                    content=chunk.get("content", ""),
                    url=chunk.get("url", ""),
                    position=chunk.get("position", 0),
                    similarity_score=chunk.get("similarity_score", 0.0)
                )
                for chunk in response.get("matched_chunks", [])
            ],
            error=response.get("error"),
            status="error" if response.get("error") else "success",
            query_time_ms=response.get("query_time_ms"),
            confidence=response.get("confidence")
        )

        logger.info(f"Query processed successfully in {response.get('query_time_ms', 0):.2f}ms")
        return formatted_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return QueryResponse(
            answer="",
            sources=[],
            matched_chunks=[],
            error=str(e),
            status="error"
        )

class AuthStatusResponse(BaseModel):
    authenticated: bool
    user: Optional[Dict] = None
    message: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    """
    return HealthResponse(
        status="healthy",
        message="RAG Agent API is running"
    )

@app.get("/auth-status", response_model=AuthStatusResponse)
async def auth_status(current_user=Depends(get_current_user)):
    """
    Check authentication status
    """
    if current_user:
        return AuthStatusResponse(
            authenticated=True,
            user=current_user,
            message="User is authenticated"
        )
    else:
        return AuthStatusResponse(
            authenticated=False,
            message="User is not authenticated"
        )

# For running with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)