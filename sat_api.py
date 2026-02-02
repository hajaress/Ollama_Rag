from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def greet():
    return {"message" : "Hello!!!"}

class Item(BaseModel):
    name: str
    price: float

# In-memory "database"
items = {}
@app.get("/items/")
def get_items():
    return {"items": items}
# POST → Create new item
@app.post("/items/")
def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return {"id": item_id, "item": item}

# PUT → Update/replace existing item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    items[item_id] = item  # replaces the item entirely
    return {"id": item_id, "item": item}
