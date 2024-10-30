import logging
import os
import sys
from datetime import datetime

class Logger:
    _instance = None
    
    @staticmethod
    def setup():
        if not Logger._instance:
            # Create logs directory if it doesn't exist
            logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            
            # Create logger
            logger = logging.getLogger('marketplace_calculator')
            logger.setLevel(logging.DEBUG)
            
            # Create formatters
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
            )
            console_formatter = logging.Formatter(
                '%(levelname)s - %(message)s'
            )
            
            # File handler
            log_file = os.path.join(logs_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_formatter)
            
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(console_formatter)
            
            # Add handlers
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
            Logger._instance = logger
        
        return Logger._instance
    
    @staticmethod
    def get_logger():
        if not Logger._instance:
            Logger.setup()
        return Logger._instance