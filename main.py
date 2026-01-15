from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Konfigurasi CORS agar bisa diakses dari browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Izinkan semua origin (untuk development)
    allow_credentials=True,
    allow_methods=["*"],  # Izinkan semua method (GET, POST, PUT, DELETE, dll)
    allow_headers=["*"],  # Izinkan semua headers
)

# Database sementara (in-memory)
items = []

# Model Pydantic
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# ==================== ROOT ====================
@app.get("/")
def read_root():
    return {"Hello": "World"}


# ==================== CREATE ====================
@app.post("/items")
def create_item(
    name: str = Form(...),
    price: float = Form(...),
    description: str | None = Form(None),
    tax: float | None = Form(None)
):
    new_item = {
        "name": name,
        "price": price,
        "description": description,
        "tax": tax
    }
    items.append(new_item)
    return new_item


# ==================== READ ====================
@app.get("/items")
def read_items() -> list:
    return items

@app.get("/items/select={item_id}")
def read_item(item_id: int):
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")


# ==================== UPDATE ====================
@app.put("/items/update/select={item_id}")
def update_item(
    item_id: int,
    name: str = Form(...),
    price: float = Form(...),
    description: str | None = Form(None),
    tax: float | None = Form(None)
):
    if item_id < len(items):
        updated_item = {
            "name": name,
            "price": price,
            "description": description,
            "tax": tax
        }
        items[item_id] = updated_item
        return updated_item
    else:
        raise HTTPException(status_code=404, detail="Item not found")


# ==================== DELETE ====================
@app.delete("/items/delete/{item_id}")
def delete_item(item_id: int):
    if item_id < len(items):
        deleted_item = items.pop(item_id)
        return {"detail": "Item deleted", "item": deleted_item}
    else:
        raise HTTPException(status_code=404, detail="Item not found")