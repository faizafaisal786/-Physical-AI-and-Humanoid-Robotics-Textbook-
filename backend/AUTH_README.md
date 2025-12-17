# Authentication System Documentation

Modern authentication system built with FastAPI, following BetterAuth-style security practices.

## Features

- **Email/Password Authentication** - Secure user registration and login
- **JWT Tokens** - Access tokens (30 min) + Refresh tokens (30 days)
- **Session Management** - Track and manage user sessions across devices
- **Password Security** - Bcrypt hashing with strength validation
- **Protected Routes** - Middleware for authentication and authorization
- **Cursor-based Pagination** - Efficient pagination for products API

## Project Structure

```
backend/
├── app.py                 # Main FastAPI application
├── models.py              # SQLAlchemy database models
├── schemas.py             # Pydantic request/response schemas
├── database.py            # Database configuration
├── auth_utils.py          # Password hashing & JWT utilities
├── auth_routes.py         # Authentication endpoints
├── dependencies.py        # Auth middleware & dependencies
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
└── auth.db                # SQLite database (auto-created)
```

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

**Important:** Change the `JWT_SECRET_KEY` in production!

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Initialize Database

```bash
python init_db.py
```

### 4. Run Server

```bash
# Option 1: Using uvicorn (recommended)
uvicorn app:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Python directly
python app.py
```

### 5. Access API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **API Info:** http://localhost:8000/

## API Endpoints

### Authentication

#### 1. Signup (Register)
```http
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "username": "johndoe",
  "full_name": "John Doe"
}
```

**Password Requirements:**
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit

**Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "is_active": true,
    "is_verified": false,
    "is_admin": false,
    "created_at": "2025-12-17T10:00:00",
    "last_login": "2025-12-17T10:00:00"
  },
  "tokens": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer",
    "expires_in": 1800
  },
  "message": "Account created successfully"
}
```

#### 2. Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response:** Same as signup response

#### 3. Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### 4. Logout
```http
POST /auth/logout
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### 5. Logout from All Devices
```http
POST /auth/logout-all
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

#### 6. Get Active Sessions
```http
POST /auth/sessions
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Protected Routes

#### Get Current User Profile
```http
GET /me
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "is_admin": false,
  "created_at": "2025-12-17T10:00:00",
  "last_login": "2025-12-17T10:00:00"
}
```

### Products API (Public/Optional Auth)

#### Get Products (Paginated)
```http
GET /products?limit=10&next_cursor={cursor}
Authorization: Bearer {access_token}  # Optional
```

#### Get Single Product
```http
GET /products/1
Authorization: Bearer {access_token}  # Optional
```

## Usage Examples

### JavaScript/TypeScript

```javascript
// 1. Signup
const signup = async (email, password) => {
  const response = await fetch('http://localhost:8000/auth/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();

  // Store tokens
  localStorage.setItem('access_token', data.tokens.access_token);
  localStorage.setItem('refresh_token', data.tokens.refresh_token);

  return data;
};

// 2. Login
const login = async (email, password) => {
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();

  localStorage.setItem('access_token', data.tokens.access_token);
  localStorage.setItem('refresh_token', data.tokens.refresh_token);

  return data;
};

// 3. Make authenticated request
const getProfile = async () => {
  const token = localStorage.getItem('access_token');

  const response = await fetch('http://localhost:8000/me', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (response.status === 401) {
    // Token expired, refresh it
    await refreshToken();
    return getProfile(); // Retry
  }

  return await response.json();
};

// 4. Refresh token
const refreshToken = async () => {
  const refresh_token = localStorage.getItem('refresh_token');

  const response = await fetch('http://localhost:8000/auth/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token })
  });

  const data = await response.json();
  localStorage.setItem('access_token', data.access_token);

  return data;
};

// 5. Logout
const logout = async () => {
  const refresh_token = localStorage.getItem('refresh_token');

  await fetch('http://localhost:8000/auth/logout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token })
  });

  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
};
```

### Python

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Signup
def signup(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/signup",
        json={"email": email, "password": password}
    )
    data = response.json()
    return data

# 2. Login
def login(email, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )
    return response.json()

# 3. Get profile (authenticated)
def get_profile(access_token):
    response = requests.get(
        f"{BASE_URL}/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return response.json()

# 4. Refresh token
def refresh_token(refresh_token):
    response = requests.post(
        f"{BASE_URL}/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    return response.json()
```

### cURL

```bash
# Signup
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123"}'

# Get profile (replace TOKEN with actual token)
curl http://localhost:8000/me \
  -H "Authorization: Bearer TOKEN"

# Get products (paginated)
curl http://localhost:8000/products?limit=10

# Refresh token
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"REFRESH_TOKEN"}'

# Logout
curl -X POST http://localhost:8000/auth/logout \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"REFRESH_TOKEN"}'
```

## Security Best Practices

1. **Always use HTTPS in production**
2. **Change JWT_SECRET_KEY** - Use a long, random string
3. **Set proper CORS origins** - Don't use `*` in production
4. **Use environment variables** - Never commit secrets to git
5. **Implement rate limiting** - Prevent brute force attacks
6. **Add email verification** - Before allowing sensitive operations
7. **Use strong passwords** - Enforce password policy
8. **Rotate refresh tokens** - Consider rotating on refresh
9. **Monitor sessions** - Track and alert on suspicious activity
10. **Use PostgreSQL in production** - SQLite is for development only

## Database Models

### User
- id, email, username, full_name
- hashed_password
- is_active, is_verified, is_admin
- created_at, updated_at, last_login

### Session
- id, user_id, refresh_token
- ip_address, user_agent
- is_active, created_at, expires_at, last_used

## Environment Variables

```bash
# Database
DATABASE_URL=sqlite:///./auth.db

# JWT
JWT_SECRET_KEY=your-secret-key-here

# App
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# Token Expiration
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
```

## Troubleshooting

### Token Expired Error
- Access tokens expire after 30 minutes
- Use refresh token to get new access token
- Implement automatic token refresh in your client

### Invalid Credentials
- Check email and password are correct
- Passwords are case-sensitive
- Verify account is active

### CORS Errors
- Update `ALLOWED_ORIGINS` in .env
- Set correct origins in `app.py` CORS middleware

### Database Errors
- Run `python init_db.py` to create tables
- Check database file permissions
- Verify SQLite is installed

## Production Deployment

### Use PostgreSQL

```bash
# Install psycopg2
pip install psycopg2-binary

# Update DATABASE_URL
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Use a Proper ASGI Server

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Environment Variables

- Use production secret manager (AWS Secrets Manager, etc.)
- Never commit .env to git
- Rotate secrets regularly

## Next Steps

- [ ] Add email verification
- [ ] Implement password reset
- [ ] Add OAuth providers (Google, GitHub)
- [ ] Add 2FA/TOTP support
- [ ] Implement rate limiting
- [ ] Add user roles and permissions
- [ ] Add audit logging
- [ ] Add password history
- [ ] Implement account lockout
- [ ] Add API rate limiting per user

## Support

For issues or questions:
1. Check the API documentation: http://localhost:8000/docs
2. Review the code in `backend/` directory
3. Check the error logs in terminal

---

**Built with FastAPI, SQLAlchemy, and modern authentication best practices.**
