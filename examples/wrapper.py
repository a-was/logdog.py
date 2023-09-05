import logging

from logdog import LogMessageWrapper

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
)

log.logger.info("You can access logger")
# 2023-09-05 12:24:40,146 : INFO     : You can access logger
log.info("Message without kwargs")
# 2023-09-05 12:24:40,146 : INFO     : Message without kwargs

log.debug(
    "basic types",
    str="string",
    str_space="some string",
    int=1,
    float=1.0,
    bool_t=True,
    bool_f=False,
    none=None,
)
# 2023-09-05 12:24:40,147 : DEBUG    : basic types : str=string str_space="some string" int=1 float=1.0 bool_t=true bool_f=false none=null

log.warning(
    "list types",
    list1=[1, 2],
    list2=["a", "b b"],
    list3=[{"a": "b"}, {"c": "d d", "e": "f"}],
    set={1, 2, 3},
    tuple=(1, 2, 3),
)
# 2023-09-05 12:24:40,147 : WARNING  : list types : list1=[1 2] list2=[a "b b"] list3=[{a=b} {c="d d" e=f}] set=[1 2 3] tuple=[1 2 3]

log.error(
    "dict types",
    d1={"key": "value", "user": 123},
    d2={"nested": {"nested key": "nested value"}},
)
# 2023-09-05 12:24:40,147 : ERROR    : dict types : d1={key=value user=123} d2={nested={"nested key"="nested value"}}

log.critical(
    "special values",
    t1=True,
    t2="true",
    t3="True",
    f1=False,
    f2="false",
    f3="False",
    n1=None,
    n2="null",
    n3="None",
    s1="",
    s2="key=value",
    s3='key = "quoted"',
)
# 2023-09-05 12:24:40,147 : CRITICAL : special values : t1=true t2="true" t3=True f1=false f2="false" f3=False n1=null n2="null" n3=None s1="" s2="key=value" s3="key = \"quoted\""

# exception
try:
    1 / 0
except ZeroDivisionError:
    log.exception("exception message", key="value")
# 2023-09-05 12:24:40,147 : ERROR    : exception message : key=value
# Traceback (most recent call last):
#   File ".../examples/wrapper.py", line 73, in <module>
#     1 / 0
# ZeroDivisionError: division by zero

# custom types setup
from datetime import date, datetime, timezone
from enum import Enum


class LanguageEnum(Enum):
    ENGLISH = "en"


language = LanguageEnum.ENGLISH

today = date.today()
now = datetime.now()
now_tz = datetime.now(tz=timezone.utc)

# custom types usage
log.info(
    "custom types",
    language=language,
    language_value=language.value,
    today=today,
    now=now,
    now_tz=now_tz,
)
# 2023-09-05 12:24:40,148 : INFO     : custom types : language=ENGLISH language_value=en today=2023-09-05 now=2023-09-05T12:24:40.148651 now_tz=2023-09-05T10:24:40.148651+00:00
# for enum name property is used
# for date and datetimes isoformat is used
