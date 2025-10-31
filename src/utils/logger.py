"""
Logging configuration
"""

import logging
import sys
from src.utils.config import Config

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with configuration"""
    config = Config()
    
    logger = logging.getLogger(name)
    
    # Set log level
    log_level = config.get("logging.level", "INFO")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create formatter
    log_format = config.get("logging.format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    formatter = logging.Formatter(log_format)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Add handler if not already added
    if not logger.handlers:
        logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger