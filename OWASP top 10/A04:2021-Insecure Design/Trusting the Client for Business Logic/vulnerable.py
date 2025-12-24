from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CheckoutStep3(BaseModel):
    item_id: int
    quantity: int
    price_to_pay: float  # VULNERABLE: The price is sent by the client!

@app.post("/checkout/final")
def complete_purchase(data: CheckoutStep3):
    """
    VULNERABLE DESIGN: 
    The server 'trusts' the price sent by the user's browser.
    """
    # In a real app, this would charge the credit card
    print(f"Charging card: ${data.price_to_pay}")
    
    return {
        "status": "Success",
        "message": f"You bought {data.quantity} of item {data.item_id} for ${data.price_to_pay}"
    }