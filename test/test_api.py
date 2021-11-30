import os

import pytest
from pytest_mock import MockerFixture
from xtb import XtbApi, records
from xtb.exceptions import XtbApiError, XtbSocketError


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
    assert all(isinstance(symbol, records.SymbolRecord) for symbol in symbols)


def test_get_calendar(api: XtbApi):
    calendar = api.get_calendar()
    assert isinstance(calendar, list)
    assert all(isinstance(event, records.CalendarRecord) for event in calendar)


def test_get_symbol(api: XtbApi):
    symbol = api.get_symbol('EURPLN')
    assert isinstance(symbol, records.SymbolRecord)
    assert symbol.symbol == 'EURPLN'


def test_get_chart_last_request(api: XtbApi):
    last_request = api.get_chart_last_request(
        period=5, start=1637698293552, symbol='EURUSD'
    )
    assert isinstance(last_request, records.ChartResponse)


def test_get_chart_range_request(api: XtbApi):
    range_request = api.get_chart_range_request(
        end=1262944412000, period=5, start=1262944112000,
        symbol='EURUSD', ticks=0
    )
    assert isinstance(range_request, records.ChartResponse)


def test_get_commission_def(api: XtbApi):
    comm = api.get_commission_def('EURPLN', 1)
    assert isinstance(comm, records.CommissionRecord)
    assert comm.commission == 0.0
    assert comm.rateOfExchange == 1.0
