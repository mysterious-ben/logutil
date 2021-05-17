# Logutil

(Extremely) easy initialization for `logging` and `loguru`

## Why

This packages makes it (extremely) easy to send `logging` and `loguru` logs to 
- streams
- files
- sentry
- pushover
- slack

## Installation

- Logging only: `pip install logutil`
- ... + loguru: `pip install logutil[loguru]`
- ... + pushover/sentry/slack: `pip install logutil[notifiers]`
- ... + loguru + pushover/sentry/slack: `pip install logutil[all]`

## Examples

### Standard python logging

```python
from logutil import init_logging, get_logging_logger
init_logging(
    name='data_feeds',
    sentry_on=True,
    sentry_dsn='<your sentry dsn string>',
    sentry_breadcramp_level='INFO',
    sentry_event_level='WARNING',
)
logger = get_logging_logger('data_feeds')
logger.info('Test INFO message (logging)')
logger.warning('Test WARNING message (logging)')
```
```
2020-07-19T12:59:18.740Z data_feeds INFO: Test INFO message (logging)
2020-07-19T12:59:18.740Z data_feeds WARNING: Test WARNING message (logging)
```

### Loguru

```python
from logutil import init_loguru, get_loguru_logger
init_loguru()
logger = get_loguru_logger(
    slack_on=True,
    slack_level='WARNING',
    slack_webhook_url='<your slack app webhook url string>',
)
logger.info('Test INFO message (loguru)')
logger.warning('Test WARNING message (loguru)')
```
```
2020-07-19T12:56:20.771Z __main__ INFO: Test INFO message (loguru)
2020-07-19T12:56:20.771Z __main__ WARNING: Test WARNING message (loguru)
```

## Notes

- Formatting is ignored for `sentry` notifications with `logging`
