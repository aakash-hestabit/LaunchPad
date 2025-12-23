import logging
from pathlib import Path
import os

def setup_logger():

    log_dir = Path(__file__).resolve().parent.parent / 'logs'
  
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file_path = log_dir / 'drift_checker.log'
    
    logging.basicConfig(
        filename=str(log_file_path),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='a' 
    )

    logger = logging.getLogger()
    return logger