from ._base import BaseRecord


class CommissionRecord(BaseRecord):
    commission: float
    rateOfExchange: float
