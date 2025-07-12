from loguru import logger
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

logger.add(f"{log_dir}/pipeline.log", rotation="500 KB")
