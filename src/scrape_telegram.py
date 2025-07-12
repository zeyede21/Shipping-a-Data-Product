import os
import json
from pathlib import Path
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv
from loguru import logger

# Load environment variables
load_dotenv()
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

# Setup logger
Path("logs").mkdir(exist_ok=True)
logger.add("logs/scrape_telegram.log", rotation="1 MB")

# Channels to scrape
CHANNELS = [
    "CheMed123",
    "lobelia4cosmetics",
    "tikvahpharma",
]

# Channels we want to store images for
IMAGE_CHANNELS = {"CheMed123", "lobelia4cosmetics"}

# Base folders
TODAY = datetime.now().strftime("%Y-%m-%d")
RAW_MSG_DIR = Path(f"data/raw/telegram_messages/{TODAY}")
RAW_MSG_DIR.mkdir(parents=True, exist_ok=True)

RAW_IMG_DIR = Path(f"data/raw/images/{TODAY}")

# Scrape and store messages for one channel
async def scrape_channel(channel_name: str, limit: int = 200):
    output_path = RAW_MSG_DIR / f"{channel_name}.json"
    logger.info(f"📥 Scraping {channel_name}...")

    async with TelegramClient("scraper_session", API_ID, API_HASH) as client:
        messages_data = []

        try:
            async for message in client.iter_messages(channel_name, limit=limit):
                msg = {
                    "id": message.id,
                    "date": message.date.isoformat(),
                    "sender_id": message.sender_id,
                    "text": message.message,
                    "has_media": bool(message.media),
                    "media_type": type(message.media).__name__ if message.media else None,
                    "image_path": None
                }

                # Save images only for specified channels
                if (
                    channel_name in IMAGE_CHANNELS and
                    isinstance(message.media, MessageMediaPhoto)
                ):
                    channel_img_dir = RAW_IMG_DIR / channel_name
                    channel_img_dir.mkdir(parents=True, exist_ok=True)
                    image_file = channel_img_dir / f"{message.id}.jpg"
                    await message.download_media(file=image_file)
                    msg["image_path"] = str(image_file)

                messages_data.append(msg)

            # Save messages to JSON
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(messages_data, f, ensure_ascii=False, indent=2)

            logger.success(f"✅ Saved {len(messages_data)} messages to {output_path}")

        except Exception as e:
            logger.error(f"❌ Failed to scrape {channel_name}: {e}")

# Main runner
async def main():
    for channel in CHANNELS:
        await scrape_channel(channel)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
