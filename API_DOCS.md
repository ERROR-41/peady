# API Documentation

This document provides detailed information about the Peady Pet Adoption API endpoints.

## Base URL

- Development: `http://localhost:8000/api/v1/`
- Production: `https://your-domain.com/api/v1/`

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Obtaining a Token

1. **Register a new user:**
   ```
   POST /auth/users/
   {
     "email": "user@example.com",
     "password": "yourpassword",
     "re_password": "yourpassword"
   }
   ```

2. **Login to get JWT token:**
   ```
   POST /auth/jwt/create/
   {
     "email": "user@example.com",
     "password": "yourpassword"
   }
   ```

## API Endpoints Reference

### 🔐 Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/users/` | Register new user | No |
| POST | `/auth/jwt/create/` | Login (get JWT) | No |
| POST | `/auth/jwt/refresh/` | Refresh JWT token | No |
| POST | `/auth/users/activation/` | Activate account | No |
| POST | `/auth/users/reset_password/` | Reset password | No |

### 🐾 Pet Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/pets/` | List all pets | No |
| POST | `/api/v1/pets/` | Create new pet | Yes (Admin) |
| GET | `/api/v1/pets/{id}/` | Get pet details | No |
| PUT | `/api/v1/pets/{id}/` | Update pet | Yes (Admin) |
| DELETE | `/api/v1/pets/{id}/` | Delete pet | Yes (Admin) |

### 📂 Pet Categories

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/categories/` | List categories | No |
| POST | `/api/v1/categories/` | Create category | Yes (Admin) |
| GET | `/api/v1/categories/{id}/` | Get category | No |
| PUT | `/api/v1/categories/{id}/` | Update category | Yes (Admin) |

### 🖼️ Pet Images

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/pets/{pet_id}/images/` | Get pet images | No |
| POST | `/api/v1/pets/{pet_id}/images/` | Add pet image | Yes (Admin) |
| DELETE | `/api/v1/pets/{pet_id}/images/{id}/` | Delete image | Yes (Admin) |

### ⭐ Pet Reviews

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/pets/{pet_id}/reviews/` | Get pet reviews | No |
| POST | `/api/v1/pets/{pet_id}/reviews/` | Add review | Yes |
| PUT | `/api/v1/pets/{pet_id}/reviews/{id}/` | Update review | Yes (Owner) |
| DELETE | `/api/v1/pets/{pet_id}/reviews/{id}/` | Delete review | Yes (Owner/Admin) |

### 🛒 Shopping Cart

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/carts/` | Get user's cart | Yes |
| POST | `/api/v1/carts/` | Create cart | Yes |
| GET | `/api/v1/carts/{cart_id}/items/` | Get cart items | Yes |
| POST | `/api/v1/carts/{cart_id}/items/` | Add item to cart | Yes |
| PUT | `/api/v1/carts/{cart_id}/items/{id}/` | Update cart item | Yes |
| DELETE | `/api/v1/carts/{cart_id}/items/{id}/` | Remove from cart | Yes |

### 📦 Orders

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/orders/` | List user orders | Yes |
| POST | `/api/v1/orders/` | Create order | Yes |
| GET | `/api/v1/orders/{id}/` | Get order details | Yes |
| GET | `/api/v1/orders/{order_id}/items/` | Get order items | Yes |

### 👤 User Profile

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/profile/` | Get user profile | Yes |
| PUT | `/api/v1/profile/` | Update profile | Yes |
| PATCH | `/api/v1/profile/` | Partial update | Yes |

### 💰 Account Balance

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/account_balance/` | Get balance | Yes |
| POST | `/api/v1/account_balance/` | Add money | Yes |

### 💳 Payment History

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/payment_history/` | Get transactions | Yes |

## Error Responses

The API returns standard HTTP status codes:

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

Error response format:
```json
{
  "error": "Error message description",
  "code": "ERROR_CODE"
}
```

## Rate Limiting

- Authenticated users: 1000 requests per hour
- Anonymous users: 100 requests per hour

## Interactive Documentation

For detailed request/response schemas and to test the API:

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`