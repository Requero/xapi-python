from dataclasses import dataclass
from datetime import datetime

from xtb.common import FromDictMixin


@dataclass
class CalendarRecord(FromDictMixin):
    """
    Values for single Calendar record
    See http://developers.xstore.pro/documentation/#CALENDAR_RECORD
    """
    country: str
    current: str
    forecast: str
    impact: str
    period: str
    previous: str
    time: datetime
    title: str
