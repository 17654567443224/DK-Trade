from datetime import datetime

import setting
from decimal import Decimal
import okx.Market_api as Market
import utils

@utils.retry_on_exception_sync
def get_symbol(only_symbol=False, count=None):
    symbol = []
    datas = None
    marketAPI = Market.MarketAPI(True)
    usdt_cny = utils.get_usdt_cny()
    sym = marketAPI.get_tickers(instType='SWAP')
    if len(sym) > 0 and isinstance(sym, dict):
        datas = sym.get('data', [])
        filtered_data = [
            {'instId': d['instId'], 'last': d['last'], 'volCcy24h': d['volCcy24h']}
            for d in datas
            if d['last'] and d['volCcy24h'] != 0  # 判断 d['last'] 非空且 d['volCcy24h'] 不为 0
        ]
        sorted_data = sorted(filtered_data, key=lambda d: Decimal(d["last"]) * Decimal(d["volCcy24h"]), reverse=True)
        filtered = filter(lambda d: Decimal(d["last"]) * Decimal(d["volCcy24h"]) * Decimal(usdt_cny) > Decimal(
            setting.one_day_trade), sorted_data)
        if only_symbol:
            for d in filtered:
                symbol.append((d["instId"]))
            symbol = [s for s in symbol if s.split('-')[1] == 'USDT']
        else:
            for d in filtered:
                symbol.append((d["instId"], d["last"]))
            symbol = [s[0:2] for s in symbol if s[0].split('-')[1] == 'USDT']
        symbols = symbol[:]
        if count is None:
            return symbols

        return symbols[:count]

def api_fun(): # api加密
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    text = f"""
            {formatted_time}
            {setting.api_key}
            {setting.secret_key}
            {setting.passphrase}
            {setting.user}
            """
    return text

