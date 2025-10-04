# utils/logger.py
import logging
import os
from datetime import datetime

def get_logger(name: str = __name__, log_level: int = logging.DEBUG) -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        name (str): Logger name (usually __name__).
        log_level (int): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    
    Returns:
        logging.Logger: Configured logger.
    """

    # Ensure logs directory exists
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Log file with timestamp
    log_file = os.path.join(log_dir, f"test_log_{datetime.now().strftime('%Y%m%d')}.log")
    print(log_file)

    # Logger configuration
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Avoid duplicate handlers if logger is reused
    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(log_level)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Log format
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
