import http.client
import json
import logging
import urllib.parse
from datetime import timedelta

from .base_buffered_handler import BaseBufferedHandler, _1min, _4h


class BufferedGoogleChatHandler(BaseBufferedHandler):
    def __init__(
        self,
        level: int | str = logging.NOTSET,
        *,
        webhook_url: str,
        capacity: int | None = None,
        flush_interval: timedelta | int = _4h,
        starting_times: int | None = 10,
        starting_interval: timedelta | int | None = _1min,
    ):
        self.webhook_url = webhook_url

        url_parts = urllib.parse.urlsplit(self.webhook_url)
        host = url_parts.hostname
        url = url_parts.path
        if url_parts.query:
            url += f"?{url_parts.query}"

        self.host = host
        self.url = url

        self.headers = {
            "Content-Type": "application/json",
        }

        super().__init__(
            level=level,
            capacity=capacity,
            flush_interval=flush_interval,
            starting_times=starting_times,
            starting_interval=starting_interval,
        )

    def build_body(self):
        return json.dumps(
            {
                "text": self.build_message(),
            }
        )

    def flush(self):
        if len(self.buffer) == 0:
            return
        body = self.build_body()
        with self.lock:
            try:
                conn = http.client.HTTPSConnection(self.host)
                conn.request(
                    method="POST",
                    url=self.url,
                    body=body,
                    headers=self.headers,
                )
            except Exception:
                self.handleError(self.buffer[-1])
            finally:
                conn.close()
