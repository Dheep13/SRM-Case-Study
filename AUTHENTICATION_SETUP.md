# Authentication Setup

## Overview

Authentication has been added to the application. Users must login before accessing the homepage and other protected routes.

## Features

- **Login Page**: Beautiful login/register interface
- **Database Authentication**: Username/password stored in database
- **Session Management**: 7-day session tokens
- **Route Protection**: All routes except `/login` require authentication
- **Auto-redirect**: Unauthenticated users redirected to login

## Database Schema

The authentication system uses two tables:

### `users` table
- Stores user credentials (username, password_hash)
- User profile information (email, full_name, student_level)
- Account status (is_active)

### `user_sessions` table
- Stores active session tokens
- Tracks session expiration
- Links to user via user_id

## Default Test Users

The database automatically creates two test users on first initialization:

1. **Admin User**
   - Username: `admin`
   - Password: `password123`
   - Level: Graduate

2. **Student User**
   - Username: `student`
   - Password: `password123`
   - Level: Junior

## API Endpoints

### POST `/api/auth/login`
Login with username and password.

**Request:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "token": "session_token_here",
  "user": {
    "id": "uuid",
    "username": "admin",
    "email": "admin@evolveiq.com",
    "full_name": "Admin User",
    "student_level": "Graduate"
  }
}
```

### POST `/api/auth/register`
Register a new user account.

**Request:**
```json
{
  "username": "newuser",
  "password": "password123",
  "email": "user@example.com",
  "full_name": "New User",
  "student_level": "Junior"
}
```

### POST `/api/auth/verify`
Verify session token validity.

**Request:**
```json
{
  "token": "session_token_here"
}
```

### POST `/api/auth/logout`
Logout and invalidate session.

**Request:**
```json
{
  "token": "session_token_here"
}
```

## Frontend Flow

1. **User visits app** → Check for auth token
2. **No token** → Redirect to `/login`
3. **Has token** → Verify with backend
4. **Token valid** → Show homepage
5. **Token invalid** → Redirect to `/login`

## How to Use

### First Time Setup

1. **Start Docker services:**
   ```bash
   docker compose up -d
   ```

2. **Database initializes automatically** with:
   - Schema tables
   - Default test users

3. **Access frontend:**
   - Go to http://localhost:3000
   - You'll be redirected to login page

4. **Login with test credentials:**
   - Username: `admin` or `student`
   - Password: `password123`

### Creating New Users

Users can register through the login page:
1. Click "Register" on login page
2. Fill in username, password, and optional details
3. Account is created and user is logged in automatically

## Security Notes

⚠️ **Current Implementation:**
- Passwords are stored as plain text (for development)
- Session tokens are simple random strings

🔒 **For Production:**
- Use bcrypt or similar for password hashing
- Implement JWT tokens with proper signing
- Add password strength requirements
- Implement rate limiting on login
- Use HTTPS only
- Add CSRF protection

## Files Created/Modified

### Backend
- `api.py` - Added authentication endpoints
- `db_integration/auth_schema.sql` - User and session tables
- `docker-compose.yml` - Added auth schema to initialization

### Frontend
- `frontend/src/pages/Login.jsx` - Login/Register page
- `frontend/src/pages/Login.css` - Login page styles
- `frontend/src/utils/auth.js` - Authentication utilities
- `frontend/src/components/ProtectedRoute.jsx` - Route protection
- `frontend/src/App.jsx` - Added authentication flow
- `frontend/src/utils/api.js` - Added auth API methods

## Testing

1. **Test Login:**
   - Go to http://localhost:3000
   - Should redirect to `/login`
   - Login with `admin` / `password123`
   - Should redirect to homepage

2. **Test Logout:**
   - Click "Logout" button in navbar
   - Should redirect back to login

3. **Test Registration:**
   - Click "Register" on login page
   - Create new account
   - Should auto-login and redirect to homepage

4. **Test Route Protection:**
   - Logout
   - Try to access http://localhost:3000 directly
   - Should redirect to login

## Troubleshooting

### "Invalid username or password"
- Check database has users table
- Verify auth_schema.sql was run
- Check database logs: `docker compose logs database`

### "Token expired"
- Session expired (7 days)
- User needs to login again

### Login page not showing
- Check frontend is running
- Check browser console for errors
- Verify routes are configured correctly

