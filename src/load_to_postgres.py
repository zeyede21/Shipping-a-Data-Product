import os
import json
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from datetime import datetime

load_dotenv()

PG_HOST = os.getenv("POSTGRES_HOST")
PG_PORT = os.getenv("POSTGRES_PORT")
PG_DB = os.getenv("POSTGRES_DB")
PG_USER = os.getenv("POSTGRES_USER")
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def get_conn():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )

def create_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE SCHEMA IF NOT EXISTS raw;
    CREATE TABLE IF NOT EXISTS raw.telegram_messages (
        id INT PRIMARY KEY,
        date TIMESTAMP,
        sender_id BIGINT,
        text TEXT,
        has_media BOOLEAN,
        media_type TEXT,
        image_path TEXT,
        channel TEXT
    );
    """)
    conn.commit()
    cur.close()
    conn.close()

def load_json_to_postgres(json_file: Path, channel: str):
    with open(json_file, "r", encoding="utf-8") as f:
        messages = json.load(f)

    conn = get_conn()
    cur = conn.cursor()

    inserted = 0
    for msg in messages:
        try:
            cur.execute("""
            INSERT INTO raw.telegram_messages (id, date, sender_id, text, has_media, media_type, image_path, channel)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
            """, (
                msg["id"],
                msg["date"],
                msg["sender_id"],
                msg["text"],
                msg["has_media"],
                msg["media_type"],
                msg.get("image_path"),
                channel
            ))
            inserted += 1
        except Exception as e:
            logger.warning(f"⚠️ Skipped message {msg['id']}: {e}")

    conn.commit()
    cur.close()
    conn.close()
    logger.success(f"✅ Inserted {inserted} messages from {channel}")

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    folder = Path(f"data/raw/telegram_messages/{today}")
    create_table()

    for json_file in folder.glob("*.json"):
        channel = json_file.stem
        load_json_to_postgres(json_file, channel)

if __name__ == "__main__":
    main()
