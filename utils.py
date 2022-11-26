from datetime import datetime, date

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"


def date_to_str(d: date):
    return d.strftime(f"{DATE_FORMAT}")


def str_to_datetime(s: str) -> datetime:
    return datetime.strptime(s, f"{DATE_FORMAT} {TIME_FORMAT}")


def datetime_to_timestamp(d: datetime) -> int:
    return int(d.timestamp() * 1000)