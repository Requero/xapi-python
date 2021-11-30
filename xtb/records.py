from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar

from pydantic import BaseModel


class BaseRecord(BaseModel):
    @classmethod
    def from_dict(cls, dictionary: Dict[Any, Any]):
        return cls(**dictionary)  # noqa


GenericRecord = TypeVar('GenericRecord', bound=BaseRecord)


def cast_to_collection_of(
        type_: Type[GenericRecord],
        value: Dict[Any, Any],
) -> List[GenericRecord]:
    """
    Casts the dictionary to the list of BaseRecords
    """
    return list(map(type_.from_dict, value))


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


class ChartResponse(BaseRecord):
    """
    Response for chart commands. See:
    http://developers.xstore.pro/documentation/#getChartLastRequest
    http://developers.xstore.pro/documentation/#getChartRangeRequest
    """
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


class CommissionRecord(BaseRecord):
    """
    Values for Commision Record
    See http://developers.xstore.pro/documentation/#getCommissionDef
    """
    commission: float
    rateOfExchange: float


class SymbolRecord(BaseRecord):
    """
    Values for single Symbol record
    See http://developers.xstore.pro/documentation/#SYMBOL_RECORD
    """
    ask: float
    bid: float
    categoryName: str
    contractSize: int
    currency: str
    currencyPair: bool
    currencyProfit: str
    description: str
    expiration: Optional[datetime]
    groupName: str
    high: float
    initialMargin: int
    instantMaxVolume: int
    leverage: float
    longOnly: bool
    lotMax: float
    lotMin: float
    lotStep: float
    low: float
    marginHedged: int
    marginHedgedStrong: bool
    marginMaintenance: int
    marginMode: int
    percentage: float
    pipsPrecision: int
    precision: int
    profitMode: int
    quoteId: int
    shortSelling: bool
    spreadRaw: float
    spreadTable: float
    starting: Optional[datetime]
    stepRuleId: int
    stopsLevel: int
    swap_rollover3days: int
    swapEnable: bool
    swapLong: float
    swapShort: float
    swapType: int
    symbol: str
    tickSize: float
    tickValue: float
    time: datetime
    timeString: str
    trailingEnabled: bool
    type: int


ChartResponse.update_forward_refs()
