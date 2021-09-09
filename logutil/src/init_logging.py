"""
Logging (standard python library)
"""


import logging
from pathlib import Path
from typing import Optional, Union

PathType = Union[str, Path]
LevelType = Union[str, int]


def init_logging(
    name: Optional[str] = None,
    fmt: str = "%(asctime)s.%(msecs)03dZ %(name)s %(funcName)s %(levelname)s: %(message)s",
    datefmt: str = "%Y-%m-%dT%H:%M:%S",
    use_gmt_time: bool = True,
    level: Union[str, int] = "DEBUG",
    propagate: bool = False,
    stream_on: bool = True,
    file_on: bool = True,
    pushover_on: bool = False,
    sentry_on: bool = False,
    slack_on: bool = False,
    file_level: Optional[Union[str, int]] = None,
    file_path: PathType = Path(__file__).absolute().parent / "logs" / "log.log",
    file_rotation_bytes: int = 20 * 1024 * 1024,
    file_retention: int = 1,
    pushover_level: LevelType = "WARNING",
    pushover_user: str = "",
    pushover_token: str = "",
    sentry_event_level: LevelType = "WARNING",
    sentry_breadcramp_level: LevelType = "DEBUG",
    sentry_dsn: str = "",
    slack_level: LevelType = "WARNING",
    slack_webhook_url: str = "",
):
    """Initialize standard python logging

    :param name: logger name
    :param fmt: logging format
    :param datefmt: datetime format
    :param use_gmt_time: if true, log datetime in GMT
    :param level: logging level for the stream handler
    :param propagate: if true, propagate to the root logger
    :param stream_on: include stream logging handler
    :param file_on: include file logging handler
    :param pushover_on: include pushover logging handler
    :param sentry_on: include sentry logging handler
    :param slack_on: include slack logging handler
    :param file_level: logging level for the file handler
        Defaults to the stream handler level
    :param file_path: log file path
    :param file_rotation_bytes: rotate log file when it reaches <n> bytes
    :param file_retention: keep <n> old log file
    :param pushover_level: pushover logging level (notifications)
    :param pushover_user: pushover user
    :param pushover_token: pushover token
    :param sentry_event_level: sentry event logging level (notifications)
    :param sentry_breadcramp_level: sentry breadcramp logging level (additional info)
    :param sentry_dsn: sentry DNS
    :param slack_level: slack logging level (notifications)
    :param slack_webhook_url: slack app webhook url
    """
    import time
    from logging.handlers import RotatingFileHandler

    _logger = logging.getLogger(name)
    _logger.handlers.clear()
    _logger.propagate = propagate
    Path(file_path).parent.mkdir(exist_ok=True, parents=True)
    formatter = logging.Formatter(fmt, datefmt=datefmt)
    if use_gmt_time:
        formatter.converter = time.gmtime  # type: ignore

    if stream_on:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        _logger.addHandler(sh)

    _logger.setLevel(level)

    if file_on:
        fh = RotatingFileHandler(
            file_path, mode="a", maxBytes=file_rotation_bytes, backupCount=file_retention
        )
        fh.setFormatter(formatter)
        file_level_ = level if file_level is None else file_level
        fh.setLevel(file_level_)
        _logger.addHandler(fh)

    if pushover_on:
        from notifiers.logging import NotificationHandler

        pushover_handler = NotificationHandler(
            "pushover",
            defaults=dict(
                user=pushover_user,
                token=pushover_token,
            ),
            level=pushover_level,
        )
        pushover_handler.setFormatter(formatter)
        _logger.addHandler(pushover_handler)

    if sentry_on:
        import sentry_sdk
        from sentry_sdk.integrations.logging import BreadcrumbHandler, EventHandler

        sentry_sdk.init(dsn=sentry_dsn, integrations=[])

        sentry_breadcrumb_handler = BreadcrumbHandler(level=sentry_breadcramp_level)
        _logger.addHandler(sentry_breadcrumb_handler)

        sentry_event_handler = EventHandler(level=sentry_event_level)
        _logger.addHandler(sentry_event_handler)

    if slack_on:
        from notifiers.logging import NotificationHandler

        slack_handler = NotificationHandler(
            "slack",
            defaults=dict(
                webhook_url=slack_webhook_url,
            ),
            level=slack_level,
        )
        slack_handler.setFormatter(formatter)
        _logger.addHandler(slack_handler)


def get_logging_logger(name: Optional[str] = None):
    return logging.getLogger(name)
