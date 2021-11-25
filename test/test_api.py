import os

import pytest
from pytest_mock import MockerFixture
from xtb import XtbApi
from xtb.exceptions import XtbApiError, XtbSocketError
from xtb.connector import SyncConnector
from xtb.records import CalendarRecord, SymbolRecord


USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']


@pytest.fixture(scope='module')
def api():
    with XtbApi() as api:
        api.login(user=USER, password=PASSWORD)
        yield api


def test_connect_raise():
    api = XtbApi()
    api.connect()
    expected_msg = r'Tried to connect\(\) without calling close\(\)'
    with pytest.raises(XtbSocketError, match=expected_msg):
        api.connect()
    api.close()


def test_close_raise():
    api = XtbApi()
    api.connect()
    api.close()
    expected_msg = r'Tried to close\(\) without calling connect\(\)'
    with pytest.raises(XtbSocketError, match=expected_msg):
        api.close()


def test_login():
    with XtbApi() as api:
        out = api.login(user=USER, password=PASSWORD, app_name='Test')
        assert out['status']
        assert 'streamSessionId' in out


def test_logout():
    with XtbApi() as api:
        api.login(user=USER, password=PASSWORD)
        out = api.logout()
    assert out == {'status': True}


def test_api_no_connect():
    api = XtbApi()
    expected_msg = r'Tried to use the API without calling connect\(\) first'
    with pytest.raises(XtbSocketError, match=expected_msg):
        api.get_all_symbols()


def test_api_raises_error(api: XtbApi, mocker: MockerFixture):
    code = 'Dummy code'
    descr = 'Dummy description'
    return_value = {'status': False, 'errorCode': code, 'errorDescr': descr}
    mocker.patch.object(api._connector, '_send_packet')
    mocker.patch.object(
        api._connector, '_get_response', return_value=return_value
    )

    expected_msg = f'There was an error connecting to the API. {code}: {descr}'
    with pytest.raises(XtbApiError, match=expected_msg) as ex:
        api.get_calendar()
        assert ex.value.code == code
        assert ex.value.description == descr


def test_get_all_symbols(api: XtbApi):
    symbols = api.get_all_symbols()
    assert isinstance(symbols, list)
    assert all(isinstance(symbol, SymbolRecord) for symbol in symbols)


def test_get_calendar(api: XtbApi):
    calendar = api.get_calendar()
    assert isinstance(calendar, list)
    assert all(isinstance(event, CalendarRecord) for event in calendar)


def test_get_symbol(api: XtbApi):
    symbol = api.get_symbol('EURPLN')
    assert isinstance(symbol, SymbolRecord)
    assert symbol.symbol == 'EURPLN'
