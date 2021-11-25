from typing import Any, Dict

from pydantic import BaseModel


class BaseRecord(BaseModel):
    @classmethod
    def from_dict(cls, dictionary: Dict[Any, Any]):
        return cls(**dictionary)  # noqa
