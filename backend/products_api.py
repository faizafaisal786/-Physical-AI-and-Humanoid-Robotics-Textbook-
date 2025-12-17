"""
Products API with Cursor-based Pagination
Following API_Pagination_Skill guidelines for large, dynamic datasets
"""

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import base64
import json
from datetime import datetime

app = FastAPI(
    title="Products API",
    description="API with cursor-based pagination for efficient product listing",
    version="1.0.0"
)


# Models
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


# Mock Database (In production, replace with actual database)
MOCK_PRODUCTS = [
    Product(id=i, name=f"Product {i}", price=10.0 + i,
            category=["Electronics", "Clothing", "Books", "Home"][i % 4],
            created_at=f"2025-01-{(i % 30) + 1:02d}T10:00:00Z",
            in_stock=i % 3 != 0)
    for i in range(1, 101)  # 100 products
]


def encode_cursor(product_id: int) -> str:
    """
    Encode cursor to hide implementation details
    Cursor contains the last product ID for stable pagination
    """
    cursor_data = {'id': product_id}
    cursor_json = json.dumps(cursor_data)
    encoded = base64.b64encode(cursor_json.encode('utf-8')).decode('utf-8')
    return encoded


def decode_cursor(cursor: str) -> int:
    """
    Decode cursor to extract product ID
    Raises HTTPException if cursor is invalid
    """
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


@app.get(
    "/products",
    response_model=ProductsResponse,
    summary="Get paginated products",
    description="Retrieve products with cursor-based pagination for consistent performance"
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
        description="Cursor for next page (from previous response)"
    )
) -> ProductsResponse:
    """
    Get products with cursor-based pagination.

    **Pagination Strategy:** Cursor-based (following API_Pagination_Skill)

    **Why Cursor-based?**
    - Handles large product catalogs efficiently
    - Prevents duplicates/missing items during inventory updates
    - Consistent performance regardless of page depth
    - Ideal for mobile/infinite scroll patterns

    **Usage:**
    1. First request: GET /products?limit=10
    2. Subsequent requests: GET /products?limit=10&next_cursor={cursor_from_previous_response}
    3. Continue until has_next=false

    **Args:**
        limit: Number of products per page (1-100)
        next_cursor: Encoded cursor from previous response

    **Returns:**
        ProductsResponse with data and pagination metadata
    """

    # Decode cursor to get starting position
    last_id = 0
    if next_cursor:
        last_id = decode_cursor(next_cursor)

    # Simulate database query: SELECT * FROM products WHERE id > last_id ORDER BY id LIMIT (limit + 1)
    # Fetch one extra item to determine if there's a next page
    filtered_products = [p for p in MOCK_PRODUCTS if p.id > last_id]
    products_page = filtered_products[:limit + 1]

    # Check if there are more items
    has_next = len(products_page) > limit
    products = products_page[:limit]

    # Generate next cursor from last item
    next_cursor_value = None
    if has_next and products:
        next_cursor_value = encode_cursor(products[-1].id)

    # Build response
    return ProductsResponse(
        data=products,
        pagination=PaginationMetadata(
            limit=limit,
            next_cursor=next_cursor_value,
            has_next=has_next,
            count=len(products)
        )
    )


@app.get(
    "/products/{product_id}",
    response_model=Product,
    summary="Get single product by ID"
)
async def get_product(product_id: int) -> Product:
    """Get a single product by ID"""
    product = next((p for p in MOCK_PRODUCTS if p.id == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


@app.get("/", summary="API Info")
async def root():
    """API information and usage guide"""
    return {
        "message": "Products API with Cursor-based Pagination",
        "version": "1.0.0",
        "pagination_type": "cursor-based",
        "endpoints": {
            "list_products": "GET /products?limit=10&next_cursor=...",
            "get_product": "GET /products/{id}",
            "docs": "GET /docs",
        },
        "example_usage": {
            "step_1": "GET /products?limit=10",
            "step_2": "Use next_cursor from response in next request",
            "step_3": "GET /products?limit=10&next_cursor=eyJpZCI6MTB9",
            "step_4": "Repeat until has_next=false"
        }
    }


# Example client-side usage (JavaScript)
"""
// Infinite scroll pattern with cursor-based pagination
async function loadAllProducts() {
    let allProducts = [];
    let cursor = null;
    let hasMore = true;

    while (hasMore) {
        const url = cursor
            ? `/products?limit=20&next_cursor=${cursor}`
            : `/products?limit=20`;

        const response = await fetch(url);
        const data = await response.json();

        allProducts.push(...data.data);
        cursor = data.pagination.next_cursor;
        hasMore = data.pagination.has_next;
    }

    return allProducts;
}

// Load single page
async function loadProductsPage(cursor = null) {
    const url = cursor
        ? `/products?limit=20&next_cursor=${cursor}`
        : `/products?limit=20`;

    const response = await fetch(url);
    return await response.json();
}
"""


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
