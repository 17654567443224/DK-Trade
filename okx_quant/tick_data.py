import asyncio
import random
from functionns import setting
from okx.Market_api import MarketAPI
from decimal import Decimal

old_symbol = []

class Tick(MarketAPI):
    def __init__(self):
        MarketAPI.__init__(self)
        self.market = MarketAPI()

        self.trading_view = None
    async def get_symbol(self):
        global old_symbol
        global switch
        symbol = []
        datas = None
        sym = self.market.get_tickers(instType='SWAP')
        if len(sym) > 0 and isinstance(sym,dict):
            datas = sym.get('data', [])
        filtered_data = [{'instId': d['instId'], 'last': d['last'], 'volCcy24h': d['volCcy24h']} for d in datas]
        sorted_data = sorted(filtered_data, key=lambda d: Decimal(d["last"]) * Decimal(d["volCcy24h"]), reverse=True)
        filtered = filter(lambda d: Decimal(d["last"]) * Decimal(d["volCcy24h"]) * Decimal('6.8') > Decimal(
            setting.one_day_trade), sorted_data)
        for d in filtered:
            symbol.append((d["instId"], d["last"]))
        symbol = [s[0:2] for s in symbol if s[0].split('-')[1] == 'USDT']
        symbols = symbol[:]
        if old_symbol:
            old_symbol = dict(old_symbol)
            symbols = dict(symbols)
            matched_keys = set(old_symbol.keys()) & set(symbols.keys())
            result = {key: abs((Decimal(old_symbol[key]) - Decimal(symbols[key]))*Decimal('100')/Decimal(old_symbol[key])) for key in matched_keys}
            sorted_d = sorted(result.items(), key=lambda x: x[1], reverse=True)
            ls_sym = list(sorted_d[0])
            sym = ls_sym[0]
            cal_price = ls_sym[1]
            if cal_price > setting.cal_price:
                await self.get_Kline(sym)
            old_symbol = symbols
        else:
            old_symbol = symbols

    async def get_Kline(self, sym):
        result = self.market.get_markprice_candlesticks(sym, bar='1m', limit=4)
        bar_datas = result.get('data')[1:]
        new_bar = bar_datas[0]
        mid_bar = bar_datas[1]
        old_bar = bar_datas[2]
        new_bar_high = new_bar[2]
        new_bar_low = new_bar[3]
        mid_bar_high = mid_bar[2]
        mid_bar_low = mid_bar[3]
        old_bar_high = old_bar[2]
        old_bar_low = old_bar[3]
        return await self.get_direction(new_bar_high,new_bar_low,mid_bar_high,mid_bar_low,old_bar_high,old_bar_low)

    async def get_direction(self, new_high_, new_low_, mid_high_, mid_low_, old_high_, old_low_):
        new_high = Decimal(new_high_)
        second_high = Decimal(mid_high_)  # 最高价
        last_high = Decimal(old_high_)

        new_low = Decimal(new_low_)
        second_low = Decimal(mid_low_)  # 最低价
        last_low = Decimal(old_low_)

        max_high = max(new_high, second_high, last_high)  # 三根线中max 最高价
        max_low = max(new_low, second_low, last_low)  # 三根线中min 最低价
        min_high = min(new_high, second_high, last_high)  # 三根线中min 最高价
        min_low = min(new_low, second_low, last_low)  # 三根线中min 最低价
        if max_high == new_high and min_low == (last_low or second_low):
            trading_view = 1  # 多

        elif max_high == new_high and min_low == new_low:
            dh = max_high - min_high
            dl = max_low - min_low
            if dh > dl:
                trading_view = 1
            else:
                trading_view = 0  # 空

        elif max_high == last_high and min_low == (new_low or second_low):
            trading_view = 0

        elif max_high == last_high and min_low == last_low:
            dh = max_high - min_high
            dl = max_low - min_low
            if dh > dl:
                trading_view = 0
            else:
                trading_view = 1

        elif max_high == second_high and max_low == second_low:
            if last_low > new_low:
                trading_view = 0
            else:
                trading_view = 1

        elif max_high == second_high and max_low == last_low:
            trading_view = 0

        elif max_high == second_high and max_low == new_low:
            trading_view = 1

        elif (max_high - min_high) > (max_low - min_low):
            if max_high == new_high:
                trading_view = 1
            elif max_high == last_high:
                trading_view = 0
            elif max_high == second_high:
                trading_view = 0

        elif (max_high - min_high) < (max_low - min_low):
            if min_low == new_low:
                trading_view = 0
            elif min_low == last_low:
                trading_view = 1
            elif min_low == second_low:
                trading_view = 1
        else:
            a = [0, 1]
            trading_view = random.choice(a)

        return trading_view

if __name__ == '__main__':
    asd = Tick(setting.api_key, setting.secret_key, setting.passphrase)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asd.get_symbol())
    # while True:
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(asd.get_Kline(sym='ETH-USDT-SWAP'))
    #     time.sleep(10)
