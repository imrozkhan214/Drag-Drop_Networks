# utils.py
import logging

# Setting up basic logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

def log_connection(client_ip, status):
    # Logs client connection attempts
    logging.info(f"Connection from {client_ip}: {status}")

def log_error(message):
    # Logs errors
    logging.error(f"Error: {message}")
    
def log_transfer_status(status):
    # Logs file transfer status
    logging.info(f"Transfer status: {status}")
