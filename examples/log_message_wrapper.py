import logging

from src.logdog import JsonEncoder, LogMessageWrapper

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s : %(levelname)-8s : %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# usage
log = LogMessageWrapper(
    logger,
    prefix=" : ",
    # encoder=JsonEncoder(),  # uncomment to use different encoder
)

log.logger.info("You can access logger")
# 2023-09-05 12:24:40,146 : INFO     : You can access logger
log.info("Message without kwargs")
# 2023-09-05 12:24:40,146 : INFO     : Message without kwargs

log.info(
    "basic usage",
    str="string",
    str_space="some string",
    int=1,
    float=1.0,
    bool_t=True,
    bool_f=False,
    none=None,
)
# 2023-09-05 12:24:40,147 : INFO     : basic usage : str=string str_space="some string" int=1 float=1.0 bool_t=true bool_f=false none=null

try:
    1 / 0
except ZeroDivisionError:
    log.exception("exception message", key="value")
# 2023-09-05 12:24:40,147 : ERROR    : exception message : key=value
# Traceback (most recent call last):
#   File ".../examples/log_message_wrapper.py", line 75, in <module>
#     1 / 0
# ZeroDivisionError: division by zero
