"""
This file marks the directory as a Python package and handles
initialization logic.
"""

import logging
from dotenv import load_dotenv

# load environment from the .env file
load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logger.info("Package initialized successfully.")
