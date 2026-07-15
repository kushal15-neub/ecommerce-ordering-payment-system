# Entity Relationship Diagram (ERD)

This document describes the database schema for the E-commerce Ordering & Payment System.

## ERD Diagram

```mermaid
erDiagram
    USERS {
        int id PK
        string username UK
        string email UK
        string password
        string role "customer | admin"
        datetime date_joined
        datetime last_login
    }

    CATEGORIES {
        int id PK
        string name
        int parent_id FK "nullable, self-reference"
    }

    PRODUCTS {
        int id PK
        string name
        string sku UK "nullable"
        text description
        decimal price
        int stock
        boolean status "active/inactive"
        int category_id FK "nullable"
        datetime created_at
        datetime updated_at
    }

    ORDERS {
        int id PK
        int user_id FK
        decimal total_amount
        string status "pending | paid | cancelled"
        datetime created_at
        datetime updated_at
    }

    ORDER_ITEMS {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal price
        decimal subtotal
    }

    PAYMENTS {
        int id PK
        int order_id FK
        string provider "stripe | bkash"
        string transaction_id UK
        string status "pending | success | failed"
        json raw_response
        datetime created_at
        datetime updated_at
    }

    USERS ||--o{ ORDERS : places
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : included_in
    ORDERS ||--o{ PAYMENTS : has
    CATEGORIES ||--o{ CATEGORIES : parent_of
    CATEGORIES ||--o{ PRODUCTS : groups
```

## Relationships

| From | To | Type | Description |
|------|-----|------|-------------|
| User | Order | One-to-Many | A user can place many orders |
| Order | OrderItem | One-to-Many | An order contains multiple line items |
| Product | OrderItem | One-to-Many | A product can appear in many order items |
| Order | Payment | One-to-Many | An order can have payment attempts |
| Category | Category | Self-referential | Parent/child category hierarchy |
| Category | Product | One-to-Many | A category groups many products |

## Indexed / Unique Fields

| Table | Field | Constraint |
|-------|-------|------------|
| Users | email | UNIQUE |
| Users | username | UNIQUE |
| Products | sku | UNIQUE |
| Payments | transaction_id | UNIQUE |

## Status Values

### Order.status
- `pending` — order created, awaiting payment
- `paid` — payment confirmed, stock reduced
- `cancelled` — order cancelled

### Payment.status
- `pending` — payment initiated, awaiting confirmation
- `success` — payment confirmed
- `failed` — payment failed

### Payment.provider
- `stripe` — Stripe PaymentIntent (test mode)
- `bkash` — Mock bKash sandbox simulation

## Notes

- **OrderItem.price** and **OrderItem.subtotal** are stored at order time (price snapshot).
- **Payment.raw_response** stores the full provider response as JSON.
- **Category.parent** enables hierarchical product categorization for DFS traversal.
