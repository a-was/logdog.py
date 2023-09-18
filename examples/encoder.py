from datetime import date, datetime, timezone
from enum import Enum

from src.logdog import JsonEncoder, LogfmtEncoder

encoder = LogfmtEncoder()
# encoder = JsonEncoder()


print("basic types:")
obj = {
    "str": "string",
    "str_space": "some string",
    "int": 1,
    "float": 1.0,
    "bool_t": True,
    "bool_f": False,
    "none": None,
}
print(encoder.encode(obj))
# str=string str_space="some string" int=1 float=1.0 bool_t=true bool_f=false none=null

print("list types:")
obj = {
    "list1": [1, 2],
    "list2": ["a", "b b"],
    "list3": [{"a": "b"}, {"c": "d d", "e": "f"}],
    "tuple": (1, 2, 3),
}
print(encoder.encode(obj))
# list1=[1 2] list2=[a "b b"] list3=[{a=b} {c="d d" e=f}] tuple=[1 2 3]

print("dict types:")
obj = {
    "d1": {"key": "value", "user": 123},
    "d2": {"nested": {"nested key": "nested value"}},
}
print(encoder.encode(obj))
# d1={key=value user=123} d2={nested={"nested key"="nested value"}}

print("special values:")
obj = {
    "t1": True,
    "t2": "true",
    "t3": "True",
    "f1": False,
    "f2": "false",
    "f3": "False",
    "n1": None,
    "n2": "null",
    "n3": "None",
    "s1": "",
    "s2": "key=value",
    "s3": 'key = "quoted"',
}
print(encoder.encode(obj))
# t1=true t2="true" t3=True f1=false f2="false" f3=False n1=null n2="null" n3=None s1="" s2="key=value" s3="key = \"quoted\""

print("custom types:")


class LanguageEnum(Enum):
    ENGLISH = "en"


language = LanguageEnum.ENGLISH

today = date.today()
now = datetime.now()
now_tz = datetime.now(tz=timezone.utc)

obj = {
    "language": language,
    "language_value": language.value,
    "today": today,
    "now": now,
    "now_tz": now_tz,
}
print(encoder.encode(obj))
# language=ENGLISH language_value=en today=2023-09-05 now=2023-09-05T12:23:56.860436 now_tz=2023-09-05T10:23:56.860436+00:00
# for json:
# {"language": "ENGLISH", "language_value": "en", "today": "2023-09-05", "now": "2023-09-05T12:25:51.199612", "now_tz": "2023-09-05T10:25:51.199612+00:00"}
