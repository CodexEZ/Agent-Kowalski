
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, this is a basic FastAPI server!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# To run this server, save it as main.py and then execute in your terminal:
# uvicorn main:app --reload
