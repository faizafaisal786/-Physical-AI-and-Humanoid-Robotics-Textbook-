"""
Main FastAPI application with authentication
Combines Products API with BetterAuth-style authentication system
"""

from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from contextlib import asynccontextmanager

from models import User
from schemas import ProductsResponse, Product, PaginationMetadata, UserResponse
from database import init_db
from dependencies import get_current_user, get_optional_current_user
from auth_routes import router as auth_router
from tasks_api import router as tasks_router
import base64
import json

# Mock products data (same as before)
MOCK_PRODUCTS = [
    Product(id=i, name=f"Product {i}", price=10.0 + i,
            category=["Electronics", "Clothing", "Books", "Home"][i % 4],
            created_at=f"2025-01-{(i % 30) + 1:02d}T10:00:00Z",
            in_stock=i % 3 != 0)
    for i in range(1, 101)
]


def encode_cursor(product_id: int) -> str:
    """Encode cursor for pagination"""
    cursor_data = {'id': product_id}
    cursor_json = json.dumps(cursor_data)
    encoded = base64.b64encode(cursor_json.encode('utf-8')).decode('utf-8')
    return encoded


def decode_cursor(cursor: str) -> int:
    """Decode cursor for pagination"""
    try:
        decoded = base64.b64decode(cursor.encode('utf-8')).decode('utf-8')
        cursor_data = json.loads(decoded)
        product_id = cursor_data.get('id')

        if not isinstance(product_id, int) or product_id < 0:
            raise ValueError("Invalid product ID in cursor")

        return product_id
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid cursor format: {str(e)}"
        )


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    print("Starting application...")
    init_db()
    print("Database initialized successfully")
    yield
    print("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title="Physical AI & Humanoid Robotics API",
    description="Modern API with authentication and intelligent task management",
    version="3.0.0",
    lifespan=lifespan
)

# CORS middleware (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes
app.include_router(auth_router)

# Include tasks routes
app.include_router(tasks_router)


# Root endpoint
@app.get("/", summary="API Info")
async def root():
    """API information and available endpoints"""
    return {
        "message": "Physical AI & Humanoid Robotics API",
        "version": "3.0.0",
        "features": [
            "cursor-based-pagination",
            "jwt-authentication",
            "intelligent-task-management",
            "ai-powered-task-generation"
        ],
        "authentication": {
            "type": "JWT Bearer Token",
            "endpoints": {
                "signup": "POST /auth/signup",
                "login": "POST /auth/login",
                "refresh": "POST /auth/refresh",
                "logout": "POST /auth/logout"
            }
        },
        "endpoints": {
            "products": "GET /products (public)",
            "tasks": "GET /tasks (protected)",
            "ai_tasks": "POST /tasks/ai-generate (protected)",
            "me": "GET /me (protected)",
            "docs": "GET /docs"
        }
    }


# Protected: Get current user profile
@app.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    tags=["User"]
)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """
    Get current authenticated user's profile

    **Requires:** Valid access token in Authorization header
    """
    return UserResponse.model_validate(current_user)


# Public/Protected: Products endpoint (optional auth)
@app.get(
    "/products",
    response_model=ProductsResponse,
    summary="Get paginated products",
    tags=["Products"]
)
async def get_products(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of products to return (1-100)"
    ),
    next_cursor: Optional[str] = Query(
        default=None,
        description="Cursor for next page"
    ),
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> ProductsResponse:
    """
    Get products with cursor-based pagination

    **Authentication:** Optional (better experience for logged-in users)

    **Note:** This endpoint works both with and without authentication.
    Authenticated users may get additional features in future updates.
    """

    # Decode cursor
    last_id = 0
    if next_cursor:
        last_id = decode_cursor(next_cursor)

    # Filter and paginate
    filtered_products = [p for p in MOCK_PRODUCTS if p.id > last_id]
    products_page = filtered_products[:limit + 1]

    has_next = len(products_page) > limit
    products = products_page[:limit]

    next_cursor_value = None
    if has_next and products:
        next_cursor_value = encode_cursor(products[-1].id)

    return ProductsResponse(
        data=products,
        pagination=PaginationMetadata(
            limit=limit,
            next_cursor=next_cursor_value,
            has_next=has_next,
            count=len(products)
        )
    )


# Protected: Get single product
@app.get(
    "/products/{product_id}",
    response_model=Product,
    summary="Get single product",
    tags=["Products"]
)
async def get_product(
    product_id: int,
    current_user: Optional[User] = Depends(get_optional_current_user)
) -> Product:
    """
    Get a single product by ID

    **Authentication:** Optional
    """
    product = next((p for p in MOCK_PRODUCTS if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


# Health check endpoint
@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "products-api",
        "version": "2.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
