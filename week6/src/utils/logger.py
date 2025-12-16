import logging
import os

def setup_logger():
    logging.basicConfig(
        filename='src/logs/pipeline.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a' 
    )
    
    logger = logging.getLogger()
    return logger

logger = setup_logger()
