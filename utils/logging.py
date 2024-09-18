import logging
from colorlog import ColoredFormatter
from cfg import LOGGING


# Initializing the logger
def colorlogger(name: str = 'perihelion') -> logging.Logger:
    logger = logging.getLogger(name)
    stream = logging.StreamHandler()

    stream.setFormatter(ColoredFormatter("%(reset)s%(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s"))
    logger.addHandler(stream)
    return logger  # Return the logger


log = colorlogger()

# Set the logger's log level to the one in the config file
if LOGGING["LEVEL"] in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    log.setLevel(LOGGING["LEVEL"])
else:
    log.setLevel("DEBUG")
    log.warning(f"Invalid log level `{LOGGING["LEVEL"]}`. Defaulting to DEBUG.")
