# Subscription Management System

A Django REST API for managing user subscriptions, plans, and features with JWT authentication.

## Features

- User registration and authentication (JWT)
- Feature management
- Subscription plans with multiple features
- User subscription management (create, update, deactivate)
- Automatic subscription switching (only one active subscription per user)
- Admin panel for data management
- API documentation with Swagger/OpenAPI
- Comprehensive test suite

## Tech Stack

- **Backend**: Django 5.2.5, Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Database**: SQLite (default, configurable)
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Testing**: Django TestCase, APITestCase

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd assignment
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- **Username**: admin
- **Email**: admin@example.com
- **Password**: admin123 (or your preferred password)

### 6. Create Sample Data via Admin Panel

After creating the superuser, you can create sample data through the admin interface:

1. **Access Admin Panel**: `http://127.0.0.1:8000/admin/`
2. **Login** with your superuser credentials
3. **Create Features**:
   - Go to "Features" → "Add Feature"
   - Create features like: "24/7 Support", "Priority Queue", "Advanced Analytics", etc.
4. **Create Plans**:
   - Go to "Plans" → "Add Plan" 
   - Create plans and assign features to them
5. **Create Test Users**:
   - Go to "Users" → "Add User"
   - Create test users for API testing

**OR** use Django shell if preferred:
- Run: `python manage.py shell`
- Use the code from the Swagger testing section to create sample data

### 7. Run the Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Documentation

### Swagger UI
- **URL**: `http://127.0.0.1:8000/swagger/`
- Interactive API documentation with request/response examples

### ReDoc
- **URL**: `http://127.0.0.1:8000/redoc/`
- Alternative documentation interface

### Admin Panel
- **URL**: `http://127.0.0.1:8000/admin/`
- **Credentials**: Use the superuser account created above

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register/` | User registration |
| POST | `/api/v1/auth/login/` | User login |
| POST | `/api/v1/auth/token/refresh/` | Refresh JWT token |

### Feature Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/features/` | List all features | ✅ |
| POST | `/api/v1/features/create/` | Create new feature | ✅ |

### Plan Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/plans/` | List all plans | ✅ |
| POST | `/api/v1/plans/create/` | Create new plan | ✅ |

### Subscription Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/subscriptions/` | List user's subscriptions | ✅ |
| POST | `/api/v1/subscriptions/create/` | Create new subscription | ✅ |
| PUT | `/api/v1/subscriptions/update/` | Update/change plan | ✅ |
| POST | `/api/v1/subscriptions/deactivate/` | Deactivate subscription | ✅ |

## Using Swagger UI for API Testing
### Authentication in Swagger

1. **Go to Swagger UI**: Open `http://127.0.0.1:8000/swagger/` in your browser

2. **Register a New User**:
   - Find the `POST /api/v1/auth/register/` endpoint
   - Click "Try it out"
   - Use this sample data:
   ```json
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "testpass123",
     "password_confirm": "testpass123"
   }
   ```
   - Click "Execute"
   - Copy the `access` token from the response

3. **Authenticate in Swagger**:
   - Click the "Authorize" button at the top of Swagger UI
   - Enter: `Bearer YOUR_ACCESS_TOKEN` (replace with actual token)
   - Click "Authorize" then "Close"

4. **Now you can test all authenticated endpoints!**

### Sample Data for Testing APIs

#### 1. User Registration Data:
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure123",
  "password_confirm": "secure123"
}
```

#### 2. User Login Data:
```json
{
  "email": "john@example.com",
  "password": "secure123"
}
```

#### 3. Create Features:
```json
{
  "name": "24/7 Support"
}
```

```json
{
  "name": "Priority Queue"
}
```

```json
{
  "name": "Advanced Analytics"
}
```

#### 4. Create Plans:
```json
{
  "name": "Basic Plan",
  "feature_ids": [1]
}
```

```json
{
  "name": "Pro Plan", 
  "feature_ids": [1, 2]
}
```

```json
{
  "name": "Enterprise Plan",
  "feature_ids": [1, 2, 3]
}
```

#### 5. Create Subscription:
```json
{
  "plan": 1
}
```

#### 6. Update Subscription (Change Plan):
```json
{
  "plan": 2
}
```

### Testing Workflow in Swagger

1. **Start with Authentication**:
   - Register → Login → Copy access token → Authorize in Swagger

2. **Create Base Data**:
   - Create 3-4 features using the feature creation endpoint
   - Create 2-3 plans with different feature combinations
   
3. **Test Subscription Flow**:
   - Create a subscription for a plan
   - List subscriptions to see the created subscription
   - Update subscription to change plan
   - List again to see the plan change
   - Deactivate subscription
   - List to confirm deactivation

### Expected API Responses

#### Successful Login Response:
```json
{
  "user_id": 1,
  "email": "john@example.com",
  "username": "john_doe",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Subscription List Response:
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "start_date": "2025-01-15T10:30:00Z",
      "is_active": true,
      "plan": {
        "id": 1,
        "name": "Basic Plan",
        "features": [
          {
            "id": 1,
            "name": "24/7 Support"
          }
        ]
      }
    }
  ]
}
```

## Testing

### Run Tests via Django

```
python manage.py test
```

### Run Specific Test Cases

```
# Test subscription models
python manage.py test subscription.tests.SubscriptionModelTestCase

# Test subscription APIs  
python manage.py test subscription.tests.SubscriptionAPITestCase
```

### Test Coverage

The test suite covers:
- Model behavior (subscription creation, auto-deactivation)
- API endpoints (CRUD operations)
- Authentication requirements
- Query optimization
- Error handling

## Project Structure

```
assignment/
├── assignment/                 # Main project directory
│   ├── __init__.py
│   ├── settings.py            # Project settings
│   ├── urls.py                # Main URL configuration
│   ├── models.py              # Custom User model
│   └── admin.py               # User admin configuration
├── subscription/              # Subscription app
│   ├── models.py              # Feature, Plan, Subscription models
│   ├── serializers.py         # API serializers
│   ├── views.py               # API views
│   ├── urls.py                # App URL configuration
│   ├── auth_urls.py           # Authentication URLs
│   ├── auth_views.py          # Authentication views
│   ├── admin.py               # Admin configuration
│   └── tests.py               # Test cases
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```