import logging

logging.basicConfig(
    filename='app.log',
    filemode='a',
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

def log_event(message: str):
    logging.info(message)
