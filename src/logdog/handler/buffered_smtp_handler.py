import contextlib
import logging
import logging.handlers
import smtplib
from datetime import timedelta
from email.message import EmailMessage

from .base_buffered_handler import BaseBufferedHandler, _1min, _4h


class BufferedSmtpHandler(BaseBufferedHandler):
    def __init__(
        self,
        level: int | str = logging.NOTSET,
        *,
        host: str,
        port: int,
        user: str | None = None,
        password: str | None = None,
        sender: str,
        receivers: list[str] | str,
        subject: str,
        use_starttls: bool = True,
        use_ssl: bool = False,
        capacity: int | None = None,
        flush_interval: timedelta | int | str = _4h,
        starting_times: int | None = 10,
        starting_interval: timedelta | int | str | None = _1min,
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.sender = sender
        if isinstance(receivers, str):
            receivers = [r.strip() for r in receivers.split(";")]
        self.receivers = ", ".join(receivers)
        self.subject = subject

        self.use_starttls = use_starttls
        self.use_ssl = use_ssl

        # check connection
        with self._server() as smtp:
            smtp.noop()

        super().__init__(
            level=level,
            capacity=capacity,
            flush_interval=flush_interval,
            starting_times=starting_times,
            starting_interval=starting_interval,
        )

    @contextlib.contextmanager
    def _server(self):
        if self.use_ssl:
            smtp = smtplib.SMTP_SSL(self.host, self.port)
        else:
            smtp = smtplib.SMTP(self.host, self.port)
            if self.use_starttls:
                smtp.starttls()
        if self.user and self.password:
            smtp.login(self.user, self.password)
        with smtp:
            yield smtp

    def flush(self):
        if len(self.buffer) == 0:
            return
        msg = EmailMessage()
        msg["Subject"] = self.subject
        msg["From"] = self.sender
        msg["To"] = self.receivers
        msg.set_content(
            self.build_message(),
        )
        with self.lock:
            try:
                with self._server() as server:
                    server.send_message(msg)
            except Exception:
                self.handleError(self.buffer[-1])
            finally:
                self.buffer.clear()
