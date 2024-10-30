import logging
import os
import sys
from datetime import datetime
from typing import Optional

class Logger:
    _instance: Optional[logging.Logger] = None
    _initialized: bool = False
    _handlers: list = []
    
    @staticmethod
    def setup() -> logging.Logger:
        """
        Sets up the logger with file and console handlers.
        Returns the logger instance.
        """
        # Create the logger instance if it doesn't exist
        if not Logger._instance:
            Logger._instance = logging.getLogger('marketplace_calculator')
            Logger._instance.setLevel(logging.DEBUG)
        
        # Only add handlers if we haven't initialized before
        if not Logger._initialized:
            try:
                # Remove any existing handlers to prevent duplication
                Logger._instance.handlers.clear()
                
                # Create logs directory if it doesn't exist
                logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
                os.makedirs(logs_dir, exist_ok=True)
                
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
                Logger._handlers.append(file_handler)
                
                # Console handler
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setLevel(logging.INFO)
                console_handler.setFormatter(console_formatter)
                Logger._handlers.append(console_handler)
                
                # Add handlers
                for handler in Logger._handlers:
                    Logger._instance.addHandler(handler)
                
                # Set the initialized flag
                Logger._initialized = True
                
                Logger._instance.debug("Logger initialized successfully")
                
            except Exception as e:
                print(f"Error setting up logger: {str(e)}")
                raise
        
        return Logger._instance
    
    @staticmethod
    def get_logger() -> logging.Logger:
        """
        Returns the logger instance, creating it if necessary.
        """
        if not Logger._instance:
            Logger.setup()
        return Logger._instance
    
    @staticmethod
    def shutdown() -> None:
        """
        Properly shuts down the logger, closing all handlers and cleaning up resources.
        Should be called when the application is closing.
        """
        if Logger._instance:
            try:
                Logger._instance.debug("Shutting down logger...")
                
                # Close and remove all handlers
                for handler in Logger._handlers:
                    try:
                        handler.flush()
                        handler.close()
                        Logger._instance.removeHandler(handler)
                    except Exception as e:
                        # Log but don't raise, as we want to continue cleanup
                        print(f"Error closing handler: {str(e)}")
                
                Logger._handlers.clear()
                Logger._initialized = False
                Logger._instance = None
                
            except Exception as e:
                print(f"Error during logger shutdown: {str(e)}")
                raise
    
    @staticmethod
    def flush() -> None:
        """
        Flushes all handlers, ensuring all pending messages are written.
        Useful when you need to ensure all logs are written before continuing.
        """
        if Logger._instance:
            for handler in Logger._handlers:
                try:
                    handler.flush()
                except Exception as e:
                    print(f"Error flushing handler: {str(e)}")