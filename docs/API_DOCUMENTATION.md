# API Documentation

Base URL: `http://127.0.0.1:8000`

## Authentication

All protected endpoints require JWT Bearer token:

```
Authorization: Bearer <access_token>
```

---

## 1. Authentication APIs

### Register

```http
POST /api/auth/register/
Content-Type: application/json
```

**Request Body:**
```json
{
    "username": "Kushal",
    "email": "kushal@gmail.com",
    "password": "Password123"
}
```

**Response:** `201 Created`
```json
{
    "id": 2,
    "username": "Kushal",
    "email": "kushal@gmail.com"
}
```

---

### Login (Get JWT Token)

```http
POST /api/auth/login/
Content-Type: application/json
```

**Request Body:**
```json
{
    "username": "Kushal",
    "password": "Password123"
}
```

**Response:** `200 OK`
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIs...",
    "access": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

### Refresh Token

```http
POST /api/auth/token/refresh/
Content-Type: application/json
```

**Request Body:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## 2. Product APIs

### List Products (Public)

```http
GET /api/products/
```

**Optional query:** `?category=1` (includes child categories via DFS)

**Response:** `200 OK` — array of products

---

### Product Detail (Public)

```http
GET /api/products/1/
```

---

### Create Product (Admin only)

```http
POST /api/products/
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "name": "Laptop",
    "sku": "LAP-001",
    "description": "High performance laptop",
    "price": "50000.00",
    "stock": 20,
    "status": true,
    "category": 1
}
```

---

### Category Tree (DFS)

```http
GET /api/products/categories/1/tree/
```

**Response:**
```json
{
    "category_id": 1,
    "children": ["Laptops", "Phones", "Gaming Laptops"]
}
```

---

### Product Recommendations (DFS)

```http
GET /api/products/recommendations/1/
```

Returns related products from the same category tree.

---

## 3. Order APIs (JWT Required)

### List My Orders

```http
GET /api/orders/
Authorization: Bearer <access_token>
```

---

### Create Order

```http
POST /api/orders/
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "items": [
        {"product": 1, "quantity": 2},
        {"product": 2, "quantity": 1}
    ]
}
```

> **Note:** Do not send `user` in the body — it is auto-assigned from JWT.

**Response:** `201 Created`
```json
{
    "id": 1,
    "user": 1,
    "total_amount": "100800.00",
    "status": "pending",
    "items": [
        {"id": 1, "product": 1, "quantity": 2, "price": "50000.00", "subtotal": "100000.00"},
        {"id": 2, "product": 2, "quantity": 1, "price": "800.00", "subtotal": "800.00"}
    ]
}
```

---

### Order Detail

```http
GET /api/orders/1/
Authorization: Bearer <access_token>
```

---

## 4. Payment APIs (JWT Required)

### List My Payments

```http
GET /api/payments/
Authorization: Bearer <access_token>
```

---

### Create Payment

```http
POST /api/payments/create/
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Stripe:**
```json
{
    "order": 1,
    "provider": "stripe"
}
```

**bKash (mock):**
```json
{
    "order": 1,
    "provider": "bkash"
}
```

**Response:** `201 Created`
```json
{
    "id": 2,
    "order": 1,
    "provider": "stripe",
    "transaction_id": "pi_3Tt0C9HCohIAyvBv1IaJLHey",
    "status": "pending",
    "raw_response": { ... }
}
```

---

### Payment Detail

```http
GET /api/payments/2/
Authorization: Bearer <access_token>
```

---

## 5. Webhook APIs (No JWT)

### Stripe Webhook

```http
POST /api/payments/stripe/webhook/
```

Called by Stripe when payment succeeds or fails. Test locally with Stripe CLI.

---

### bKash Mock Webhook

```http
POST /api/payments/bkash/webhook/
Content-Type: application/json
```

**Request Body:**
```json
{
    "transaction_id": "BKASH-XXXXXXXXXXXX",
    "status": "success"
}
```

---

## Common Error Responses

| Code | Meaning |
|------|---------|
| 401 | Missing or expired JWT token — login again |
| 403 | Not authorized (e.g., non-admin creating product) |
| 404 | Resource not found |
| 400 | Validation error (missing fields, insufficient stock) |

---

## Postman Tips

1. **Wrong URL format:** Use `GET http://127.0.0.1:8000/api/payments/` — do not type `GET` inside the URL bar.
2. **Expired token:** If you see `Token is expired`, login again and update the Bearer token.
3. **Orders need items:** Send at least one product in the `items` array when creating orders.
4. **Payments endpoint:** Use `POST /api/payments/create/` to start payment, not `POST /api/payments/`.

Import the Postman collection from `docs/postman_collection.json`.
