"""
A tiny Python logging handler that pushes log records to Loki's HTTP API.

We keep it dependency-light (just `requests`) and fail-safe: if Loki is down,
logging must never crash the app, so push errors are swallowed.

Loki push API:  POST http://localhost:3100/loki/api/v1/push
  { "streams": [ { "stream": {labels...}, "values": [ ["<unix_nanos>", "line"] ] } ] }
"""
import logging
import time

import requests


class LokiHandler(logging.Handler):
    def __init__(self, url="http://localhost:3100/loki/api/v1/push",
                 labels=None, timeout=2):
        super().__init__()
        self.url = url
        self.labels = labels or {"app": "pixelquest-api"}
        self.timeout = timeout

    def emit(self, record):
        try:
            line = self.format(record)
            ts = str(time.time_ns())                  # nanoseconds, as a string
            stream_labels = dict(self.labels)
            stream_labels["level"] = record.levelname  # label by log level
            payload = {
                "streams": [
                    {"stream": stream_labels, "values": [[ts, line]]}
                ]
            }
            requests.post(self.url, json=payload, timeout=self.timeout)
        except Exception:
            # never let logging break the app
            pass


def get_logger(name="pixelquest"):
    """A logger that prints to the console AND ships to Loki."""
    logger = logging.getLogger(name)
    if logger.handlers:            # already configured
        return logger
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(console)

    loki = LokiHandler()
    loki.setFormatter(fmt)
    logger.addHandler(loki)

    return logger
