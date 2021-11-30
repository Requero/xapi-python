from datetime import datetime
from typing import Optional

from xtb.records._base import BaseRecord


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
