# Logutil

(Extremely) easy initialization for `logging` and `loguru`

## Why

This packages makes initialization of `logging` and `loguru` with stream, file, sentry and pushover handlers (extremely) easy.

## Installation

- Logging only: `pip install logutil`
- ... + loguru: `pip install logutil[loguru]`
- ... + notifiers/sentry: `pip install logutil[notifiers]`
- ... + loguru + notifiers/sentry: `pip install logutil[all]`

## Examples

### Standard python logging

```python
from logutil import init_logging, get_logging_logger
init_logging('sub1')
logger = get_logging_logger('sub1')
logger.info('Test INFO message (logging)')
logger.warning('Test WARNING message (logging)')
```
```
2020-07-19T12:59:18.740Z sub1 INFO: Test INFO message (logging)
2020-07-19T12:59:18.740Z sub1 WARNING: Test WARNING message (logging)
```

### Loguru

```python
from logutil import init_loguru, get_loguru_logger
init_loguru()
logger = get_loguru_logger()
logger.info('Test INFO message (loguru)')
logger.warning('Test WARNING message (loguru)')
```
```
2020-07-19T12:56:20.771Z __main__ INFO: Test INFO message (loguru)
2020-07-19T12:56:20.771Z __main__ WARNING: Test WARNING message (loguru)
```

## Notes

- Formatting is ignored for `sentry` notifications with `logging`
