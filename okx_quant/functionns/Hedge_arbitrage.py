import sys
import asyncio
import base64
import datetime
import hmac
import json
import time
import zlib
import setting
import requests
import websockets
import threading
import deal_data
from typing import Optional
import okx.Market_api as Market
import okx.Account_api as Account
import okx.Public_api as Public
from decimal import Decimal
from enum import Enum
from utils import deal_message,  retry_on_exception_sync, retry_on_exception_decorator
from queue import Queue
import okx.Trade_api as Trade
import math
import spot_symbol_trade as sp
from wx_webhook import wx_robot
from datetime import datetime
if sys.platform == "win32" and sys.version_info >= (3, 8, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
class Interval(Enum):
    CANDLE_3M = "candle3M"
    CANDLE_1M = "candle1M"
    CANDLE_1W = "candle1W"
    CANDLE_1D = "candle1D"
    CANDLE_2D = "candle2D"
    CANDLE_3D = "candle3D"
    CANDLE_5D = "candle5D"
    CANDLE_12H = "candle12H"
    CANDLE_6H = "candle6H"
    CANDLE_4H = "candle4H"
    CANDLE_2H = "candle2H"
    CANDLE_1H = "candle1H"
    CANDLE_30m = "candle30m"
    CANDLE_15m = "candle15m"
    CANDLE_5m = "candle5m"
    CANDLE_3m = "candle3m"
    CANDLE_1m = "candle1m"

class websocket_funs:
    def __init__(self, user):
        self.load_interval = setting.load_interval
        self.liqpx_slip = setting.liqpx_slip
        self.Trigger_slip = setting.Trigger_slip
        self.order_wait_time = setting.order_wait_time
        self.quick_tradingview = setting.quick_tradingview
        self.profit_per = setting.profit_per
        self.stop_loss = setting.stop_loss
        self.position_update = setting.position_update
        self.profit_min = setting.profit_min
        self.float_val = setting.float_val
        self.one_day_trade = setting.one_day_trade
        self.marketAPI = Market.MarketAPI(True)
        self.accountAPI = Account.AccountAPI()
        self.symbol_ls = []
        self.avg_switch = False
        self.start_time: Optional[time]
        self.publicAPI = Public.PublicAPI(False)
        self.tradeAPI = Trade.TradeAPI(False)
        self.accountAPI.get_position_mode('long_short_mode')
        self.order_switch = False
        self.strike_sym_ls = []
        self.order_ls = []  # positions_history_data
        self.order_dict = {}  # （Order sent, transaction unknown）
        self.order_algo = []  # Dict of stop loss and stop loss orders
        self.fluctuation_values = {}  # kline_dym_dice，if ...
        self.get_pnl_ls()
        self.price_dict = None
        self.multiplier = self.iniy_multiplier()
        self.demultiplier = self.multiplier
        self.init_ba = self.get_banlance_all()
        if setting.hedge_switch:
            self.init_ba = self.init_ba / Decimal('2')
        self.trade_switch = True
        self.ignore_temp = []
        self.profit_switch = False
        self.spot_order = {}
        self.position_time = 0
        self.spot_num = 0
        self.spot_price_dict = {}
        self.spot_profit_dict = {}
        self.spot_ls = []
        self.target_switch = False
        self.wx = wx_robot(user)
        self.wx_switch = False
        self.symbol_temp = []
        self.order_count = 0
        self.Pos_temp = None
    @retry_on_exception_sync
    def cancel_wait_order(self):
        time.sleep(0.1)
        result = deal_message(self.tradeAPI.get_order_list(instType='SWAP', uly='', instFamily='', instId='', ordType='limit', state='', after='',
                                         before='', limit=''))
        if result:
            for i in result:
                if i.get('state') == 'live':
                    ordId = i.get('ordId')
                    sym = i.get('instId')
                    u_time = int(i.get('cTime')) / 1000
                    e_time = int(time.time()) - int(u_time)
                    if e_time > self.order_wait_time and sym in self.order_dict and i['algoId'] == '':
                        res = deal_message(self.tradeAPI.cancel_order(sym, ordId=ordId))
                        if res[0].get('sMsg') == "":
                            print("cancel_order_success")
                            self.trade_switch = True
                            if sym in self.order_dict:
                                del self.order_dict[sym]
                        else:
                            print("cancel_order_failed")
            return 1

    def get_pnl_ls(self):
        #  10s/1request	 String		type1：part_close;2：all_close;3：break_pos;4：loss_pos; 5：ADL;
        if setting.fail_count_reset == True:
            return
        while True:
            try:
                print("load_position")
                res = deal_message(
                    self.accountAPI.get_positions_history(instType='SWAP', instId='', mgnMode='isolated', type='2',
                                                          after=self.get_server_time(), before='',
                                                          limit='', posId=''))
                if res:
                    for i in res:
                        r = i.get('pnl')
                        self.order_ls.append(r)
                    print("load_position_finish")
                    break
            except:
                print("inter_lag")
                time.sleep(10)

    def get_price(self, symbol: list, q: Queue):  # load_interval：cal_kline_count
        """
        Return the dict composed of symbol and avg
        :param symbol:
        :return:
        """
        self.spot_price_dict = {}
        result = None
        count = 0
        price_ls = []
        cal_ls = []
        self.fluctuation_values = {}
        for i in symbol:
            count += 1
            if count % 20 == 0:
                time.sleep(0.2)
            while True:
                try:
                    res = self.marketAPI.get_markprice_candlesticks(instId=i, limit=self.load_interval, bar=setting.rest_interval)
                    code = res.get('code')
                    if code == '0':
                        result = deal_message(res)
                        break
                    else:
                        print(code)
                        symbol.remove(i)
                except:
                    time.sleep(2)
                    continue
            self.spot_price_dict[i] = result
            max_high_price = max(Decimal(res_max[2]) for res_max in result)
            min_low_price = min(Decimal(res_min[3]) for res_min in result)
            max_low_price = max(Decimal(res_min[3]) for res_min in result)  # max(low)o h l c
            min_high_price = min(Decimal(res_max[2]) for res_max in result)  # min(max)
            cal_price = (max_high_price + min_low_price) / Decimal(2)
            if (max_high_price - min_high_price) > Decimal(self.quick_tradingview)*cal_price and (max_low_price - min_low_price) > Decimal(self.quick_tradingview)*cal_price:
                max_high_price = max_high_price * (Decimal("1") - Decimal(self.liqpx_slip))
                min_low_price = min_low_price * (Decimal("1") + Decimal(self.liqpx_slip))
            cal_ls.append((max_high_price - min_low_price) / ((max_high_price + min_low_price) / Decimal(2)))
            price_ls.append([max_high_price, min_low_price])
        self.fluctuation_values = dict(zip(symbol, cal_ls))
        print("success_get_symbol")
        sym_avg_dict = dict(zip(symbol, price_ls))
        self.Dynamic_tuning()
        q.put(sym_avg_dict)

    def symbol_monitor(self, interval: Interval):
        """
        base: mark_price_?interval
        :return:
        """
        thread = threading.Thread(target=self.order_monitor)
        thread.start()
        while True:
            symbol_ls = deal_data.get_symbol(only_symbol=True, count=setting.symbol_count)
            self.symbol_ls = symbol_ls
            print("symbol_monitor")
            thread = threading.Thread(target=self.run_public_thread, args=(symbol_ls, interval.value,))
            thread.start()
            thread.join()

    def run_public_thread(self, symbol_ls, interval):
        self.start_time = time.time()
        print("asyncio_run")
        asyncio.run(self.subscribe_symbol(symbol_ls, interval, ))

    async def subscribe_symbol(self, symbol: list, interval):
        channels = []
        for s in symbol:
            channels.append({"channel": "mark-price-" + interval, "instId": str(s)})
        print("subscribe_data")
        await self.subscribe_without_login(channels, url=setting.mark_klprice)


    # data:live pricing result:key:symbol val:max,min   symbol：live_symbol  data: [['1697550300000', '28231.1', '28280.2', '28128.3', '28247.6', '0']]
    def cal_tradingview(self, result, symbol, data):
        self.target_switch = False
        if symbol in result:
            if symbol not in self.strike_sym_ls and symbol not in self.order_dict:
                if Decimal(data[0][2]) > Decimal(result[symbol][0]) and Decimal(data[0][3]) > Decimal(result[symbol][1]):  # 0：timestamp 1：o 2：h 3：l 4：c
                    try:
                        res_kl = self.marketAPI.get_markprice_candlesticks(instId=symbol, limit="6",
                                                                        bar=setting.rest_interval)
                        code = res_kl.get('code')
                        if code == '0':
                            all_res = deal_message(res_kl)
                            new_res = deal_message(res_kl)[:4]
                        else:
                            print(code)
                            self.trade_switch = True
                            return
                    except:
                        self.trade_switch = True
                        return
                    ts = int(Decimal(new_res[0][0]) / Decimal('1000'))
                    time_ = int(time.time()) - ts
                    if time_ < 240:
                        new_res = new_res[1:]
                    target_temp = []
                    total = 0
                    for i in range(0, len(all_res) - 1):  # [0,1,2,3,4,5]
                        high_target = Decimal(all_res[i][2]) - Decimal(all_res[i+1][2])
                        target_temp.append(high_target)
                        total = total + high_target
                    avg_total = total / Decimal(len(target_temp))
                    for i in target_temp:
                        if abs(i) < avg_total / Decimal('2'):
                            target_temp.remove(i)
                    if min(target_temp) > 0:
                        self.target_switch = True
                    if (Decimal(new_res[0][2]) - Decimal(new_res[1][2])) / (Decimal(new_res[0][2]) - Decimal(new_res[0][3])) > 0.5 or self.target_switch == True:
                        price = Decimal(data[0][2]) * Decimal(0.9995)  #　0.9995
                        price = self.match_precision(Decimal(price), Decimal(data[0][2]))  # price：str
                        trading_view = 1  # long
                        print("Trigger_long", symbol)
                        self.trading(trading_view, symbol, price)
                        return
                    else:
                        trading_view = 0  # short
                        print("Trigger_short", symbol)
                        price = Decimal(data[0][3]) * Decimal(1.0005)  # 1.0005
                        price = self.match_precision(Decimal(price), Decimal(data[0][3]))
                        self.trading(trading_view, symbol, price)
                        return
                elif Decimal(data[0][3]) < Decimal(result[symbol][1]) and Decimal(data[0][2]) < Decimal(result[symbol][0]):
                    try:
                        res_kl = self.marketAPI.get_markprice_candlesticks(instId=symbol, limit="6",
                                                                        bar=setting.rest_interval)
                        code = res_kl.get('code')
                        if code == '0':
                            all_res = deal_message(res_kl)
                            new_res = deal_message(res_kl)[:4]
                        else:
                            print(code)
                            self.trade_switch = True
                            return
                    except:
                        self.trade_switch = True
                        return
                    ts = int(Decimal(new_res[0][0]) / Decimal('1000'))
                    time_ = int(time.time()) - ts
                    if time_ < 240:
                        new_res = new_res[1:]
                    target_temp = []
                    total = 0
                    for i in range(0, len(all_res) - 1):  # [0,1,2,3,4,5]
                        high_target = Decimal(all_res[i][2]) - Decimal(all_res[i + 1][2])
                        target_temp.append(high_target)
                        total = total + high_target
                    avg_total = total / Decimal(len(target_temp))
                    for i in target_temp:
                        if abs(i) < avg_total / Decimal('2'):
                            target_temp.remove(i)
                    if max(target_temp) < 0:
                        self.target_switch = True
                    if (Decimal(new_res[1][3]) - Decimal(new_res[0][3])) / (Decimal(new_res[0][2]) - Decimal(new_res[0][3])) > 0.5 or self.target_switch == True:
                        trading_view = 0  # short
                        print("Trigger_short", symbol)
                        price = Decimal(data[0][3]) * Decimal(1.0005)  # 1.0005
                        price = self.match_precision(Decimal(price), Decimal(data[0][3]))
                        self.trading(trading_view, symbol, price)
                        return
                    else:
                        price = Decimal(data[0][2]) * Decimal(0.9995)  # 0.9995
                        price = self.match_precision(Decimal(price), Decimal(data[0][2]))  # price：str
                        trading_view = 1  # long
                        print("Trigger_long", symbol)
                        self.trading(trading_view, symbol, price)
                        return
                else:
                    self.trade_switch = True

    @retry_on_exception_sync
    def get_banlance_all(self):
        banlance_all = Decimal(deal_message(self.accountAPI.get_account(ccy='USDT'))[0]['details'][0]['cashBal'])
        return banlance_all

    @retry_on_exception_sync
    def get_banlance_avail(self):
        banlance_avail = Decimal(deal_message(self.accountAPI.get_account(ccy='USDT'))[0]['details'][0]['availBal'])
        return banlance_avail

    def get_position_tiers(self, symbol, lever, usdt, price):
        switch = True
        while switch == True:
            try:
                switch = False
                symbol = self.remove_swap(symbol)
                result = deal_message(self.publicAPI.get_tier(instType='SWAP', instFamily=symbol, tdMode='isolated'))
                for i in result:
                    if i['maxSz'] is None or i['minSz'] is None:
                        continue
                    elif Decimal(i['maxLever']) == Decimal(lever):  #  and Decimal(usdt) < Decimal(i['maxSz']) and Decimal(usdt) > Decimal(i['minSz'])
                        val = Decimal(usdt) * Decimal(lever)
                        size = self.convert_contract_coin(symbol, order_type='open', price=price, val=str(val))
                        if Decimal(size) <= Decimal(i['maxSz']) and Decimal(size) >= Decimal(i['minSz']):
                            return size
                    elif Decimal(i['maxLever']) < Decimal(lever):
                        lever = i['maxLever']
                        continue
                return -1
            except:
                switch = True

    def remove_swap(self, symbol):
        if '-SWAP' in symbol:
            symbol = symbol.replace("-SWAP", "")
        return symbol

    def match_precision(self, dec1: Decimal, dec2: Decimal):  # match_precision
        precision = abs(dec2.as_tuple().exponent)
        format_str = "{:." + str(precision) + "f}"
        result_str = format_str.format(dec1)
        return result_str

    @retry_on_exception_sync
    def convert_contract_coin(self, symbol, val, price, order_type):  # transform_sheet_coin price:limit val：usdt order_type:  open  close
        symbol = self.remove_swap(symbol)
        cv_co = deal_message(self.publicAPI.convert_contract_coin(instId=f'{symbol}-SWAP', sz=val, px=str(price), opType=order_type,unit='usds'))
        return cv_co[0].get('sz')

    @retry_on_exception_sync
    def dynamic_param(self, symbol):
        symbol = self.remove_swap(symbol) + '-SWAP'
        result = deal_message(
            self.marketAPI.get_markprice_candlesticks(instId=symbol, limit=5, bar=setting.rest_interval))
        max_high_price = max(Decimal(res_max[2]) for res_max in result)
        min_low_price = min(Decimal(res_min[3]) for res_min in result)
        sum_price = (max_high_price - min_low_price) / ((max_high_price + min_low_price) / Decimal("2"))
        # Map the results to the weight range through an exponential function
        weight = 1 / math.exp(-sum_price)  # exp
        weight_d = 1 / weight
        sum_val = Decimal(str(1 - weight_d)).log10()
        sum_val = abs(math.ceil(sum_val))  # ceil abs
        self.liqpx_slip = setting.liqpx_slip * weight
        self.order_wait_time = setting.order_wait_time / sum_val
        self.profit_per = setting.profit_per * (sum_val / 100 + 1)
        self.stop_loss = setting.stop_loss
        self.position_update = setting.position_update - 10 * sum_val
        self.profit_min = setting.profit_min + 0.05 * sum_val
        self.float_val = setting.float_val + 0.005 * sum_val

    @retry_on_exception_sync
    def trade_logic(self, trading_view, bv, lever, symbol, price, ba):  # trade_logic
        if self.init_ba / Decimal(setting.total_fail_count) * Decimal(self.multiplier) > bv:
            self.trade_switch = True
            print("account_empty", self.multiplier)
            return
        self.dynamic_param(symbol)
        usdt = self.init_ba / Decimal(setting.total_fail_count) * Decimal(self.multiplier)
        sz = self.get_position_tiers(symbol, lever, usdt, price)
        if sz == -1:
            self.ignore_temp.append(symbol+'-SWAP')
            self.trade_switch = True
            return
        if trading_view == 1:  # 多
            if self.multiplier < self.demultiplier:
                result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                      mgnMode='isolated', posSide='long')  # set lever
                res = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='buy', posSide='long', tag= "open",
                                                   ordType='market', sz=sz, banAmend='',
                                                   quickMgnType='manual')
                order_id = deal_message(res)[0].get('ordId')
                code = res.get('code')
                if code != '0':
                    self.trade_switch = True
                    print(res)
                    if deal_message(res)[0].get('sCode') == '51000':
                        self.ignore_temp.append(symbol + '-SWAP')
                    return
                self.order_dict[symbol+'-SWAP'] = order_id
                sz = sz * self.demultiplier
                result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                      mgnMode='isolated', posSide='short')  # set lever
                res1 = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='sell', tag="open",
                                                posSide='short',
                                                ordType='market', sz=sz, banAmend='',
                                                quickMgnType='manual')
                order_id = deal_message(res1)[0].get('ordId')
                code1 = res1.get('code')
                if code1 != '0':
                    self.trade_switch = True
                    print(res)
                    if deal_message(res)[0].get('sCode') == '51000':
                        self.ignore_temp.append(symbol+'-SWAP')
                    return
                self.order_dict[symbol+'-SWAP'] = order_id
                print("long_order", res, symbol)
                return
            else:
                result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                      mgnMode='isolated', posSide='short')  # set lever
                sz1 = sz
                sz = sz * self.demultiplier
                res1 = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='sell', tag="open",
                                                posSide='short',
                                                ordType='market', sz=sz, banAmend='',
                                                quickMgnType='manual')
                order_id = deal_message(res1)[0].get('ordId')
                code = res1.get('code')
                if code != '0':
                    self.trade_switch = True
                    print(res1)
                    if deal_message(res1)[0].get('sCode') == '51000':
                        self.ignore_temp.append(symbol + '-SWAP')
                    return
                self.order_dict[symbol+'-SWAP'] = order_id
                result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                      mgnMode='isolated', posSide='long')  # set lever
                res = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='buy', posSide='long', tag= "open",
                                                   ordType='market', sz=sz1, banAmend='',
                                                   quickMgnType='manual')
                order_id = deal_message(res)[0].get('ordId')
                code = res.get('code')
                if code != '0':
                    self.trade_switch = True
                    print(res)
                    if deal_message(res)[0].get('sCode') == '51000':
                        self.ignore_temp.append(symbol + '-SWAP')
                    return
        elif trading_view == 0:  # short
            if self.multiplier < self.demultiplier:
                result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                      mgnMode='isolated', posSide='short')  # set_lever
                res = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='sell', tag="open",
                                                posSide='short',
                                                ordType='market', sz=sz, banAmend='',
                                                quickMgnType='manual')
                order_id = deal_message(res)[0].get('ordId')
                code = res.get('code')
                if code != '0':
                    self.trade_switch = True
                    print(res)
                    if deal_message(res)[0].get('sCode') == '51000':
                        self.ignore_temp.append(symbol + '-SWAP')
                    return
                self.order_dict[symbol+'-SWAP'] = order_id
                result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                      mgnMode='isolated', posSide='long')  # set_lever
                sz = sz * self.demultiplier
                res1 = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='buy', posSide='long',
                                                tag="open",
                                                ordType='market', sz=sz, banAmend='',
                                                quickMgnType='manual')
                order_id = deal_message(res)[0].get('ordId')
                code1 = res1.get('code')
                if code1 != '0':
                    self.trade_switch = True
                    print(res)
                    if deal_message(res)[0].get('sCode') == '51000':
                        self.ignore_temp.append(symbol+'-SWAP')
                    return
                self.order_dict[symbol+'-SWAP'] = order_id
                print("short_order", res, symbol)
                return
            else:
                result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                      mgnMode='isolated', posSide='long')  # set_lever
                sz1 = sz
                sz = sz * self.demultiplier
                res1 = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='buy', posSide='long',
                                                 tag="open",
                                                 ordType='market', sz=sz, banAmend='',
                                                 quickMgnType='manual')
                order_id = deal_message(res1)[0].get('ordId')
                code1 = res1.get('code')
                if code1 != '0':
                    self.trade_switch = True
                    print(res1)
                    if deal_message(res1)[0].get('sCode') == '51000':
                        self.ignore_temp.append(symbol + '-SWAP')
                    return
                self.order_dict[symbol+'-SWAP'] = order_id
                result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                      mgnMode='isolated', posSide='short')  # set_lever
                res = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='sell', tag="open",
                                                posSide='short',
                                                ordType='market', sz=sz, banAmend='',
                                                quickMgnType='manual')
                order_id = deal_message(res)[0].get('ordId')
                code = res.get('code')
                if code != '0':
                    self.trade_switch = True
                    print(res)
                    if deal_message(res)[0].get('sCode') == '51000':
                        self.ignore_temp.append(symbol+'-SWAP')
                    return
                self.order_dict[symbol+'-SWAP'] = order_id
                print("long_order", res, symbol)
                return
        self.trade_switch = True

    def iniy_multiplier(self):
        if setting.fail_count_reset == True:
            multiplier = 1
            return multiplier
        if Decimal(self.order_ls[0]) > Decimal(0):
            multiplier = 1
        else:
            multiplier = 1
            for i in range(len(self.order_ls)):
                if self.order_ls[i] == 0:
                    continue
                if float(self.order_ls[i]) > 0:
                    return multiplier
                elif float(self.order_ls[i]) < 0:
                    multiplier = multiplier * setting.Incremental_multiplier
                if multiplier > setting.max_fail_count:
                    exit()
        return multiplier

    def lever_down(self, lever):
        if lever == '125':
            return '100'
        elif lever == '100':
            return '75'
        elif lever == '75':
            return '66'
        elif lever == '66':
            return '50'
        elif lever == '50':
            return '40'
        elif lever == '40':
            return '33'
        elif lever == '33':
            return '25'
        elif lever == '25':
            return '20'
        elif lever == '20':
            return '5'
        elif lever == '5':
            return '2'
        else:
            return -1

    async def subscribe_order(self):
        # channels = [{"channel": "positions", "instType": "SWAP"}]
        channels = [{"channel": "orders", "instType": "SWAP"}, {"channel": "positions", "instType": "SWAP"}]
        await self.subscribe(channels, url=setting.private_url)

    @retry_on_exception_sync
    def trading(self, tradingview, symbol, price):  # 1.get_banlance  2.get_max_lever and position_cont(usdt)
        symbol = self.remove_swap(symbol)
        bv = self.get_banlance_avail()
        ba = self.get_banlance_all()
        if setting.spot_switch:
            bv = bv * Decimal((1 - setting.spot_value))
        if int(ba) < 10:
            exit()
        result = deal_message(self.publicAPI.get_instruments(instType='SWAP', instFamily=symbol))
        lever = result[0]['lever']
        if setting.quick_trade_switch is not None:
            if int(lever) < setting.quick_trade_switch and self.multiplier != setting.max_fail_count:
                self.ignore_temp.append(symbol+'-SWAP')
                self.trade_switch = True
                return
        self.trade_logic(tradingview, bv, lever, symbol, price, ba)
        print(f"try_open_position,account：{bv}")

    @retry_on_exception_decorator
    async def spot_trading(self, tradingview, symbol, price):  # 1.get_banlance  2.get_max_lever and position_cont(usdt)
        bv = self.get_banlance_avail()
        bv = bv * Decimal(str(setting.spot_value)) / Decimal(str(setting.spot_count)) * Decimal(setting.spot_level)
        sz = self.convert_contract_coin(symbol, str(bv), price, 'open')
        if tradingview == 1:  # long
            result = self.accountAPI.set_leverage(instId=symbol, lever=10,
                                                  mgnMode='isolated', posSide='long')  # set lever
            self.spot_ls.append(symbol)
            res = self.tradeAPI.place_order(instId=symbol, tdMode='isolated', side='buy', posSide='long',
                                               ordType='market', sz=sz, banAmend='',
                                               quickMgnType='manual')
            order_id = deal_message(res)[0].get('ordId')
            code = res.get('code')
            if code != '0':
                self.spot_ls.remove(symbol)
                return
            self.spot_order[symbol] = order_id
            self.spot_num += 1
            print("spot_long", res, symbol)
            return
        elif tradingview == 0:  # short
            result = self.accountAPI.set_leverage(instId=symbol, lever=10,
                                                  mgnMode='isolated', posSide='short')  # set lever
            self.spot_ls.append(symbol)
            res = self.tradeAPI.place_order(instId=symbol, tdMode='isolated', side='sell',
                                            posSide='short',
                                            ordType='market', sz=sz, banAmend='',
                                            quickMgnType='manual')
            order_id = deal_message(res)[0].get('ordId')
            code = res.get('code')
            if code != '0':
                self.spot_ls.remove(symbol)
                return
            self.spot_order[symbol] = order_id
            self.spot_num += 1
            print("spot_short", res, symbol)
            return

    def order_monitor(self):
        order_thread = threading.Thread(target=self.run_in_thread)
        order_thread.start()
        if not order_thread.is_alive():
            return self.order_monitor()

    def run_position(self, result):
        for i in result:
            symbol = i['instId']
            if not i['liqPx']:
                continue
            liqpx = i['liqPx']
            avgpx = i['avgPx']
            avgpx = Decimal(avgpx)
            mode = i['posSide']
            sz = i['availPos']
            lever = i['lever']
            uplRatio = i['uplRatio']
            # markPx = i['markPx']
            # markPx = Decimal(markPx)
            pos_time = int(int(i['pTime']) / 1000)  # least_time
            count = self.order_algo.count(symbol)
            if count < 2 and symbol not in self.spot_ls and symbol not in self.order_dict:  # self.strike_sym_ls????????
                if mode == self.Pos_temp:
                    continue
                if mode == 'long':
                    side = 'sell'
                    posSide = 'long'
                    slPx = avgpx - (abs(Decimal(avgpx) - Decimal(liqpx)) + Decimal(self.liqpx_slip)*avgpx)  # 11+
                    sl_tg = slPx + Decimal(avgpx)*Decimal(self.Trigger_slip)
                    tpPx = avgpx * (Decimal("1") + Decimal(self.profit_per) / Decimal(lever))  # 50 = 0.02 = 1.02
                    tp_tg = tpPx - Decimal(avgpx)*Decimal(self.Trigger_slip)
                elif mode == 'short':
                    side = 'buy'
                    posSide = 'short'
                    slPx = avgpx + (abs(Decimal(avgpx) - Decimal(liqpx)) - Decimal(self.liqpx_slip)*avgpx)
                    sl_tg = slPx - Decimal(avgpx) * Decimal(self.Trigger_slip)
                    tpPx = avgpx * (Decimal("1") - Decimal(self.profit_per) / Decimal(lever))
                    tp_tg = tpPx + Decimal(avgpx)*Decimal(self.Trigger_slip)
                else:
                    continue
                if avgpx == tpPx or avgpx == tp_tg:
                    tpPx = tpPx * Decimal("1.05")
                    tp_tg = tp_tg * Decimal("1.05")
                if symbol not in self.order_algo:
                    slPx = self.match_precision(slPx, avgpx)
                    sl_tg = self.match_precision(sl_tg, avgpx)
                    tpPx = self.match_precision(tpPx, avgpx)
                    tp_tg = self.match_precision(tp_tg, avgpx)
                    result = self.tradeAPI.place_algo_order(symbol, 'isolated', side, ordType='oco',tag="close",
                                                       sz=sz, posSide=posSide, tpTriggerPx=str(tp_tg), tpOrdPx=str(tpPx),slTriggerPx=str(sl_tg),slOrdPx=str(slPx),
                                                      tpTriggerPxType='mark', slTriggerPxType='mark')
                    res = deal_message(result)
                    print(res)
                    if res[0].get('sCode') == '0':
                        algoId = res[0].get('algoId')
                        self.order_algo.append(symbol)
                        print("place_order-algo")
                        self.Pos_temp = mode
                        self.order_count += 1
                        break
                    else:
                        print(res[0].get('sMsg'), symbol, slPx, sl_tg, tpPx, tp_tg, avgpx)

            elif symbol in self.spot_order and symbol not in self.spot_profit_dict and symbol not in self.strike_sym_ls:
                if mode == 'long':
                    side = 'sell'
                    posSide = 'long'
                    tpPx = avgpx * (Decimal("1") + Decimal(setting.spot_profit))
                    tp_tg = tpPx - Decimal(avgpx)*Decimal(self.Trigger_slip)
                elif mode == 'short':
                    side = 'buy'
                    posSide = 'short'
                    tpPx = avgpx * (Decimal("1") - Decimal(setting.spot_profit))
                    tp_tg = tpPx + Decimal(avgpx)*Decimal(self.Trigger_slip)
                else:
                    continue
                if avgpx == tpPx or avgpx == tp_tg:
                    tpPx = tpPx * Decimal("1.05")
                    tp_tg = tp_tg * Decimal("1.05")
                tpPx = self.match_precision(tpPx, avgpx)
                tp_tg = self.match_precision(tp_tg, avgpx)
                result = self.tradeAPI.place_algo_order(symbol, 'isolated', side, ordType='conditional',
                                                   sz=sz, posSide=posSide, tpTriggerPx=str(tp_tg), tpOrdPx=str(tpPx),
                                                  tpTriggerPxType='mark')
                res = deal_message(result)
                print(res)
                if res[0].get('sCode') == '0':
                    algoId = res[0].get('algoId')
                    self.spot_profit_dict[symbol] = algoId
                    print("spot_place_order-algo")
                    break
                else:
                    print(res[0].get('sMsg'), symbol, tpPx, tp_tg, avgpx)

    def run_in_thread(self):
        asyncio.run(self.subscribe_order())

    def get_timestamp(self):
        now = datetime.datetime.now()
        t = now.isoformat("T", "milliseconds")
        return t + "Z"

    def get_server_time(self):
        url = "https://www.okx.com/api/v5/public/time"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['data'][0]['ts']
        else:
            return ""

    def get_local_timestamp(self):
        return int(time.time())

    def login_params(self, timestamp):
        message = timestamp + 'GET' + '/users/self/verify'

        mac = hmac.new(bytes(setting.secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        sign = base64.b64encode(d)

        login_param = {"op": "login", "args": [{"apiKey": setting.api_key,
                                                "passphrase": setting.passphrase,
                                                "timestamp": timestamp,
                                                "sign": sign.decode("utf-8")}]}
        login_str = json.dumps(login_param)
        return login_str

    def partial(self, res):
        data_obj = res['data'][0]
        bids = data_obj['bids']
        asks = data_obj['asks']
        instrument_id = res['arg']['instId']
        return bids, asks, instrument_id

    def update_bids(self, res, bids_p):
        bids_u = res['data'][0]['bids']
        for i in bids_u:
            bid_price = i[0]
            for j in bids_p:
                if bid_price == j[0]:
                    if i[1] == '0':
                        bids_p.remove(j)
                        break
                    else:
                        del j[1]
                        j.insert(1, i[1])
                        break
            else:
                if i[1] != "0":
                    bids_p.append(i)
        else:
            bids_p.sort(key=lambda price: self.sort_num(price[0]), reverse=True)
        return bids_p

    def update_asks(self, res, asks_p):
        asks_u = res['data'][0]['asks']
        for i in asks_u:
            ask_price = i[0]
            for j in asks_p:
                if ask_price == j[0]:
                    if i[1] == '0':
                        asks_p.remove(j)
                        break
                    else:
                        del j[1]
                        j.insert(1, i[1])
                        break
            else:
                if i[1] != "0":
                    asks_p.append(i)
        else:
            asks_p.sort(key=lambda price: self.sort_num(price[0]))
        return asks_p

    def sort_num(self, n):
        if n.isdigit():
            return int(n)
        else:
            return float(n)

    def check(self, bids, asks):
        bids_l = []
        bid_l = []
        count_bid = 1
        while count_bid <= 25:
            if count_bid > len(bids):
                break
            bids_l.append(bids[count_bid - 1])
            count_bid += 1
        for j in bids_l:
            str_bid = ':'.join(j[0: 2])
            bid_l.append(str_bid)
        asks_l = []
        ask_l = []
        count_ask = 1
        while count_ask <= 25:
            if count_ask > len(asks):
                break
            asks_l.append(asks[count_ask - 1])
            count_ask += 1
        for k in asks_l:
            str_ask = ':'.join(k[0: 2])
            ask_l.append(str_ask)
        num = ''
        if len(bid_l) == len(ask_l):
            for m in range(len(bid_l)):
                num += bid_l[m] + ':' + ask_l[m] + ':'
        elif len(bid_l) > len(ask_l):
            for n in range(len(ask_l)):
                num += bid_l[n] + ':' + ask_l[n] + ':'
            for l in range(len(ask_l), len(bid_l)):
                num += bid_l[l] + ':'
        elif len(bid_l) < len(ask_l):
            for n in range(len(bid_l)):
                num += bid_l[n] + ':' + ask_l[n] + ':'
            for l in range(len(bid_l), len(ask_l)):
                num += ask_l[l] + ':'
        new_num = num[:-1]
        int_checksum = zlib.crc32(new_num.encode())
        fina = self.change(int_checksum)
        return fina

    def change(self, num_old):
        num = pow(2, 31) - 1
        if num_old > num:
            out = num_old - num * 2 - 2
        else:
            out = num_old
        return out

    # subscribe channels un_need login
    async def subscribe_without_login(self, channels, url=setting.public_url):
        l = []
        sym_idx = 0
        count = 0
        while True:
            try:
                async with websockets.connect(url) as ws:
                    sub_param = {"op": "subscribe", "args": channels}
                    sub_str = json.dumps(sub_param)
                    await ws.send(sub_str)
                    while True:
                        try:
                            res = await asyncio.wait_for(ws.recv(), timeout=25)
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed) as e:
                            try:
                                await ws.send('ping')
                                res = await ws.recv()
                                # print(res)
                                continue
                            except Exception as e:
                                print("conn_close，retry……pb", e)
                                break
                        # print(self.get_timestamp() + res)
                        if time.time() - self.start_time >= setting.update_interval * 10:
                            self.avg_switch = False
                            return
                        res = json.loads(res)
                        if 'event' in res:
                            continue
                        elif res.get('arg') and 'data' in res:
                            symbol = res.get('arg')['instId']
                            data = res.get('data')
                            sever_time = self.get_local_timestamp()
                            if setting.spot_switch and self.spot_num < setting.spot_count and self.spot_price_dict:
                                sp_res, price = await sp.spot_monitor(data, self.spot_price_dict, symbol)
                                if sp_res != 0 and price != 0 and symbol not in self.spot_order:
                                    await self.spot_trading(sp_res, symbol, price)
                            if sever_time % setting.update_interval <= 10:  #if new interval update time < 10s,that new kline update ,then update data
                                self.avg_switch = False
                            if not self.avg_switch:
                                q = Queue()
                                g_thread = threading.Thread(target=self.get_price, args=(self.symbol_ls, q))
                                g_thread.start()
                                g_thread.join()
                                self.avg_switch = True
                                self.price_dict = q.get()
                                continue
                            if g_thread.is_alive():
                                continue
                            if not self.trade_switch and len(self.strike_sym_ls) == 0 and symbol in self.order_dict:
                                self.cancel_wait_order()
                                continue
                            if self.avg_switch and not self.trade_switch:
                                continue
                            # Determine whether there are opening position
                            if isinstance(self.fluctuation_values, list) and self.trade_switch == True:
                                if sym_idx == len(self.fluctuation_values) - 1:
                                    sym_idx = 0
                                elif self.fluctuation_values[sym_idx] == symbol and symbol in self.ignore_temp:
                                    sym_idx = sym_idx + 1
                                    continue
                                elif self.fluctuation_values[sym_idx] == symbol and symbol not in self.ignore_temp and symbol not in self.spot_order and symbol not in self.symbol_temp:
                                    self.trade_switch = False
                                    self.cal_tradingview(self.price_dict, symbol, data)
                                elif count == len(self.fluctuation_values) - sym_idx - 1:
                                    sym_idx = sym_idx + 1
                                    count = 0
                                else:
                                    count = count + 1

            except Exception as e:
                print(e)
                print("pb_conn_break，retry……")
                continue

    # subscribe channels need login
    async def subscribe(self, channels, url=setting.private_url):
        while True:
            try:
                async with websockets.connect(url) as ws:
                    # login
                    timestamp = str(self.get_local_timestamp())
                    login_str = self.login_params(timestamp)
                    await ws.send(login_str)
                    # print(f"send: {login_str}")
                    res = await ws.recv()
                    # subscribe
                    sub_param = {"op": "subscribe", "args": channels}
                    sub_str = json.dumps(sub_param)
                    await ws.send(sub_str)
                    while True:
                        try:
                            res = await asyncio.wait_for(ws.recv(), timeout=25)
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed) as e:
                            try:
                                await ws.send('ping')
                                res = await ws.recv()
                                continue
                            except Exception as e:
                                print("conn_close，retry……")
                                break
                        try:
                            res = json.loads(res)
                        except:
                            print(res)
                        if 'event' in res:
                            continue
                        elif res.get('arg')['channel'] == 'orders':
                            data = res.get('data')
                            if data and isinstance(data, list):
                                self.deal_order(data)
                        elif res.get('arg')['channel'] == 'positions':
                            data = res.get('data')
                            if data and isinstance(data, list):
                                self.run_position(data)
            except Exception as e:
                print("pv_conn_break，retry……", e)
                continue

    def deal_order(self, data):
        for i in data:
            symbol = i.get('instId')
            tag = i.get('tag')
            if i.get('state') == 'filled' and i['side'] == 'buy':  #  Purchase transaction
                if symbol in self.spot_profit_dict:
                    del self.spot_order[symbol]
                    del self.spot_profit_dict[symbol]
                    self.spot_ls.remove(symbol)
                    self.spot_num -= 1
                elif symbol in self.spot_order:
                    continue
                elif tag == "open" and symbol not in self.spot_ls and self.trade_switch == True:
                    self.strike_sym_ls.append(symbol)
                    if len(self.symbol_temp) < 5:
                        self.symbol_temp.append(symbol)
                    else:
                        self.symbol_temp = []
                    try:
                        self.wx.push_order(symbol, "做多", self.multiplier)
                        self.wx_switch = True
                    except Exception as e:
                        print(e)
                    print("Purchase transaction")

                elif self.trade_switch == False and tag == "close":
                    self.order_count += 1
                    self.strike_sym_ls = []
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if self.profit_switch == False and Decimal(i['pnl']) > 0:  # Stop profit transactions
                        self.multiplier = 1
                        self.demultiplier = self.demultiplier * setting.Incremental_multiplier
                        try:
                            self.wx.push_order(symbol, "止盈", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                    elif self.profit_switch == True and Decimal(i['pnl']) > 0:
                        self.profit_switch = False
                        self.profit_min = self.profit_min + 0.1
                        self.position_time = 0
                        try:
                            self.wx.push_order(symbol, "动态止盈", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                    elif Decimal(i['pnl']) < 0:  # Stop loss transactions
                        self.order_count += 1
                        self.multiplier = self.multiplier * setting.Incremental_multiplier
                        self.demultiplier = 1
                        try:
                            self.wx.push_order(symbol, "爆仓", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                    self.Pos_temp = None
                    self.ignore_temp = []

                elif self.trade_switch == False and Decimal(i['pnl']) < 0:
                    self.multiplier = self.multiplier * setting.Incremental_multiplier
                    self.demultiplier = 1
                    try:
                        self.wx.push_order(symbol, "止损", self.multiplier, i['pnl'])
                    except Exception as e:
                        print(e)
                    self.Pos_temp = None
                    self.ignore_temp = []

            elif i.get('state') == 'filled' and i['side'] == 'sell':  # Sales transaction
                symbol = i['instId']
                if symbol in self.spot_profit_dict:
                    del self.spot_order[symbol]
                    del self.spot_profit_dict[symbol]
                    self.spot_ls.remove(symbol)
                    self.spot_num -= 1
                elif symbol in self.spot_order:
                    continue
                elif tag == "open" and symbol not in self.spot_ls:
                    self.strike_sym_ls.append(symbol)
                    if len(self.symbol_temp) < 5:
                        self.symbol_temp.append(symbol)
                    else:
                        self.symbol_temp = []
                    try:
                        self.wx.push_order(symbol, "做空", self.multiplier)
                        self.wx_switch = True
                    except Exception as e:
                        print(e)
                    print("Sales transaction")

                elif self.trade_switch == False and tag == "close":
                    self.order_count += 1
                    self.strike_sym_ls = []
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if self.profit_switch == False and Decimal(i['pnl']) > 0:  # Stop profit transactions
                        self.multiplier = 1
                        self.demultiplier = self.demultiplier * setting.Incremental_multiplier
                        try:
                            self.wx.push_order(symbol, "止盈", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                    elif self.profit_switch == True and Decimal(i['pnl']) > 0:
                        self.profit_switch = False
                        self.profit_min = self.profit_min + 0.1
                        self.position_time = 0
                        try:
                            self.wx.push_order(symbol, "动态止盈", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                    elif Decimal(i['pnl']) < 0:  # Stop loss transactions
                        self.multiplier = self.multiplier * setting.Incremental_multiplier
                        self.demultiplier = 1
                        try:
                            self.wx.push_order(symbol, "止损", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                    self.Pos_temp = None
                    self.ignore_temp = []
                elif self.trade_switch == False and Decimal(i['pnl']) < 0:
                    self.order_count += 1
                    self.multiplier = self.multiplier * setting.Incremental_multiplier
                    self.demultiplier = 1
                    try:
                        self.wx.push_order(symbol, "爆仓", self.multiplier, i['pnl'])
                    except Exception as e:
                        print(e)
                    self.Pos_temp = None
                    self.ignore_temp = []
            else:
                continue
            if symbol in self.order_dict:
                del self.order_dict[symbol]
            if self.order_count % 2 == 0 and self.order_count != 0:
                print(self.order_count)
                self.trade_switch = True
            print(self.trade_switch, self.order_dict, self.order_algo, self.ignore_temp, self.strike_sym_ls, self.symbol_temp)
    @retry_on_exception_sync
    def close_position(self, symbol, mode, price, sz):  # close_position  symbol, mode, price, sz
        """
        Long position opening: Buy to open (side: buy; posSide: long)
        Short position opening: Sell to open (side: sell; posSide: short)
        Close long position: Sell to close (side: sell; posSide: long)
        Close short position: Buy to close (side: buy; posSide: short)
        """

        if mode == 'long':
            side = 'sell'
            posSide = 'long'
        elif mode == 'short':
            side = 'buy'
            posSide = 'short'
        else:
            return
        res = self.tradeAPI.place_order(instId=symbol, tdMode='isolated', side=side,tag="close",
                                  posSide=posSide,
                                  ordType='limit', sz=sz, banAmend='', px=str(price),
                                  quickMgnType='manual')

    # trade
    async def trade(self, trade_param, url=setting.private_url):
        while True:
            try:
                async with websockets.connect(url) as ws:
                    # login
                    timestamp = str(self.get_local_timestamp())
                    login_str = self.login_params(timestamp)
                    await ws.send(login_str)
                    # print(f"send: {login_str}")
                    res = await ws.recv()
                    print(res)

                    # trade
                    sub_str = json.dumps(trade_param)
                    await ws.send(sub_str)
                    print(f"send: {sub_str}")

                    while True:
                        try:
                            res = await asyncio.wait_for(ws.recv(), timeout=25)
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed) as e:
                            try:
                                await ws.send('ping')
                                res = await ws.recv()
                                print(res)
                                continue
                            except Exception as e:
                                print("conn_close，retry……")
                                break

                        print(self.get_timestamp() + res)

            except Exception as e:
                print("conn_break，retry……")
                continue

    # unsubscribe channels
    async def unsubscribe(self, channels, url=setting.private_url):
        async with websockets.connect(url) as ws:
            # login
            timestamp = str(self.get_local_timestamp())
            login_str = self.login_params(timestamp)
            await ws.send(login_str)
            # print(f"send: {login_str}")

            res = await ws.recv()
            print(f"recv: {res}")

            # unsubscribe
            sub_param = {"op": "unsubscribe", "args": channels}
            sub_str = json.dumps(sub_param)
            await ws.send(sub_str)
            print(f"send: {sub_str}")

            res = await ws.recv()
            print(f"recv: {res}")

    # unsubscribe channels
    async def unsubscribe_without_login(self, channels, url=setting.public_url):
        async with websockets.connect(url) as ws:
            # unsubscribe
            sub_param = {"op": "unsubscribe", "args": channels}
            sub_str = json.dumps(sub_param)
            await ws.send(sub_str)
            print(f"send: {sub_str}")

            res = await ws.recv()
            print(f"recv: {res}")

    def Dynamic_tuning(self):
        """
        load_interval: Calculation interval based on several candlesticks, default is every 10 candlesticks.
        liqpx_slip: Percentage of liquidation price slipping, default is 0.0009 (0.09%).
        Trigger_slip: Percentage of trigger price slipping, default is 0.0009 (0.09%).
        order_wait_time: Waiting time for order execution, default is 120 seconds.
        quick_tradingview: Percentage change threshold for recent 10 candlesticks in pure trend one-sided trading, default is 0.02 (2%).
        profit_per: Profit percentage, default is 1.
        stop_loss: Stop loss percentage, default is -1.
        position_update: Time for dynamic profit-taking, default is 5 (minutes).
        profit_min: Minimum value for dynamic profit-taking, default is 0.15 (15%).
        float_val: Fluctuation value for dynamic profit-taking, default is 0.05 (5%).
        one_day_trade: One-day trading volume limit, default is 200,000,000
        """
        if not self.avg_switch:
            if isinstance(self.fluctuation_values, dict):
                temp = self.fluctuation_values
                self.fluctuation_values = sorted(self.fluctuation_values, key=self.fluctuation_values.get)  # Fluctuation sorting key
                # cal_abs(avg)
                abs_values = [abs(value) for value in temp.values()]
                avg_abs_value = sum(abs_values) / len(abs_values)
                # Calculate the number of values below the average
                count_below_avg = sum(1 for value in abs_values if value < avg_abs_value)
                if 1 <= (len(self.fluctuation_values) / 2) % count_below_avg <= 2:
                    self.load_interval = setting.load_interval + 5
                    self.Trigger_slip = setting.Trigger_slip
                    self.quick_tradingview = avg_abs_value
                    self.one_day_trade = setting.one_day_trade
                elif (len(self.fluctuation_values) / 2) % count_below_avg > 2:
                    self.load_interval = setting.load_interval + 10
                    self.Trigger_slip = setting.Trigger_slip
                    self.quick_tradingview = avg_abs_value
                    self.one_day_trade = setting.one_day_trade
                else:
                    cal_number = avg_abs_value + 1
                    self.Trigger_slip = setting.Trigger_slip * 1.01
                    self.quick_tradingview = avg_abs_value * 3 / 2
                    self.one_day_trade = setting.one_day_trade * 1.25
                    self.load_interval = setting.load_interval

    def run(self):
        self.wx.start()
        while True:
            self.symbol_monitor(setting.interval)

if __name__ == '__main__':
    asd = websocket_funs(setting.user)
    # asd.symbol_monitor(interval=Interval.CANDLE_15m)
    # print(int(time.time()*1000))
    # asd.symbol_monitor(interval=Interval.CANDLE_15m)
    # print(asd.get_position_tiers(symbol='ETH-USDT', lever='75'))
    # print(asd.trading(tradingview=0, symbol='ETH-USDT-SWAP'))
    # print("-----")
    asd.run()
    # print(time.time())
    # print(asd.convert_contract_coin(symbol='ETH-USDT', val=18, price=1800, order_type='close'))
    # asd.run_position_thread()