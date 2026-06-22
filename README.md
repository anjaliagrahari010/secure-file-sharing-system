# Secure File Sharing System

A Django-based secure file sharing platform with:

- User Authentication (JWT Token-based)
- Email Verification
- Password Reset & Change
- File Encryption
- Secure Upload & Download
- Access Control
- Audit Logs
- Shareable Secure Links

## Technology Stack

- **Language:** Python 3.9+
- **Framework:** Django 5.0.6
- **REST API:** Django REST Framework
- **Authentication:** JWT (simplejwt)
- **Database:** SQLite (Development) / PostgreSQL (Production)
- **File Security:** Cryptography Library (AES-256, Dual Layer Encryption)

## Project Structure

```
encryptedFileSharing/
├── accounts/              # Authentication & User Management
│   ├── models.py         # User, EmailVerificationToken models
│   ├── views.py          # AuthViewSet, UserViewSet
│   ├── serializers.py    # Authentication serializers
│   ├── urls.py           # API routes
│   └── admin.py          # Django admin config
├── files/                # File Management (To be implemented)
│   ├── models.py         # File, SharedFile, Folder models
│   ├── views.py          # File management views
│   └── serializers.py    # File serializers
├── encryptedFileSharing/ # Project settings
│   ├── settings.py       # Django configuration
│   ├── urls.py           # Main URL router
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
└── requirements.txt      # Project dependencies
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Apply Migrations

```bash
python manage.py migrate
```

### 3. Create Superuser (Optional - for Django admin)

```bash
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Authentication API Endpoints

### 1. User Registration

**POST** `/api/auth/register/`

Register a new user account.

**Request Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "password": "SecurePassword123!",
    "password2": "SecurePassword123!"
}
```

**Response (201 Created):**
```json
{
    "message": "User registered successfully. Please verify your email.",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "phone_number": "+1234567890",
        "profile_picture": null,
        "created_at": "2026-06-22T23:40:00Z"
    }
}
```

**Validation Rules:**
- Username: unique, required
- Email: unique, valid email format, required
- Password: minimum 8 characters, not purely numeric, required
- Passwords must match

---

### 2. User Login

**POST** `/api/auth/login/`

Authenticate user and receive JWT tokens.

**Request Body:**
```json
{
    "username": "johndoe",
    "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
    "message": "Login successful",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe",
        "phone_number": "+1234567890",
        "profile_picture": null,
        "created_at": "2026-06-22T23:40:00Z"
    }
}
```

**Headers for subsequent requests:**
```
Authorization: Bearer <access_token>
```

---

### 3. User Logout

**POST** `/api/auth/logout/`

Logout user and blacklist the refresh token.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "refresh_token": "<refresh_token>"
}
```

**Response (200 OK):**
```json
{
    "message": "Logout successful"
}
```

---

### 4. Refresh Access Token

**POST** `/api/auth/refresh_token/`

Get a new access token using refresh token.

**Request Body:**
```json
{
    "refresh_token": "<refresh_token>"
}
```

**Response (200 OK):**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

## User Profile Management Endpoints

### 1. Get User Profile

**GET** `/api/users/profile/`

Get current authenticated user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone_number": "+1234567890",
    "profile_picture": null,
    "created_at": "2026-06-22T23:40:00Z"
}
```

---

### 2. Update User Profile

**PUT/PATCH** `/api/users/update_profile/`

Update user profile information.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data (if uploading image)
```

**Request Body:**
```json
{
    "full_name": "John Doe Updated",
    "phone_number": "+9876543210",
    "profile_picture": "<file>"
}
```

**Response (200 OK):**
```json
{
    "message": "Profile updated successfully",
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "full_name": "John Doe Updated",
        "phone_number": "+9876543210",
        "profile_picture": "/media/profiles/johndoe.jpg",
        "created_at": "2026-06-22T23:40:00Z"
    }
}
```

---

### 3. Change Password

**POST** `/api/users/change_password/`

