import os 
import logging 
from datetime import datetime 

# Detect serverless environment (Vercel, AWS Lambda, etc.)
IS_SERVERLESS = (
    os.environ.get("VERCEL") is not None or
    os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None or
    os.path.exists("/var/task") or  # Vercel/Lambda indicator
    not os.access(os.getcwd(), os.W_OK)  # Check if current directory is writable
)

if IS_SERVERLESS:
    # In serverless environments, use console logging only
    # File system is read-only except for /tmp, but logs there would be ephemeral
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]  # Console output only
    )
else:
    # In local/dev environments, use file logging
    LOG_FILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
    log_path = os.path.join(os.getcwd(), "logs")
    
    # Try to create logs directory, fallback to console if it fails
    try:
        os.makedirs(log_path, exist_ok=True)
        LOG_FILEPATH = os.path.join(log_path, LOG_FILE)
        logging.basicConfig(
            level=logging.INFO, 
            filename=LOG_FILEPATH, 
            format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"
        )
    except (OSError, PermissionError) as e:
        # If directory creation fails, fallback to console logging
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()]
        )
        logging.warning(f"Could not create logs directory: {e}. Using console logging instead.")

if __name__ == "__main__":
    # logging.info("This is a test log message")
    pass