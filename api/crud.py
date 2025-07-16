# api/crud.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from .schemas import ProductFrequency, ChannelActivity, MessageSearchResult

def get_top_products(db: Session, limit: int):
    query = text("""
        SELECT detected_object_class AS product_name, COUNT(*) AS count
        FROM zeyede.fct_image_detections
        GROUP BY detected_object_class
        ORDER BY count DESC
        LIMIT :limit
    """)
    return db.execute(query, {"limit": limit}).fetchall()

def get_channel_activity(db: Session, channel_name: str):
    query = text("""
        SELECT c.channel AS channel_name, COUNT(*) AS message_count
        FROM zeyede.fct_messages m
        JOIN zeyede.dim_channels c ON m.channel_id = c.channel_id
        WHERE c.channel = :channel_name
        GROUP BY c.channel
    """)
    return db.execute(query, {"channel_name": channel_name}).fetchone()

def search_messages(db: Session, query_str: str):
    query = text("""
        SELECT m.message_id, m.message AS content, c.channel AS channel_name, m.date_id AS date
        FROM zeyede.fct_messages m
        JOIN zeyede.dim_channels c ON m.channel_id = c.channel_id
        WHERE LOWER(m.message) LIKE LOWER(:query)
        LIMIT 20
    """)
    return db.execute(query, {"query": f"%{query_str}%"}).fetchall()
