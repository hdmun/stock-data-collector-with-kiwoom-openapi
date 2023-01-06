#!/usr/bin/python3
# -*-coding: utf-8 -*-

from PyQt5.QtCore import QEventLoop
from model import StockItem

from openapi import KiwoomOpenAPI, Market, ResponseError


ERROR_CONNECT_USER = -100 # 사용자 정보교환 실패
ERROR_CONNECT_SERVER = -101 # 서버접속 실패
ERROR_CONNECT_VERSION = -102 # 버전처리 실패


class KiwoomOpenAPIClient(object):
    """'KiwoomOpenAPI' 클래스를 사용해 요청을 담당하는 클래스"""

    def __init__(self, api: KiwoomOpenAPI):
        self._api: KiwoomOpenAPI = api
        self._login_event_loop: QEventLoop = None
        self._error_code: ResponseError = ResponseError.NONE

    @property
    def connected(self) -> bool:
        return self._api.connected

    def connect(self) -> ResponseError:
        if not self._api:
            raise Exception('invalid KiwoomOpenAPI')

        self._api.set_connect_handler(self._on_connect_event)
        print('initialize KiwoomOpenAPI')

        self._api.connect()
        self._login_event_loop = QEventLoop()
        self._login_event_loop.exec_()
        return self._error_code

    def _on_connect_event(self, error_code: int):
        if error_code == 0:
            print('connected KiwoomOpenAPI')
        else:
            print(f'disconnected KiwoomOpenAPI|{error_code}')

        self._error_code = error_code
        self._login_event_loop.exit()

    def get_stock_items_by_kospi(self) -> list[StockItem]:
        return list(map(
            lambda code: StockItem(code, self._api.get_master_code_name(code)),
            self._api.get_code_list(Market.KOSPI)
        ))

    def get_stock_items_by_kosdaq(self) -> list[StockItem]:
        return list(map(
            lambda code: StockItem(code, self._api.get_master_code_name(code)),
            self._api.get_code_list(Market.KOSDAQ)
        ))

    def get_stock_items_by_futures(self) -> list[StockItem]:
        return list(map(
            lambda code: StockItem(code, self._api.get_master_code_name(code)),
            self._api.get_future_code_list()
        ))