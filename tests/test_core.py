from logutil import get_logging_logger, get_loguru_logger, init_logging, init_loguru


def test_basic_logging():
    init_logging()
    logger = get_logging_logger()
    logger.debug("info message")
    logger.info("info message")
    logger.warning("info message")
    logger.error("info message")
    logger.critical("info message")


def test_basic_loguru():
    init_loguru()
    logger = get_loguru_logger()
    logger.debug("info message")
    logger.info("info message")
    logger.warning("info message")
    logger.error("info message")
    logger.critical("info message")
