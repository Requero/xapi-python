from typing import Any, Dict, List, Type, TypeVar

from xtb.records._base import BaseRecord
from xtb.records.calendar import CalendarRecord
from xtb.records.symbol import SymbolRecord
from xtb.records.chart import ChartResponse, ChartRateInfoRecord
from xtb.records.commission import CommissionRecord

__all__ = [
    'cast_to_collection_of', 'CalendarRecord', 'SymbolRecord',
    'ChartResponse', 'ChartRateInfoRecord', 'CommissionRecord'
]

GenericRecord = TypeVar('GenericRecord', bound=BaseRecord)


def cast_to_collection_of(
        type_: Type[GenericRecord],
        value: Dict[Any, Any],
) -> List[GenericRecord]:
    """
    Casts the dictionary to the list of BaseRecords
    """
    return list(map(type_.from_dict, value))
