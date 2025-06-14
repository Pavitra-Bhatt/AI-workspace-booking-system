# Booking Management System API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
All endpoints except registration and login require a Bearer token in the Authorization header.

### Register User
```http
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123",
    "full_name": "John Doe"
}
```

### Login
```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
```

Response:
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

## Appointments

### Create Appointment
```http
POST /appointments/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "start_time": "2024-03-20T10:00:00",
    "end_time": "2024-03-20T11:00:00",
    "service": "Haircut",
    "notes": "Regular haircut appointment"
}
```

Rules:
- Start time must be before end time
- No overlapping appointments allowed
- Times must be in ISO 8601 format
- Service field is required
- Notes are optional

### Get All Appointments
```http
GET /appointments/?skip=0&limit=100
Authorization: Bearer <access_token>
```

Query Parameters:
- skip: Number of records to skip (default: 0)
- limit: Maximum number of records to return (default: 100)

### Get Appointment by ID
```http
GET /appointments/{appointment_id}
Authorization: Bearer <access_token>
```

Rules:
- appointment_id must be a valid integer
- User can only access their own appointments

### Update Appointment
```http
PUT /appointments/{appointment_id}
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "start_time": "2024-03-20T11:00:00",
    "end_time": "2024-03-20T12:00:00",
    "service": "Haircut and Styling",
    "notes": "Updated appointment details"
}
```

Rules:
- All fields are optional in update
- Cannot update to create overlapping appointments
- User can only update their own appointments

### Delete Appointment
```http
DELETE /appointments/{appointment_id}
Authorization: Bearer <access_token>
```

Rules:
- Soft delete (marks appointment as cancelled)
- User can only delete their own appointments

## Error Responses

### 400 Bad Request
```json
{
    "detail": "This time slot overlaps with an existing appointment"
}
```

### 401 Unauthorized
```json
{
    "detail": "Not authenticated",
    "headers": {
        "WWW-Authenticate": "Bearer"
    }
}
```

### 404 Not Found
```json
{
    "detail": "Appointment not found"
}
```

## Data Models

### User
```json
{
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true
}
```

### Appointment
```json
{
    "id": 1,
    "user_id": 1,
    "start_time": "2024-03-20T10:00:00",
    "end_time": "2024-03-20T11:00:00",
    "service": "Haircut",
    "notes": "Regular haircut appointment",
    "status": "pending"
}
```

## Testing Guidelines

1. Authentication Flow:
   - Register a new user
   - Login to get access token
   - Use token for subsequent requests

2. Appointment Flow:
   - Create an appointment
   - Get all appointments to verify creation
   - Get single appointment by ID
   - Update appointment
   - Delete appointment
   - Verify appointment status is "cancelled"

3. Error Testing:
   - Try creating overlapping appointments
   - Try accessing other users' appointments
   - Try invalid date formats
   - Try missing required fields

## Environment Variables

Required environment variables:
```env
SQLALCHEMY_DATABASE_URL=sqlite:///./app.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
```

## Rate Limiting
- No rate limiting implemented yet
- Consider implementing in production

## Security Notes
1. Always use HTTPS in production
2. Keep access tokens secure
3. Implement proper password hashing (already done with bcrypt)
4. Regular token rotation recommended
5. Implement proper CORS policies 