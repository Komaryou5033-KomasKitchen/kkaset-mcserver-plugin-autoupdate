"""
Logging configuration for the application
"""

import logging
import logging.handlers
from pathlib import Path
from pythonjsonlogger import jsonlogger

def setup_logging(log_level: str = 'INFO', log_file: str = 'logs/plugin_manager.log'):
    """
    Setup application logging
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
    """
    # Create logs directory if it doesn't exist
    Path('logs').mkdir(exist_ok=True)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (JSON format)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    json_formatter = jsonlogger.JsonFormatter()
    file_handler.setFormatter(json_formatter)
    root_logger.addHandler(file_handler)
    
    return root_logger
