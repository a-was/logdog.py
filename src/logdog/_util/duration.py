import re


def parse_duration(duration: str) -> int:
    matches = re.findall(r"(\d+)([smh])", duration)
    multipliers = {
        "s": 1,
        "m": 60,
        "h": 60 * 60,
    }

    seconds = 0
    for value, unit in matches:
        seconds += int(value) * multipliers[unit]
    return seconds
