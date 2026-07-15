# Payment Flow Diagrams

## Stripe Payment Flow (Test Mode)

```mermaid
sequenceDiagram
    participant U as User (JWT)
    participant API as Django API
    participant S as Stripe Test API
    participant WH as Stripe Webhook

    U->>API: POST /api/orders/ (create order)
    API-->>U: Order status = pending

    U->>API: POST /api/payments/create/ {order, provider: stripe}
    API->>API: Check stock availability
    API->>S: Create PaymentIntent
    S-->>API: payment_intent_id, client_secret
    API->>API: Save Payment (status=pending)
    API-->>U: Payment + client_secret

    Note over S,WH: User completes payment on Stripe (test card)

    S->>WH: payment_intent.succeeded
    WH->>API: POST /api/payments/stripe/webhook/
    API->>API: Payment status = success
    API->>API: Order status = paid
    API->>API: Reduce product stock
    API-->>WH: HTTP 200
```

### Stripe Test Setup

```bash
stripe login
stripe listen --forward-to http://127.0.0.1:8000/api/payments/stripe/webhook/
stripe trigger payment_intent.succeeded
```

### Test Card
- Number: `4242 4242 4242 4242`
- Any future expiry, any CVC

---

## bKash Mock Payment Flow (Sandbox Simulation)

> **Note:** Real bKash sandbox/live APIs require a bKash merchant account. This project implements a mock flow that mirrors the real checkout → execute → confirm pattern using the Strategy Pattern.

```mermaid
sequenceDiagram
    participant U as User (JWT)
    participant API as Django API
    participant M as Mock bKash Strategy
    participant WH as bKash Mock Webhook

    U->>API: POST /api/orders/ (create order)
    API-->>U: Order status = pending

    U->>API: POST /api/payments/create/ {order, provider: bkash}
    API->>API: Check stock availability
    API->>M: BkashPaymentStrategy.pay(amount)
    M-->>API: transaction_id, status=pending
    API->>API: Save Payment (status=pending)
    API-->>U: Payment with BKASH-XXXX ID

    Note over U,WH: Simulates bKash Execute Payment callback

    U->>WH: POST /api/payments/bkash/webhook/
    Note right of WH: {transaction_id, status: success}
    WH->>API: Find payment by transaction_id
    API->>API: Payment status = success
    API->>API: Order status = paid
    API->>API: Reduce product stock
    API-->>U: Updated payment record
```

### Mock bKash Webhook Example

```http
POST /api/payments/bkash/webhook/
Content-Type: application/json

{
    "transaction_id": "BKASH-XXXXXXXXXXXX",
    "status": "success"
}
```

To simulate failure:

```json
{
    "transaction_id": "BKASH-XXXXXXXXXXXX",
    "status": "failed"
}
```

---

## Complete Order Lifecycle

```mermaid
stateDiagram-v2
    [*] --> OrderPending: Create order
    OrderPending --> PaymentPending: Start payment
    PaymentPending --> PaymentSuccess: Webhook success
    PaymentPending --> PaymentFailed: Webhook failed
    PaymentSuccess --> OrderPaid: Update order + reduce stock
    PaymentFailed --> OrderPending: Retry payment
    OrderPaid --> [*]
```

## Stock Management Rules

| Stage | Action |
|-------|--------|
| Order create | Validate stock >= quantity for each item |
| Payment create | Re-check stock before initiating payment |
| Payment success | Atomically reduce stock (webhook handler) |
| Payment failed | Stock unchanged |

Stock is **never** reduced until payment status becomes `success`.
