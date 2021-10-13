from dataclasses import dataclass, is_dataclass

from xtb.common import DataclassWithKwargs


class _DummyClass(DataclassWithKwargs):
    foo: str
    bar: str


def test_is_dataclass_when_created():
    assert is_dataclass(_DummyClass(foo='foo', bar='bar'))


def test_dataclass_is_still_dataclass_when_created():
    @dataclass
    class _DummyClassSecond(DataclassWithKwargs):
        foo: str

    assert is_dataclass(_DummyClassSecond(foo='a'))


def test_can_create_without_kwargs():
    instance = _DummyClass(foo='foo', bar='bar')
    assert instance.foo == 'foo'
    assert instance.bar == 'bar'
    assert instance.additional_kwargs == {}


def test_can_create_with_additional_kwargs():
    instance = _DummyClass(
        foo='foo', bar='bar', something='new', again='new2',
    )
    assert instance.foo == 'foo'
    assert instance.bar == 'bar'
    assert instance.additional_kwargs == {'something': 'new', 'again': 'new2'}
