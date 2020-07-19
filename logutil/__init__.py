# --- pip upload ---
# python setup.py sdist bdist_wheel
# twine check dist/*
# twine upload dist/*

from logutil.src.init_logging import init_logging, get_logging_logger
from logutil.src.init_loguru import init_loguru, get_loguru_logger