Change password for authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "old_password": "OldPassword123!",
    "new_password": "NewPassword456!",
    "new_password2": "NewPassword456!"
}
```

**Response (200 OK):**
```json
{
    "message": "Password changed successfully"
}
```

**Error Response (400 Bad Request):**
```json
{
    "error": "Old password is incorrect"
}
```

---

### 4. Request Password Reset

**POST** `/api/users/request_password_reset/`

Request a password reset token (sent to email).

**Request Body:**
```json
{
    "email": "john@example.com"
}
```

**Response (200 OK):**
```json
{
    "message": "If this email exists, a password reset link will be sent"
}
```

> **Note:** Response is the same whether email exists or not (for security reasons).
> A reset token will be sent to the registered email address.

---

### 5. Confirm Password Reset

**POST** `/api/users/confirm_password_reset/`

Reset password using the token received via email.

**Request Body:**
```json
{
    "token": "550e8400-e29b-41d4-a716-446655440000",
    "new_password": "NewPassword456!",
    "new_password2": "NewPassword456!"
}
```

**Response (200 OK):**
```json
{
    "message": "Password reset successfully"
}
```

---

## JWT Token Details

### Access Token
- **Lifetime:** 1 hour
- **Type:** Bearer token
- **Used for:** Authenticating API requests

### Refresh Token
- **Lifetime:** 7 days
- **Type:** Used to generate new access tokens
- **Purpose:** Long-term authentication without password

### Token Usage
Include access token in all authenticated requests:
```
Authorization: Bearer <access_token>
```

---

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

---

## Database Models

### User Model
Custom user model extending Django's AbstractUser:
- `username` - Unique username
- `email` - Unique email address
- `full_name` - User's full name
- `phone_number` - Optional phone number
- `profile_picture` - Optional profile image
- `created_at` - Account creation timestamp
- `updated_at` - Last profile update timestamp

### EmailVerificationToken Model
- `user` - Foreign key to User
- `tokens` - Unique UUID token
- `expires_at` - Token expiration time
- `is_used` - Whether token has been used
- `created_at` - Token creation timestamp

---

## Security Features

✅ **Password Security:**
- Minimum 8 characters
- Cannot be purely numeric
- Django password validators
- Hashed storage using Django's hasher

✅ **Token Security:**
- JWT tokens with HS256 algorithm
- Token rotation on refresh
- Refresh token blacklisting
- Configurable token lifetimes

✅ **API Security:**
- CORS protection
- CSRF protection (for session-based views)
- Permission classes (IsAuthenticated)
- Token expiration validation

✅ **Email Verification:**
- Token-based email verification
- Expiring verification tokens
- One-time use tokens

---

## Next Steps

1. **Implement Email Sending:**
   - Configure email backend in settings
   - Create email templates for verification and password reset
   - Implement email sending in views (TODO comments)

2. **File Management Module:**
   - Create file upload/download views
   - Implement file encryption
   - Create file sharing endpoints
   - Add access control logic

3. **Audit Logging:**
   - Track user actions (login, file access, etc.)
   - Create audit log models and views

4. **Testing:**
   - Write unit tests for authentication endpoints
   - Write integration tests for API flows
   - Test JWT token generation and validation

5. **Production Deployment:**
   - Update SECRET_KEY with environment variable
   - Set DEBUG = False
   - Configure allowed hosts
   - Use PostgreSQL instead of SQLite
   - Set up HTTPS
   - Configure email service (SendGrid, AWS SES, etc.)

---

## Testing Authentication Endpoints

### Using cURL

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "TestPassword123!",
    "password2": "TestPassword123!"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPassword123!"
  }'

# Get Profile (replace with actual access token)
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer <access_token>"
```

### Using Postman

1. Import the API endpoints as shown above
2. For authenticated requests, go to "Authorization" tab
3. Select "Bearer Token" type
4. Paste the access token from login response

---

## Troubleshooting

### "User matching query does not exist"
- Check that username/email is correct
- Ensure user has been registered

### "Invalid token"
- Token may have expired
- Use refresh token to get new access token

### "CORS error"
- Add your frontend URL to `CORS_ALLOWED_ORIGINS` in settings.py

---

## Contributing

When implementing new features:
1. Create serializers for input validation
2. Use ViewSets for API endpoints
3. Add appropriate permission classes
4. Document all endpoints in this README
5. Write tests for new functionality

---

## License

This project is under development. More details coming soon.
