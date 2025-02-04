from fastapi import FastAPI
from pydantic import BaseModel
import random
from fastapi.middleware.cors import CORSMiddleware
import uuid
from liveData import getData
from datetime import datetime
import pytz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

orders = {}

def get_current_ist_time():
    ist_timezone = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist_timezone).strftime('%Y-%m-%d %H:%M:%S')

class PlaceOrderRequest(BaseModel):
    TradingSymbol: str
    Exchange: str
    Qty: int
    OrderPrice: float

@app.post("/placeorder")
def place_order(request: PlaceOrderRequest):
    order_id = str(uuid.uuid4())
    data = getData(request.TradingSymbol, "1m", request.Exchange, nbars=1)

    print(data)

    if isinstance(data['close'], dict):
        fill_price = float(next(iter(data['close'].values()), 0))
    else:
        fill_price = float(data['close'])

    if fill_price == 0:
        return {"error": "Failed to retrieve valid FillPrice"}

    orders[order_id] = {
        "status": "Pending", 
        "reason": None, 
        "FillPrice": fill_price,
        "Qty" : request.Qty,
        "timestamp": get_current_ist_time()
    }
    
    return {"order_id": order_id, "timestamp": orders[order_id]["timestamp"]}

@app.get("/orderstatus/{order_id}")
def get_order_status(order_id: str):
    if order_id in orders:
        statuses = ["filled", "pending", "rejected"]
        selected_status = random.choice(statuses)
        reason = "None"
        
        print(orders[order_id])
        if selected_status == "rejected":
            reasons = ["Margin Shortfall", "Not Enough Quantity", "Order Expired"]
            reason = random.choice(reasons)

        update_data = {
            "status": selected_status,
            "reason": reason,
            "timestamp": get_current_ist_time()
        }

        if selected_status == "filled":
            update_data["FillPrice"] = orders[order_id].get("FillPrice", 0)  # Keep existing FillPrice

        orders[order_id].update(update_data)  # Only update necessary fields

        return orders[order_id]
    else:
        return {"error": "Order ID not found"}



