from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Server-side "Source of Truth"
PRODUCT_CATALOG = {
    1: {"name": "Laptop", "price": 1200.00},
    2: {"name": "Mouse", "price": 25.00}
}

class CheckoutStep3(BaseModel):
    item_id: int
    quantity: int
    # FIX: We removed 'price_to_pay' from the user input.

@app.post("/checkout/final")
def complete_purchase(data: CheckoutStep3):
    """
    SECURE DESIGN: 
    The server calculates the price using its own trusted data.
    """
    product = PRODUCT_CATALOG.get(data.item_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # THE FIX: Calculate price server-side
    total_price = product["price"] * data.quantity
    
    print(f"Charging card: ${total_price}")
    
    return {
        "status": "Success",
        "message": f"You bought {data.quantity} of {product['name']} for ${total_price}"
    }