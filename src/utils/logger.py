import logging
import os
from src.utils.config_loader import load_config

def setup_logging():
    """
    Configura o sistema de logging para o pipeline.
    """
    config = load_config()
    log_config = config.get('logging', {})

    log_file = log_config.get('log_file', 'logs/etl_pipeline.log')
    log_level = log_config.get('level', 'INFO')
    log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format=log_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger(__name__)

logger = setup_logging()
