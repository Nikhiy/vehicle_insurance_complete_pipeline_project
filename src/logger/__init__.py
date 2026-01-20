import logging
import os
from logging.handlers import RotatingFileHandler
from src.utils.root import from_root
from datetime import datetime

# ================================
# LOG FILE SETUP
# ================================

LOG_DIR = 'logs'

# Timestamped log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

MAX_LOG_SIZE = 5 * 1024 * 1024  # 5 MB
BACKUP_COUNT = 3               # Keep last 3 log files

log_dir_path = os.path.join(from_root(), LOG_DIR)
os.makedirs(log_dir_path, exist_ok=True)

log_file_path = os.path.join(log_dir_path, LOG_FILE)

# ================================
# LOGGER CONFIGURATION
# ================================

def configure_logger():
    # Get root logger
    logger = logging.getLogger()

    # 🔴 IMPORTANT:
    # Set root logger to INFO (NOT DEBUG)
    # This prevents PyMongo internal spam
    logger.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter(
        "[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s"
    )

    # ================================
    # FILE HANDLER (LOG FILE)
    # ================================

    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=MAX_LOG_SIZE,
        backupCount=BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)

    # File can store more detail if needed
    file_handler.setLevel(logging.INFO)

    # ================================
    # CONSOLE HANDLER (TERMINAL)
    # ================================

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Console should stay clean
    console_handler.setLevel(logging.INFO)

    # ================================
    # ADD HANDLERS
    # ================================

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # ================================
    # 🔥 SILENCE PYMONGO DEBUG LOGS
    # ================================

    logging.getLogger("pymongo").setLevel(logging.WARNING)
    logging.getLogger("pymongo.command").setLevel(logging.WARNING)
    logging.getLogger("pymongo.connection").setLevel(logging.WARNING)
    logging.getLogger("pymongo.server").setLevel(logging.WARNING)
    logging.getLogger("pymongo.topology").setLevel(logging.WARNING)

    # Optional: silence urllib3 too
    logging.getLogger("urllib3").setLevel(logging.WARNING)

# Initialize logger once
configure_logger()
