from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel


class ChartResponse(BaseModel):
    digits: int
    exemode: int
    rateInfos: List[ChartRateInfoRecord]


class ChartRateInfoRecord(BaseModel):
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
