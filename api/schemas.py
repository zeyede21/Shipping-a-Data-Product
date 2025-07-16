# api/schemas.py
from pydantic import BaseModel

class ProductFrequency(BaseModel):
    product_name: str
    count: int

class ChannelActivity(BaseModel):
    channel_name: str
    message_count: int

class MessageSearchResult(BaseModel):
    message_id: int
    content: str
    channel_name: str
    date: str
