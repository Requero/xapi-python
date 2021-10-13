from datetime import datetime

from xtb.records._base import BaseRecord


class CalendarRecord(BaseRecord):
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
