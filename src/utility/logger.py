import logging

# Configure logging once
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for more details
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Create a logger instance
def log_info(text):
    logging.info(text)