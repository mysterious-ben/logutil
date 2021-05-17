from logutil import get_logging_logger, get_loguru_logger, init_logging, init_loguru


def test_basic_logging():
    init_logging()
    logger = get_logging_logger()
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")


def test_basic_loguru():
    init_loguru()
    logger = get_loguru_logger()
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
