# api/main.py

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .schemas import ProductFrequency, ChannelActivity, MessageSearchResult
from . import crud

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/reports/top-products", response_model=list[ProductFrequency])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_products(db, limit)

@app.get("/channels/{channel_name}/activity", response_model=ChannelActivity)
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    return crud.get_channel_activity(db, channel_name)

@app.get("/search/messages", response_model=list[MessageSearchResult])
def search_messages(query: str, db: Session = Depends(get_db)):
    return crud.search_messages(db, query)