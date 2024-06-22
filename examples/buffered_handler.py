import logging
import logging.config
import random
import time
from datetime import timedelta

from src.logdog import BufferedGoogleChatHandler, BufferedSmtpHandler

formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

google = BufferedGoogleChatHandler(
    webhook_url="MY_WEBHOOK_URL",
    capacity=None,
    flush_interval=timedelta(minutes=15),
    starting_times=10,
    starting_interval="45s",
)
google.setLevel(logging.INFO)
google.setFormatter(formatter)

# smtp = BufferedSmtpHandler(
#     host="localhost",
#     port=25,
#     # user="",
#     # password="",
#     sender="sender <server@example.com>",
#     receivers=["me@example.com"],
#     subject="Server Error Report",
#     # use_starttls=True,
#     # use_ssl=False,
#     capacity=None,
#     flush_interval=timedelta(minutes=15),
#     starting_times=10,
#     starting_interval=timedelta(minutes=1),
# )
# smtp.setLevel(logging.INFO)
# smtp.setFormatter(formatter)

log = logging.getLogger(__name__)

log.setLevel(logging.INFO)
log.addHandler(console)
log.addHandler(google)
# log.addHandler(smtp)


def main():
    while True:
        short_sleep_times = random.randint(4, 10)
        for _ in range(short_sleep_times):
            try:
                1 / 0
            except ZeroDivisionError:
                log.exception("zero raised")

            sleep_seconds = random.randint(5, 120)
            print(f"Sleeping for {sleep_seconds} seconds")
            time.sleep(sleep_seconds)
        long_sleep = random.randint(15, 20)
        print(f"Sleeping for {long_sleep} minutes")
        time.sleep(long_sleep * 60)


if __name__ == "__main__":
    main()
