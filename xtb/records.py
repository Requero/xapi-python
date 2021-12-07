from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar

from pydantic import BaseModel, Field


class BaseRecord(BaseModel):
    @classmethod
    def from_dict(cls, dictionary: Dict[Any, Any]):
        return cls(**dictionary)  # noqa

    @classmethod
    def create_collection_from(cls, value: Dict[Any, Any]) -> List[Generic]:
        """
        Casts the dictionary to the list of this type
        """
        return list(map(cls.from_dict, value))


Generic = TypeVar('Generic', bound=BaseRecord)


class Calendar(BaseRecord):
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
    rateInfos: List[ChartRateInfo]


class ChartRateInfo(BaseRecord):
    """
    Values for Rate Info 
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


class Commission(BaseRecord):
    """
    Values for Commision 
    See http://developers.xstore.pro/documentation/#getCommissionDef
    """
    commission: float
    rateOfExchange: float


class User(BaseRecord):
    """
    Values for Current User Data
    See http://developers.xstore.pro/documentation/#getCurrentUserData
    """
    companyUnit: int
    currency: str
    group: str
    ibAccount: bool
    leverage: int
    leverageMultiplier: float
    spreadType: Optional[str]
    trailingStop: bool


class MarginLevel(BaseRecord):
    """
    Values for Margin Level
    See http://developers.xstore.pro/documentation/#getMarginLevel
    """
    balance: float
    credit: float
    currency: str
    equity: float
    margin: float
    margin_free: float
    margin_level: float


class MarginTrade(BaseRecord):
    """
    Values for Margin Trade
    See http://developers.xstore.pro/documentation/#getMarginTrade
    """
    margin: float


class News(BaseRecord):
    """
    Values for News
    See http://developers.xstore.pro/documentation/#NEWS_TOPIC_RECORD
    """
    body: str
    bodylen: int
    key: str
    time: datetime
    timeString: str
    title: str


class ProfitCalculation(BaseRecord):
    """
    Values for profit calculation
    See http://developers.xstore.pro/documentation/#getProfitCalculation
    """
    profit: float


class ServerTime(BaseRecord):
    """
    Values for server time
    See http://developers.xstore.pro/documentation/#getServerTime
    """
    time: datetime
    time_string: str = Field(alias='timeString')


class StepRule(BaseRecord):
    """
    Values for step rule
    See http://developers.xstore.pro/documentation/#STEP_RULE_RECORD
    """
    id: int
    name: str
    steps: List[Step]


class Step(BaseRecord):
    """
    Values for single step
    See http://developers.xstore.pro/documentation/#STEP_RECORD
    """
    from_value: float = Field(alias='fromValue')
    step: float


StepRule.update_forward_refs()


class Symbol(BaseRecord):
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


class TickPrices(BaseRecord):
    """
    Values for tick prices
    See http://developers.xstore.pro/documentation/#getTickPrices
    """
    quotations: List[Tick]


class Tick(BaseRecord):
    """
    Value for single Tick
    See http://developers.xstore.pro/documentation/#TICK_RECORD
    """
    ask: float
    ask_volume: int = Field(alias='askVolume')
    bid: float
    bid_volume: float = Field(alias='bidVolume')
    high: float
    level: int
    low: float
    spread_raw: float = Field(alias='spreadRaw')
    spread_table: float = Field(alias='spreadTable')
    symbol: str
    timestamp: datetime


TickPrices.update_forward_refs()


class Trade(BaseRecord):
    """
    A single Trade record
    See http://developers.xstore.pro/documentation/#TRADE_RECORD
    """
    close_price: float
    close_time: Optional[datetime]
    close_time: Optional[str]
    closed: bool
    cmd: int
    comment: str
    commission: Optional[float]
    custom_comment: Optional[str] = Field(alias='customComment')
    digits: int
    expiration: Optional[datetime]
    expiration_string: Optional[str] = Field(alias='expirationString')
    margin_rate: float
    offset: int
    open_price: float
    open_time: datetime
    open_time_string: str = Field(alias='open_timeString')
    order: int
    order2: int
    position: int
    profit: float
    sl: float = 0
    storage: float
    symbol: Optional[str]
    timestamp: datetime
    tp: float = 0
    volume: float


class TradingHours(BaseRecord):
    """
    Trading hours record
    See http://developers.xstore.pro/documentation/#TRADING_HOURS_RECORD
    """
    quotes: List[Quotes]
    symbol: str
    trading: List[Trading]


class Quotes(BaseRecord):
    """
    Quotes record
    See http://developers.xstore.pro/documentation/#QUOTES_RECORD
    """
    day: int
    from_t: datetime = Field(alias='fromT')
    to_t: datetime = Field(alias='toT')


class Trading(BaseRecord):
    """
    Trading record
    See http://developers.xstore.pro/documentation/#TRADING_RECORD
    """
    day: int
    from_t: datetime = Field(alias='fromT')
    to_t: datetime = Field(alias='toT')


TradingHours.update_forward_refs()


class Version(BaseRecord):
    """
    API Version
    See http://developers.xstore.pro/documentation/#getVersion
    """
    version: str


class TradeInfo(BaseRecord):
    """
    Used as an argument for starting a transaction
    See http://developers.xstore.pro/documentation/#TRADE_TRANS_INFO
    """
    cmd: int
    custom_comment: Optional[str] = Field(alias='customComment')
    expiration: datetime
    offset: int
    order: int = 0
    price: float
    sl: float
    symbol: str
    tp: float
    type: int
    volume: float


class TradeOrder(BaseRecord):
    """
    Result after a transaction
    See http://developers.xstore.pro/documentation/#tradeTransaction
    """
    order: int


class TradeStatus(BaseRecord):
    """
    A status of a transaction
    See http://developers.xstore.pro/documentation/#tradeTransactionStatus
    """
    ask: float
    bid: float
    custom_comment: Optional[str] = Field(alias='customComment')
    message: Optional[str]
    order: int
    request_status: int = Field(alias='requestStatus')
