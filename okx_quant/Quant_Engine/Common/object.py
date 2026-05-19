from dataclasses import dataclass, field
from typing import Optional

from datetime import datetime
from Quant_Engine.Common.constants import Exchange, Interval
import json

@dataclass
class BaseData:
    """
    Any data object needs a gateway_name as source
    and should inherit base data.
    """

    gateway_name: str

    extra: Optional[dict] = field(default=None, init=False)

@dataclass
class BarData(BaseData):
    """
    Candlestick bar data of a certain trading period.
    """

    symbol: str
    exchange: Exchange
    datetime: datetime

    interval: Interval = None
    volume: float = 0
    turnover: float = 0
    open_price: float = 0
    high_price: float = 0
    low_price: float = 0
    close_price: float = 0

    def __post_init__(self) -> None:
        """"""
        self.vt_symbol: str = f"{self.symbol}.{self.exchange.value}"

@dataclass
class Position(BaseData):
    symbol: str
    insType: str
    mgnMode: str  # 保证金模式
    posId: str
    posSide: str
    pos: str  # 持仓数量
    availPos: str  # 可平数量
    avgPx: str  # 均价
    upl: str
    uplRatio: str
    lever: str
    liqPx: str
    markPx: str
    notionalUsd: str  # 以美金价值为单位的持仓数量
    adl: str

class Base_Message:
    def __init__(self, data):
        self._data = data
        self.code = self._data['code']
        self.data = self._data['data']
        self.massage = self._data['msg']
class Strategy_Message(Base_Message):
    def __init__(self, data):
        super().__init__(data)
        self.userId = self.data['id']
        self.account = json.loads(self.data['account'])
        self.lever = self.data['lever']
        self.max_position = self.data['maxPosition']
        self._args = self.data['args']
        self._args = json.loads(self._args)
        if 'pv' in self._args:
            self.pv = self._args['pv']
            self.symbol_selection = self._args['symbol_selection']
            self.open_position = self._args['open_position']
            self.profit_loss = self._args['profit_loss']
            self.fund = self._args['fund']
            self._funDict = self.data['funDict']
            self._funDict = json.loads(self._funDict)
            self.funSymbol_selection = self._funDict['symbol_selection']
            self.funProfit_loss = self._funDict['profit_loss']
            self.funFund = self._funDict['fund']
        else:
            self.pv = ""
            self.symbol_selection = self._args['symbol_selection']
            self.open_position = self._args['open_position']
            self.profit_loss = self._args['profit_loss']
            self.fund = self._args['fund']
            self._funDict = self.data['funDict']
            self._funDict = json.loads(self._funDict)
            self.funSymbol_selection = self._funDict['symbol_selection']
            self.funOpen_position = self._funDict['open_position']
            self.funProfit_loss = self._funDict['profit_loss']
            self.funFund = self._funDict['fund']


@dataclass
class User(BaseData):
    userId: str
    exchange: str
    action: dict




@dataclass
class Order(BaseData):
    ...
