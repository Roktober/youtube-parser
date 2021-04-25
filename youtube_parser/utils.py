from datetime import datetime
import dateutil.parser


def to_rfc_339_time(t: datetime) -> str:
    if not t.tzinfo:
        raise ValueError('Not tz info')
    return t.isoformat(sep='T')


def from_iso_8601(date: str) -> datetime:
    return dateutil.parser.isoparse(date)
