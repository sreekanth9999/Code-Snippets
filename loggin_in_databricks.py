#reference link : https://ganeshchandrasekaran.com/databricks-using-python-logging-module-in-notebooks-6348bbb3ac60

import os, logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logging(log_dir):

    #Create a new folder, if folder already exists don't throw error
    os.makedirs(log_dir, exist_ok=True)

    # Create a logger with the name of the module
    logger = logging.getLogger(__name__)
    
    # Define the log message format and formatter
    log_format = "%(asctime)s %(levelname)s [%(name)s] {%(threadName)s} %(message)s"
    log_formatter = logging.Formatter(fmt=log_format, datefmt="%H:%M:%S")

    # Create a StreamHandler to output logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)

    # Set the formatter for the file handler
    # Create a TimedRotatingFileHandler that rotates the log file every 60 mins
    # and keeps up to 5 backup files

    log_file = os.path.join(log_dir, f"applog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    file_handler = TimedRotatingFileHandler(log_file, when="m", interval=60, backupCount=5)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Return the configured logger and file handler
    return logger, file_handler


def main():
 try:
 
  # Specify a logging folder
     log_dir = "/Volumes/logs/"

     # Or Get the current working directory and append logs subfolder
     # log_dir = os.path.join(os.getcwd(), 'logs')
     
     # Invoke the Logger
     logger, file_handler = setup_logging(log_dir)

     ## Write your code

     logger.info(f"\n: Application started successfully")

     ## Write your code

     logger.warning(f"\n: High memory usage detected (85%)")

     ## Write your code

     logger.error(f"\n: Database connection timeout after 30s")


     ## Write Your Code

     logger.debug(f"\n: Attempting database reconnection (attempt 1/3)")

     ## Write Your code

     logger.error(f"\n: Database connection timeout after 30s")



    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        # Close the file handler and remove it from the logger
        file_handler.close()
        logger.removeHandler(file_handler)

if __name__ == '__main__':
    main()
