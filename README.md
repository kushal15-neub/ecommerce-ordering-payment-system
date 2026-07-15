# E-commerce Ordering & Payment System

Backend API for managing users, products, orders, and payments with Stripe (test mode) and mock bKash support.

## Features

- JWT Authentication (register, login, token refresh)
- Product Management (admin create/update/delete, public read)
- Orders with multiple items and automatic totals
- Stripe Payments (test mode + webhook)
- bKash Mock Payments (sandbox simulation + webhook)
- Strategy Pattern for payment providers
- DFS Category Tree traversal
- Product Recommendations via category hierarchy
- Redis caching (optional, falls back to local memory)
- Seed data command for demo

## Tech Stack

- Python / Django 6
- Django REST Framework
- MySQL
- JWT (SimpleJWT)
- Stripe Test API
- Redis (optional)

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
STRIPE_PUBLIC_KEY=pk_test_xxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxx
SECRET_KEY=your-django-secret-key
REDIS_URL=redis://127.0.0.1:6379/1
```

`REDIS_URL` is optional. If not set, the app uses local memory cache.

### 3. Database

```bash
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

### 4. Admin login

After seeding:

- Username: `admin`
- Password: `Admin123!`
- URL: `http://127.0.0.1:8000/admin/`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register customer |
| POST | `/api/auth/login/` | Get JWT tokens |
| POST | `/api/auth/token/refresh/` | Refresh access token |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List products |
| GET | `/api/products/?category=1` | Filter by category tree |
| GET | `/api/products/{id}/` | Product detail |
| POST | `/api/products/` | Create product (admin) |
| PUT/PATCH/DELETE | `/api/products/{id}/` | Update/delete (admin) |
| GET | `/api/products/categories/{id}/tree/` | Category tree (DFS) |
| GET | `/api/products/recommendations/{id}/` | Related products |

### Orders (JWT required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders/` | My orders |
| POST | `/api/orders/` | Create order |
| GET | `/api/orders/{id}/` | Order detail |

### Payments (JWT required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/payments/` | My payments |
| POST | `/api/payments/create/` | Start payment |
| GET | `/api/payments/{id}/` | Payment detail |
| POST | `/api/payments/stripe/webhook/` | Stripe webhook |
| POST | `/api/payments/bkash/webhook/` | Mock bKash webhook |

## JWT Usage

### Register

```bash
POST /api/auth/register/
{
  "username": "john",
  "email": "john@gmail.com",
  "password": "Pass1234!"
}
```

### Login

```bash
POST /api/auth/login/
{
  "username": "john",
  "password": "Pass1234!"
}
```

Response:

```json
{
  "access": "eyJ...",
  "refresh": "eyJ..."
}
```

Use the access token in headers:

```
Authorization: Bearer <access_token>
```

## Order Flow

1. User registers and logs in
2. User browses products
3. User creates an order with multiple items
4. User starts payment with `stripe` or `bkash`
5. Provider confirms payment (Stripe webhook or bKash mock webhook)
6. Order status becomes `paid` and stock is reduced

## Stripe (Test Mode)

```bash
stripe login
stripe listen --forward-to http://127.0.0.1:8000/api/payments/stripe/webhook/
stripe trigger payment_intent.succeeded
```

Use ngrok if testing webhooks from outside localhost:

```bash
ngrok http 8000
```

Then forward Stripe webhooks to your ngrok URL.

## bKash (Mock / Sandbox Simulation)

**Note:** Real bKash sandbox and live APIs require a bKash merchant account. Since merchant credentials were not available, this project implements a **mock bKash strategy** that follows the same flow:

1. Create payment with provider `bkash` → status `pending`
2. Simulate confirmation via mock webhook:

```bash
POST /api/payments/bkash/webhook/
{
  "transaction_id": "BKASH-XXXXXXXXXXXX",
  "status": "success"
}
```

The strategy pattern allows swapping to real bKash API calls when credentials are available.

## Docker

Docker deployment was attempted but could not be completed within the assessment timeline. The project runs locally with:

- Django development server
- MySQL database
- Optional Redis for caching

## Running Tests

```bash
python manage.py test
```

## Design Patterns & Algorithms

- **Strategy Pattern:** `StripePaymentStrategy` and `BkashPaymentStrategy`
- **DFS:** Category tree traversal for filtering and recommendations
- **Caching:** Category tree cached in Redis or local memory
- **Deterministic totals:** Order subtotals and totals calculated consistently
- **Stock safety:** Stock validated on order create and payment; reduced only after successful payment

## Project Structure

```
config/          # Django settings & URLs
users/           # User model & JWT auth
products/        # Products, categories, DFS, recommendations
orders/          # Orders & order items
payments/        # Payments, strategies, webhooks
```

## Submission Notes

- Stripe uses official **test mode** (free, no real charges)
- bKash uses **mock sandbox simulation** due to unavailable merchant account
- Docker was not included due to setup issues; local + ngrok deployment is documented instead
