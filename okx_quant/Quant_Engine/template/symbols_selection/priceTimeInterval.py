import time
from decimal import Decimal
from Quant_Engine.utils import get_usdt_cny, retry_on_exception_sync

import okx.Market_api as Market
class priceTimeInterval:
    def __init__(self, symbol_count: int, update_interval: int):
        self.symbol_count = int(symbol_count)
        self.market = Market.MarketAPI(True)
        self.old_time = int(time.time())
        self.update_interval = int(update_interval)  # 分钟
        self.init = False

    def _check_time(self):
        if not self.init:
            self.init = True
            return True
        new_time = int(time.time())
        if new_time - self.old_time >= self.update_interval * 60 * 10:
            self.old_time = new_time
            return True
        return False

    @retry_on_exception_sync
    def filter_symbolByVolCcy24h(self, trade: int, only_symbol=True):
        # mode = "value"数值 “percnet”百分比
        if not self._check_time():
            return None
        symbol = []
        datas = None
        usdt_cny = get_usdt_cny()
        sym = self.market.get_tickers(instType='SWAP')
        if len(sym) > 0 and isinstance(sym, dict):
            datas = sym.get('data', [])
            filtered_data = [
                {'instId': d['instId'], 'last': d['last'], 'volCcy24h': d['volCcy24h'], 'high24h': d['high24h'], 'low24h': d['low24h'], 'open24h': d['open24h']}
                for d in datas
                if d['last'] and d['volCcy24h'] != 0 and d['high24h'] and d['high24h'] != 0 and d['low24h'] and d['low24h'] != 0 and d['open24h'] and d['open24h'] != 0  # 判断 d['last'] 非空且 d['volCcy24h'] 不为 0
            ]
            filtered = None

            sorted_data = sorted(filtered_data, key=lambda d: Decimal(d["last"]) * Decimal(d["volCcy24h"]),
                                 reverse=True)
            filtered = filter(lambda d: Decimal(d["last"]) * Decimal(d["volCcy24h"]) * Decimal(usdt_cny) > Decimal(
                trade), sorted_data)

            if only_symbol and filtered:
                for d in filtered:
                    symbol.append((d["instId"]))
                symbol = [s for s in symbol if s.split('-')[1] == 'USDT']
            else:
                for d in filtered:
                    symbol.append((d["instId"], d["last"]))
                symbol = [s[0:2] for s in symbol if s[0].split('-')[1] == 'USDT']

            symbols = symbol[:]
            if self.symbol_count is None:
                return symbols

            return symbols[:self.symbol_count]

    def filter_symbolByPercentCcy24h(self, trade: float, only_symbol=True):
        # mode = "value"数值 “percnet”百分比
        if not self._check_time():
            return None
        symbol = []
        datas = None
        usdt_cny = get_usdt_cny()
        sym = self.market.get_tickers(instType='SWAP')
        if len(sym) > 0 and isinstance(sym, dict):
            datas = sym.get('data', [])
            filtered_data = [
                {'instId': d['instId'], 'last': d['last'], 'volCcy24h': d['volCcy24h'], 'high24h': d['high24h'], 'low24h': d['low24h'], 'open24h': d['open24h']}
                for d in datas
                if d['last'] and d['volCcy24h'] != 0 and d['high24h'] and d['high24h'] != 0 and d['low24h'] and d['low24h'] != 0 and d['open24h'] and d['open24h'] != 0  # 判断 d['last'] 非空且 d['volCcy24h'] 不为 0
            ]
            filtered = None

            sorted_data = sorted(filtered_data, key=lambda d: (Decimal(d['high24h']) - Decimal(d["low24h"]) / Decimal(d['open24h'])),
                                 reverse=True)
            filtered = filter(lambda d: (Decimal(d['high24h']) - Decimal(d["low24h"])) / Decimal(d['open24h']) > Decimal(
                trade), sorted_data)
            if only_symbol and filtered:
                for d in filtered:
                    symbol.append((d["instId"]))
                symbol = [s for s in symbol if s.split('-')[1] == 'USDT']
            else:
                for d in filtered:
                    symbol.append((d["instId"], d["last"]))
                symbol = [s[0:2] for s in symbol if s[0].split('-')[1] == 'USDT']

            symbols = symbol[:]
            if self.symbol_count is None:
                return symbols

            return symbols[:self.symbol_count]
