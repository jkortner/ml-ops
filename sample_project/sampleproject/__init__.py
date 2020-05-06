
import logging

LOGGING_FORMAT = '%(asctime)-15s: [%(name)s] %(message)s'
# LOGGING_FORMAT = '[%(name)s] %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=LOGGING_FORMAT)
