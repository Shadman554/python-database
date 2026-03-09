"""
Centralized logging configuration for the application
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Define log format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Setup logger with both file and console handlers
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # File handler with rotation (10MB max, keep 5 backups)
    log_file = LOGS_DIR / f"{name.replace('.', '_')}.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Create application logger
app_logger = setup_logger("vetstan_api", logging.INFO)

# Create separate loggers for different components
auth_logger = setup_logger("vetstan_api.auth", logging.INFO)
db_logger = setup_logger("vetstan_api.database", logging.INFO)
api_logger = setup_logger("vetstan_api.routes", logging.INFO)
security_logger = setup_logger("vetstan_api.security", logging.WARNING)

def log_request(method: str, path: str, status_code: int, duration: float):
    """Log HTTP request details"""
    api_logger.info(f"{method} {path} - {status_code} - {duration:.3f}s")

def log_error(error: Exception, context: str = ""):
    """Log error with context"""
    app_logger.error(f"Error in {context}: {str(error)}", exc_info=True)

def log_security_event(event: str, details: dict = None):
    """Log security-related events"""
    security_logger.warning(f"Security Event: {event} - {details or {}}")
