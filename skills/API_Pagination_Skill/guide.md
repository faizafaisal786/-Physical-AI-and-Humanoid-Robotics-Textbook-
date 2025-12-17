# API Pagination Skill - Decision Framework

## Overview
API Pagination is a technique to break large datasets into smaller, manageable chunks. This guide helps you decide between Cursor-based and Offset-based pagination strategies.

## Pagination Types

### 1. Offset-based Pagination
Uses `offset` and `limit` parameters to navigate through pages.

**Example:**
```
GET /products?offset=20&limit=10
```

### 2. Cursor-based Pagination
Uses a cursor (pointer) to mark the position in the dataset.

**Example:**
```
GET /products?cursor=eyJpZCI6MTAwfQ&limit=10
```

## Decision Framework

### Use **Cursor-based Pagination** when:

| Criteria | Reason |
|----------|--------|
| **Large datasets** (>10K records) | More efficient than offset pagination for large datasets |
| **Real-time data** with frequent inserts/deletes | Prevents duplicate or missing items during pagination |
| **Consistent performance** is critical | Query performance doesn't degrade with deeper pages |
| **Mobile/streaming applications** | Better for infinite scroll patterns |
| **High concurrency** | Handles concurrent modifications better |

**Pros:**
- ✅ Consistent performance regardless of page depth
- ✅ No duplicate or missing records during pagination
- ✅ Works well with database indexes
- ✅ Handles deletions/insertions gracefully

**Cons:**
- ❌ Cannot jump to arbitrary pages
- ❌ More complex implementation
- ❌ Requires stable sort order

---

### Use **Offset-based Pagination** when:

| Criteria | Reason |
|----------|--------|
| **Small datasets** (<10K records) | Simpler implementation, performance impact minimal |
| **Static data** with rare changes | No risk of duplicate/missing items |
| **Page number navigation** needed | Users need to jump to specific page numbers |
| **Simple requirements** | Quick prototyping or MVPs |
| **Reporting/analytics** | Users need to navigate to specific pages |

**Pros:**
- ✅ Simple to implement and understand
- ✅ Can jump to any page number
- ✅ Familiar to users (page 1, 2, 3...)
- ✅ Works well for small datasets

**Cons:**
- ❌ Performance degrades with large offsets
- ❌ Duplicates/gaps possible if data changes
- ❌ Inefficient for large datasets
- ❌ Database query cost increases with offset

---

## Quick Decision Tree

```
Is dataset > 10K records?
├── YES → Use Cursor-based
└── NO
    ├── Data changes frequently?
    │   ├── YES → Use Cursor-based
    │   └── NO → Use Offset-based
    └── Need page number navigation?
        ├── YES → Use Offset-based
        └── NO → Use Cursor-based
```

## Implementation Templates

### Cursor-based Pagination Template

```python
from fastapi import FastAPI, Query
from typing import Optional, List
import base64
import json

app = FastAPI()

@app.get("/items")
async def get_items(
    limit: int = Query(default=10, ge=1, le=100),
    cursor: Optional[str] = Query(default=None)
):
    # Decode cursor
    last_id = 0
    if cursor:
        decoded = base64.b64decode(cursor).decode('utf-8')
        cursor_data = json.loads(decoded)
        last_id = cursor_data.get('id', 0)

    # Fetch items (example with database)
    # items = db.query(Item).filter(Item.id > last_id).limit(limit + 1).all()

    # Check if there are more items
    has_next = len(items) > limit
    items = items[:limit]

    # Generate next cursor
    next_cursor = None
    if has_next and items:
        cursor_data = {'id': items[-1].id}
        next_cursor = base64.b64encode(
            json.dumps(cursor_data).encode('utf-8')
        ).decode('utf-8')

    return {
        "data": items,
        "pagination": {
            "limit": limit,
            "next_cursor": next_cursor,
            "has_next": has_next
        }
    }
```

### Offset-based Pagination Template

```python
from fastapi import FastAPI, Query
from typing import List
from math import ceil

app = FastAPI()

@app.get("/items")
async def get_items(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100)
):
    offset = (page - 1) * limit

    # Fetch items and total count
    # items = db.query(Item).offset(offset).limit(limit).all()
    # total = db.query(Item).count()

    total_pages = ceil(total / limit)

    return {
        "data": items,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }
```

## Best Practices

### For Cursor-based Pagination:
1. **Use stable, indexed columns** for cursor (e.g., ID, created_at)
2. **Encode cursors** to hide implementation details
3. **Include sort order** in cursor if using composite keys
4. **Validate cursor format** to prevent errors
5. **Document cursor opacity** - clients shouldn't parse cursors

### For Offset-based Pagination:
1. **Set reasonable limits** (e.g., max 100 items per page)
2. **Use COUNT queries wisely** - they can be expensive
3. **Add caching** for frequently accessed pages
4. **Consider total count alternatives** (e.g., "More than 10,000 results")

## Common Patterns

### Infinite Scroll (Cursor-based)
```javascript
// Client-side example
let cursor = null;
while (hasMore) {
    const response = await fetch(`/api/items?limit=20&cursor=${cursor}`);
    const data = await response.json();

    appendItems(data.items);
    cursor = data.pagination.next_cursor;
    hasMore = data.pagination.has_next;
}
```

### Page Navigation (Offset-based)
```javascript
// Client-side example
function goToPage(pageNumber) {
    const response = await fetch(`/api/items?page=${pageNumber}&limit=20`);
    const data = await response.json();

    renderItems(data.items);
    renderPagination(data.pagination);
}
```

## Summary

| Feature | Cursor-based | Offset-based |
|---------|--------------|--------------|
| Performance | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Simplicity | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Consistency | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Flexibility | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Use Cases | Large, dynamic datasets | Small, static datasets |

**Default Recommendation:** Use Cursor-based pagination for production APIs with large or frequently changing datasets. Use Offset-based for admin panels, reports, or small datasets where page numbers matter.
