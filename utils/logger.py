import logging
import os

LOG_LEVEL = "INFO"
LOG_FILE = "logs/ml-scoring-api.log"
 
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
 
    if logger.handlers:
        return logger
 
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
 
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
 
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
 
    # File handler
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
 
    return logger