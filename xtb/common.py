import abc
from dataclasses import dataclass, is_dataclass
from typing import Any, Dict


class DataclassWithKwargs(abc.ABC):

    def __new__(cls, *args, **kwargs):
        # Based on https://stackoverflow.com/a/63291704
        if not is_dataclass(cls):
            cls = dataclass(cls)

        try:
            initializer = cls.__initializer
        except AttributeError:
            cls.__initializer = initializer = cls.__init__
            cls.__init__ = lambda *_, **__: None

        filter_ = filter(lambda x: x not in cls.__annotations__, kwargs.keys())
        additional_kwargs = {name: kwargs.pop(name) for name in list(filter_)}
        instance = object.__new__(cls)
        initializer(instance, **kwargs)  # noqa
        setattr(instance, '_additional_kwargs', additional_kwargs)
        return instance

    @property
    def additional_kwargs(self) -> Dict[str, Any]:
        return self._additional_kwargs  # noqa


class FromDictMixin:

    @classmethod
    def from_dict(cls, dictionary: Dict[Any, Any]):
        return cls(**dictionary)  # noqa


