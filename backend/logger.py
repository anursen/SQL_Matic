import logging
import os
from pathlib import Path
from config import config
import sys

def setup_logger():
    """Initialize and configure the logger based on config settings"""
    
    logger = logging.getLogger("sql_matic")
    log_level = getattr(logging, config._config.get('logging', {}).get('level', 'INFO'))
    logger.setLevel(log_level)
    
    # Configure formatter
    log_format = config._config.get('logging', {}).get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter(log_format)
    
    # Configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Configure file handler if specified
    log_file = config._config.get('logging', {}).get('file')
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(__file__).parent / os.path.dirname(log_file)
        log_path.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(Path(__file__).parent / log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Create a global logger instance
logger = setup_logger()
