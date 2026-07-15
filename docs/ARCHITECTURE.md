# System Architecture

## High-Level Architecture

```mermaid
flowchart TB
    subgraph Client
        A[Postman / Browser / Frontend]
    end

    subgraph Backend["Django REST API"]
        B[Auth Module<br/>JWT Register/Login]
        C[Products Module<br/>CRUD + DFS + Cache]
        D[Orders Module<br/>Order + OrderItems]
        E[Payments Module<br/>Strategy Pattern]
    end

    subgraph External
        F[Stripe Test API]
        G[Mock bKash Webhook]
    end

    subgraph Data
        H[(MySQL Database)]
        I[(Redis / LocMem Cache)]
    end

    A -->|HTTP REST| B
    A -->|HTTP REST| C
    A -->|HTTP REST| D
    A -->|HTTP REST| E

    B --> H
    C --> H
    C --> I
    D --> H
    E --> H

    E -->|PaymentIntent| F
    F -->|Webhook| E
    G -->|Mock Webhook| E
```

## Application Structure

```
ecommerce-ordering-payment-system/
├── config/              # Project settings, root URLs
├── users/               # Custom User model, JWT auth
├── products/            # Products, Categories, DFS, recommendations
├── orders/              # Orders, OrderItems
├── payments/            # Payments, Strategy pattern, webhooks
└── docs/                # Documentation (ERD, architecture, API)
```

## Design Patterns

### Strategy Pattern (Payments)

```mermaid
classDiagram
    class PaymentStrategy {
        <<abstract>>
        +pay(amount) dict
    }

    class StripePaymentStrategy {
        +pay(amount) dict
    }

    class BkashPaymentStrategy {
        +pay(amount) dict
    }

    class CreatePaymentView {
        +post(request)
    }

    PaymentStrategy <|-- StripePaymentStrategy
    PaymentStrategy <|-- BkashPaymentStrategy
    CreatePaymentView --> PaymentStrategy : selects by provider
```

The payment view selects a strategy based on `provider` (`stripe` or `bkash`) without modifying order logic.

### DFS + Caching (Products)

```mermaid
flowchart LR
    A[Category Tree Request] --> B{Cache Hit?}
    B -->|Yes| C[Return Cached Tree]
    B -->|No| D[DFS Traverse Categories]
    D --> E[Store in Redis/LocMem]
    E --> C
    D --> F[Filter/Recommend Products]
```

- **DFS** traverses the category hierarchy to find all child categories.
- **Cache** stores category tree results to reduce database queries.
- Used for product filtering by category and product recommendations.

## Technology Stack

| Layer | Technology |
|-------|------------|
| Framework | Django 6 + Django REST Framework |
| Authentication | JWT (SimpleJWT) |
| Database | MySQL |
| Cache | Redis (optional) / LocMem fallback |
| Payments | Stripe Test API + Mock bKash |
| Environment | python-dotenv |

## Security

- JWT tokens required for orders and payments
- Admin role required for product create/update/delete
- Stripe API keys stored in `.env` (not committed)
- Webhook endpoints exempt from CSRF (provider callbacks)

## Deployment (Local)

```mermaid
flowchart LR
    A[Developer Machine] --> B[Django runserver :8000]
    B --> C[MySQL localhost]
    B --> D[Optional Redis]
    E[Stripe CLI / ngrok] -->|Webhook forward| B
```

**Note:** Docker deployment was attempted but not completed. The project runs locally with `python manage.py runserver`. Webhooks can be tested using Stripe CLI or ngrok.

## Data Flow Summary

1. User registers and logs in → receives JWT access token
2. User browses products (public read)
3. User creates order with items → total calculated
4. User initiates payment → strategy creates payment record
5. Provider confirms (Stripe webhook / bKash mock webhook)
6. Order marked paid → stock reduced atomically
