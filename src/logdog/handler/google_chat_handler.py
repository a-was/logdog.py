import http.client
import json
import logging
import urllib.parse


class GoogleChatHandler(logging.Handler):
    def __init__(
        self,
        level: int | str = logging.NOTSET,
        *,
        webhook_url: str,
    ):
        super().__init__(level)

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

    def _build_body(self, record: logging.LogRecord):
        return json.dumps(
            {
                "text": self.format(record),
            }
        )

    def emit(self, record: logging.LogRecord):
        body = self._build_body(record)
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
                self.handleError(record)
            finally:
                conn.close()
