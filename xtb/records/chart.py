from __future__ import annotations

from datetime import datetime
from typing import List

from xtb.records._base import BaseRecord


class ChartResponse(BaseRecord):
    digits: int
    exemode: int
    rateInfos: List[ChartRateInfoRecord]


class ChartRateInfoRecord(BaseRecord):
    """
    Values for Rate Info Record
    See http://developers.xstore.pro/documentation/#RATE_INFO_RECORD
    """
    close: float
    ctm: datetime
    ctmString: str
    high: float
    low: float
    open: float
    vol: float


ChartResponse.update_forward_refs()
