"""Logging utility module"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional


class Logger:
    """Custom logger for the Network AI Agent"""

    _instance: Optional["Logger"] = None
    _loggers: dict = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    @staticmethod
    def setup(
        name: str,
        level: str = "INFO",
        log_file: str = "logs/network_agent.log",
        max_bytes: int = 10485760,
        backup_count: int = 5,
    ) -> logging.Logger:
        """Setup logger with file and console handlers"""

        if name in Logger._loggers:
            return Logger._loggers[name]

        # Create logs directory if it doesn't exist
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))

        # Create formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File handler with rotation
        fh = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        fh.setLevel(getattr(logging, level.upper()))
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, level.upper()))
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        Logger._loggers[name] = logger
        return logger

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get or create logger"""
        if name not in Logger._loggers:
            Logger.setup(name)
        return Logger._loggers[name]
