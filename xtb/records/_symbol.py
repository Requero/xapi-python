from dataclasses import dataclass
from datetime import datetime
from numbers import Number
from typing import Any

from xtb.common import FromDictMixin


@dataclass
class SymbolRecord(FromDictMixin):
    """
    Values for single Symbol record
    See http://developers.xstore.pro/documentation/#SYMBOL_RECORD

    exemode and quoteIdCross are not documented and had to be added
    (21.03.2021)
    """
    ask: float
    bid: float
    categoryName: str
    contractSize: Number
    currency: str
    currencyPair: bool
    currencyProfit: str
    description: str
    exemode: Any
    expiration: datetime
    groupName: str
    high: float
    initialMargin: Number
    instantMaxVolume: Number
    leverage: float
    longOnly: bool
    lotMax: float
    lotMin: float
    lotStep: float
    low: float
    marginHedged: Number
    marginHedgedStrong: bool
    marginMaintenance: Number
    marginMode: Number
    percentage: float
    pipsPrecision: Number
    precision: Number
    profitMode: Number
    quoteId: Number
    quoteIdCross: Number
    shortSelling: bool
    spreadRaw: float
    spreadTable: float
    starting: datetime
    stepRuleId: Number
    stopsLevel: Number
    swap_rollover3days: Number
    swapEnable: bool
    swapLong: float
    swapShort: float
    swapType: Number
    symbol: str
    tickSize: float
    tickValue: float
    time: datetime
    timeString: str
    trailingEnabled: bool
    type: Number
