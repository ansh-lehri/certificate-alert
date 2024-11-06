import logging
import sys
import os


logger = logging.getLogger(__name__)

if os.getenv('LOG_LEVEL') is not None:
    if os.getenv('LOG_LEVEL') not in [logging.getLevelName(logging.INFO), logging.getLevelName(logging.DEBUG),
                                      logging.getLevelName(logging.CRITICAL), logging.getLevelName(logging.WARNING),
                                      logging.getLevelName(logging.ERROR) ]:
        raise Exception(f"Invalid log level {os.getenv('LOG_LEVEL')} in environment variable")
    logger.setLevel(os.getenv('LOG_LEVEL'))
else:
    logger.setLevel(logging.INFO)

stdout_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout_handler)