import logging
import logging.handlers

LOG_FILENAME = "logger.log"


def get_logger():
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger(__name__)
    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME, maxBytes=10000, backupCount=100
    )
    # create a logging format
    formatter = logging.Formatter(
        " %(asctime)s %(levelname)-5.5s [%(name)s:%(lineno)s][%(threadName)s] %(message)s"
    )

    handler.setFormatter(formatter)
    my_logger.addHandler(handler)
    return my_logger
    """ my_logger.debug("debug message")
    my_logger.info("info message")
    my_logger.warn("warn message")
    my_logger.error("error message")
    my_logger.critical("critical message") """
