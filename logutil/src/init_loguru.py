"""
Loguru
"""


import sys
from pathlib import Path
from typing import Optional, Union

PathType = Union[str, Path]
LevelType = Union[str, int]


def get_loguru_logger():
    from loguru import logger as _logger

    return _logger


def init_loguru(
    fmt: str = "{time:YYYY-MM-DDTHH:mm:ss.SSS!UTC}Z {name} {level}: {message}",
    level: Union[str, int] = "DEBUG",
    enqueue: bool = False,
    stream_on: bool = True,
    file_on: bool = True,
    pushover_on: bool = False,
    sentry_on: bool = False,
    slack_on: bool = False,
    file_fmt: Optional[str] = None,
    pushover_fmt: Optional[str] = None,
    sentry_fmt: Optional[str] = None,
    slack_fmt: Optional[str] = None,
    file_level: Optional[Union[str, int]] = None,
    file_path: PathType = Path(__file__).absolute().parent / "logs" / "log.log",
    file_rotation: str = "20 MB",
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
    """Initialize loguru logging

    :param fmt: logging format
    :param level: logging level for the stream handler
    :param enqueue: set true to make multiprocess / async safe
        always thread-safe
    :param stream_on: include stream logging handler
    :param file_on: include file logging handler
    :param pushover_on: include pushover logging handler
    :param sentry_on: include sentry logging handler
    :param slack_on: include slack logging handler
    :param file_fmt: file logging format (if None, fmt is used)
    :param pushover_fmt: pushover logging format (if None, fmt is used)
    :param sentry_fmt: sentry logging format (if None, fmt is used)
    :param slack_fmt: slack logging format (if None, fmt is used)
    :param file_level: logging level for the file handler
        Defaults to the stream handler level
    :param file_path: log file path
    :param file_rotation: rotate log file when it reaches this size
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
    from loguru import logger as _logger

    _logger.remove()
    if stream_on:
        _logger.add(sys.stderr, format=fmt, level=level, enqueue=enqueue)

    if file_on:
        file_fmt = fmt if file_fmt is None else file_fmt
        file_level_ = level if file_level is None else file_level
        _logger.add(
            file_path,
            format=file_fmt,
            level=file_level_,
            enqueue=enqueue,
            rotation=file_rotation,
            retention=file_retention,
        )

    if pushover_on:
        from notifiers.logging import NotificationHandler

        pushover_fmt = fmt if pushover_fmt is None else pushover_fmt
        pushover_handler = NotificationHandler(
            "pushover",
            defaults=dict(
                user=pushover_user,
                token=pushover_token,
            ),
            level=pushover_level,
        )
        _logger.add(pushover_handler, format=pushover_fmt, level=pushover_level, enqueue=enqueue)

    if sentry_on:
        import sentry_sdk
        from sentry_sdk.integrations.logging import BreadcrumbHandler, EventHandler

        sentry_fmt = fmt if sentry_fmt is None else sentry_fmt
        sentry_sdk.init(dsn=sentry_dsn, integrations=[])

        sentry_breadcrumb_handler = BreadcrumbHandler(level=sentry_breadcramp_level)
        _logger.add(
            sentry_breadcrumb_handler,
            format=sentry_fmt,
            level=sentry_breadcramp_level,
            enqueue=enqueue,
        )

        sentry_event_handler = EventHandler(level=sentry_event_level)
        _logger.add(
            sentry_event_handler, format=sentry_fmt, level=sentry_event_level, enqueue=enqueue
        )

    if slack_on:
        from notifiers.logging import NotificationHandler

        slack_fmt = fmt if slack_fmt is None else slack_fmt
        slack_handler = NotificationHandler(
            "slack",
            defaults=dict(
                webhook_url=slack_webhook_url,
            ),
            level=slack_level,
        )
        _logger.add(slack_handler, format=slack_fmt, level=slack_level, enqueue=enqueue)
