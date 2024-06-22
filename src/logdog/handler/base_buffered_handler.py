import io
import logging
import logging.handlers
import threading
import time
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime, timedelta

from .. import _util

_4h = timedelta(hours=4)
_1min = timedelta(minutes=1)


class BaseBufferedHandler(ABC, logging.Handler):
    def __init__(
        self,
        level: int | str = logging.NOTSET,
        *,
        capacity: int | None = None,
        flush_interval: timedelta | int | str = _4h,
        starting_times: int | None = 10,
        starting_interval: timedelta | int | str | None = _1min,
    ):
        super().__init__(level)

        self.capacity = capacity or None
        self.buffer: list[logging.LogRecord] = []

        if isinstance(flush_interval, timedelta):
            self.flush_interval = int(flush_interval.total_seconds())
        elif isinstance(flush_interval, int):
            self.flush_interval = flush_interval
        elif isinstance(flush_interval, str):
            self.flush_interval = _util.duration.parse_duration(flush_interval)
        if self.flush_interval <= 0:
            raise ValueError("flush_interval must be positive")

        if starting_times:
            self.starting_times = starting_times
            if isinstance(starting_interval, timedelta):
                self.starting_interval = int(starting_interval.total_seconds())
            elif isinstance(starting_interval, int):
                self.starting_interval = starting_interval
            elif isinstance(starting_interval, str):
                self.starting_interval = _util.duration.parse_duration(flush_interval)
            if self.starting_interval <= 0:
                raise ValueError("starting_interval must be positive")
        else:
            self.starting_times = 0
            self.starting_interval = None

        self.closed = threading.Event()
        self._start_flushing_thread()

    def emit(self, record: logging.LogRecord):
        if self.closed.is_set():
            return
        self.buffer.append(record)
        if self._should_flush(record):
            self.flush()

    def _should_flush(self, record: logging.LogRecord) -> bool:
        if self.capacity is None:
            # using timed flush only
            return False
        return len(self.buffer) >= self.capacity

    @abstractmethod
    def flush(self):
        raise NotImplementedError

    def close(self):
        try:
            self.closed.set()
            self.flush()
        finally:
            super().close()

    def _start_flushing_thread(self):
        self.thread = threading.Thread(
            target=self._flush_intervals,
            daemon=True,
        )
        self.thread.start()

    def _sleep_time_generator(self):
        for _ in range(self.starting_times):
            yield self.starting_interval
        while True:
            yield self.flush_interval

    def _flush_intervals(self):
        for sleep_time in self._sleep_time_generator():
            if self.closed.is_set():
                break
            time.sleep(sleep_time)
            self.flush()

    def build_message(self) -> str:
        sb = io.StringIO()
        count = defaultdict(lambda: 0)
        min_time = None
        max_time = None
        for r in self.buffer:
            key = f"{r.filename}:{r.lineno}::{r.funcName}()"
            count[key] += 1

            if min_time is None or r.created < min_time:
                min_time = r.created
            if max_time is None or r.created > max_time:
                max_time = r.created
        min_date_str = datetime.fromtimestamp(min_time).isoformat(sep=" ", timespec="milliseconds")
        max_date_str = datetime.fromtimestamp(max_time).isoformat(sep=" ", timespec="milliseconds")

        if len(self.buffer) > 1:
            sb.write(f"Collected {len(self.buffer)} logs created between {min_date_str} and {max_date_str}\n")
        else:
            sb.write(f"Collected 1 log created at {max_date_str}\n")
        sb.write("\n")

        for k, v in count.items():
            sb.write(f"{v} - {k}\n")
        sb.write("\n")

        for r in self.buffer:
            sb.write(f"{self.format(r)}\n\n")

        sb.write("-- End of message --\n")
        return sb.getvalue()
