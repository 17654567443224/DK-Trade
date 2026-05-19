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
from utils import deal_message, retry_on_exception_sync, check_switch
from queue import Queue
import okx.Trade_api as Trade
import math
import deal_Market_kline
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
        self.order_wait_time = setting.order_wait_time
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
        self.order_algo = {}  # Dict of stop loss and stop loss orders
        self.fluctuation_values = {}  # kline_dym_dice，if ...
        self.price_dict = None
        self.init_ba = self.get_banlance_all()
        self.trade_switch = True
        self.lock = threading.Lock()
        self.pv_lock = threading.Lock()
        self.ignore_temp = []
        self.profit_switch = False
        self.position_time = 0
        self.wx = wx_robot(user, "Opportunity")
        self.wx_switch = False
        self.all_positions = []

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

    def get_price(self, symbol: list, q: Queue):  # load_interval：cal_kline_count
        """
        Return the dict composed of symbol and avg
        :param symbol:
        :return:
        """
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
                    res = self.marketAPI.get_markprice_candlesticks(instId=i, bar=setting.opportunity_interval, limit=6)  #default limit 100
                    code = res.get('code')
                    if code == '0':
                        result = deal_message(res)
                        result = deal_Market_kline.encapsulate_data(result)
                        break
                    else:
                        print(res)
                        symbol.remove(i)
                except:
                    time.sleep(2)
                    continue
            index = 0
            avg_ls = []
            while index <= len(result) - 1:
                avg = result[index].high_price - result[index].low_price
                avg_ls.append(avg)
                index += 1
            avg_num = sum(avg_ls) / len(avg_ls)
            diff_num = max(abs(avg_ls[i] - avg_ls[i + 1]) for i in range(len(avg_ls) - 1))
            cal_ls.append(avg_num)
            price_ls.append(diff_num)
        self.fluctuation_values = dict(zip(symbol, cal_ls))
        sym_avg_dict = dict(zip(symbol, price_ls))
        self.Dynamic_tuning()
        q.put(sym_avg_dict)

    def symbol_monitor(self, interval: Interval):
        """
        base: mark_price_?interval
        :return:
        """
        self.order_monitor()
        while True:
            symbol_ls = deal_data.get_symbol(only_symbol=True, count=setting.symbol_count)
            if not symbol_ls:
                time.sleep(5)
                continue
            self.symbol_ls = symbol_ls
            thread = threading.Thread(target=self.run_public_thread, args=(symbol_ls, interval.value,))
            thread.start()
            thread.join()

    def run_public_thread(self, symbol_ls, interval):
        self.ignore_temp = []
        self.start_time = time.time()
        print("asyncio_run")
        asyncio.run(self.subscribe_symbol(symbol_ls, interval, ))

    async def subscribe_symbol(self, symbol: list, interval):
        channels = []
        for s in symbol:
            channels.append({"channel": "mark-price-" + interval, "instId": str(s)})
        print("subscribe_data")
        await self.subscribe_without_login(channels, url=setting.mark_klprice)

    # data:live pricing result:key:symbol val:float   symbol：live_symbol  data: [['1697550300000', '28231.1', '28280.2', '28128.3', '28247.6', '0']]
    def cal_tradingview(self, result, symbol, data):
        diff_cal = Decimal(data[0][2]) - Decimal(data[0][3])
        if symbol in result:
            if symbol not in self.strike_sym_ls and symbol not in self.order_dict:
                if diff_cal > Decimal(result[symbol]):  # 0：timestamp 1：o 2：h 3：l 4：c
                    if abs(Decimal(data[0][1]) - Decimal(data[0][2])) / abs(Decimal(data[0][1]) - Decimal(data[0][3])) > 1.5:
                        price = Decimal(data[0][2]) * Decimal(0.9995)  #　0.9995
                        price = self.match_precision(Decimal(price), Decimal(data[0][2]))  # price：str
                        trading_view = 1  # long
                        print("Trigger_long", symbol)
                        self.trading(trading_view, symbol, price)
                        return
                    elif abs(Decimal(data[0][1]) - Decimal(data[0][3])) / abs(Decimal(data[0][1]) - Decimal(data[0][2])) > 1.5:
                        trading_view = 0  # short
                        print("Trigger_short", symbol)
                        price = Decimal(data[0][3]) * Decimal(1.0005)  # 1.0005
                        price = self.match_precision(Decimal(price), Decimal(data[0][3]))
                        self.trading(trading_view, symbol, price)
                        return
        self.trade_switch = True

    @retry_on_exception_sync
    def get_banlance_all(self):
        if setting.steady_switch:
            return Decimal('45')
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
        sum_price = (max_high_price - min_low_price) / (max_high_price + min_low_price)
        sum_price = abs(sum_price)
        # Map the results to the weight range through an exponential function
        weight = 1 / math.exp(-sum_price)  # exp
        weight_d = 1 / weight
        sum_val = Decimal(str(1 - weight_d)).log10()
        sum_val = abs(math.floor(1/sum_val))  # ceil abs
        self.liqpx_slip = setting.liqpx_slip * weight
        self.order_wait_time = setting.order_wait_time / sum_val
        self.profit_per = setting.profit_per * (sum_val / 100 + 1)
        self.stop_loss = setting.stop_loss
        self.position_update = setting.position_update - 10 * sum_val
        self.profit_min = setting.profit_min + 0.05 * sum_val
        self.float_val = setting.float_val + 0.005 * sum_val

    def catch_error_sCode(self, code:str):
        if code == '51004':
            self.wx.normal_text("挂单超过杠杆上限")
        elif code == '51005':
            self.wx.normal_text("委托数量大于单笔上限")
        elif code == '51008':
            self.wx.normal_text("余额不足")
    @retry_on_exception_sync
    def trade_logic(self, trading_view, bv, lever, symbol, price):  # trade_logic
        self.dynamic_param(symbol)
        usdt = bv * Decimal('0.1')
        sz = self.get_position_tiers(symbol, lever, usdt, price)
        if sz == -1:
            self.ignore_temp.append(symbol+'-SWAP')
            self.trade_switch = True
            return
        if trading_view == 1:  # 多
            result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                  mgnMode='isolated', posSide='long')  # set lever
            res = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='buy', posSide='long', px=str(price), tag="opoopen",
                                               ordType='limit', sz=sz, banAmend='',
                                               quickMgnType='manual')
            order_id = deal_message(res)[0].get('ordId')
            code = res.get('code')
            if code != '0':
                self.trade_switch = True
                print(res)
                Scode = deal_message(res)[0].get('sCode')
                if Scode == '51000':
                    self.ignore_temp.append(symbol + '-SWAP')
                else:
                    self.catch_error_sCode(Scode)
                return
            self.order_dict[symbol+'-SWAP'] = order_id
            print("long_order", symbol, self.trade_switch)
            return
        elif trading_view == 0:  # short
            result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                  mgnMode='isolated', posSide='short')  # set_lever
            res = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='sell',tag= "opoopen",
                                            posSide='short',
                                            ordType='limit', sz=sz, banAmend='', px=str(price),
                                            quickMgnType='manual')
            order_id = deal_message(res)[0].get('ordId')
            code = res.get('code')
            if code != '0':
                self.trade_switch = True
                print(res)
                Scode = deal_message(res)[0].get('sCode')
                if Scode == '51000':
                    self.ignore_temp.append(symbol + '-SWAP')
                else:
                    self.catch_error_sCode(Scode)
                return
            self.order_dict[symbol+'-SWAP'] = order_id
            print("short_order", symbol, self.trade_switch)
            return
        self.trade_switch = True

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
        if setting.opportunity_trade_switch:
            ba = ba * Decimal(setting.opportunity_proportion)
            bv = bv * Decimal(setting.opportunity_proportion)
        if int(ba) < 10:
            exit()
        result = deal_message(self.publicAPI.get_instruments(instType='SWAP', instFamily=symbol))
        lever = result[0]['lever']
        self.trade_logic(tradingview, bv, lever, symbol, price, ba)

    def order_monitor(self):
        order_thread = threading.Thread(target=self.run_in_thread)
        order_thread.start()
        if not order_thread.is_alive():
            self.order_monitor()

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
            if symbol not in self.all_positions:
                self.all_positions.append(symbol)
            if symbol not in self.order_algo and symbol not in self.order_dict and symbol in self.strike_sym_ls:
                if mode == 'long':
                    side = 'sell'
                    posSide = 'long'
                    slPx = avgpx - (abs(Decimal(avgpx) - Decimal(liqpx)) - Decimal('0.10')*avgpx)  # 11+
                    sl_tg = slPx + Decimal(avgpx)*Decimal('0.005')
                    tpPx = avgpx * (Decimal('1.65') / Decimal(lever))  # 50 = 0.02 = 1.02
                    tp_tg = tpPx - Decimal(avgpx)*Decimal('0.005')
                elif mode == 'short':
                    side = 'buy'
                    posSide = 'short'
                    slPx = avgpx + (abs(Decimal(avgpx) - Decimal(liqpx)) - Decimal('0.10')*avgpx)
                    sl_tg = slPx - Decimal(avgpx) * Decimal('0.005')
                    tpPx = avgpx * (Decimal('1.65') / Decimal(lever))
                    tp_tg = tpPx + Decimal(avgpx)*Decimal('0.005')
                else:
                    continue
                if avgpx == tpPx or avgpx == tp_tg:
                    if posSide == 'long':
                        tpPx = tpPx * Decimal("1.05")
                        tp_tg = tp_tg * Decimal("1.05")
                    else:
                        tpPx = tpPx * Decimal("0.95")
                        tp_tg = tp_tg * Decimal("0.95")
                elif avgpx == slPx or avgpx == sl_tg:
                    if posSide == 'long':
                        slPx = slPx * Decimal("1.05")
                        sl_tg = sl_tg * Decimal("1.05")
                    else:
                        slPx = slPx * Decimal("0.95")
                        sl_tg = sl_tg * Decimal("0.95")

                slPx = self.match_precision(slPx, avgpx)
                sl_tg = self.match_precision(sl_tg, avgpx)
                tpPx = self.match_precision(tpPx, avgpx)
                tp_tg = self.match_precision(tp_tg, avgpx)
                result = self.tradeAPI.place_algo_order(symbol, 'isolated', side, ordType='oco', tag="opoclose",
                                                   sz=sz, posSide=posSide, tpTriggerPx=str(tp_tg), tpOrdPx=str(tpPx), slTriggerPx=str(sl_tg), slOrdPx=str(slPx),
                                                  tpTriggerPxType='mark', slTriggerPxType='mark')
                res = deal_message(result)
                if res[0].get('sCode') == '0':
                    algoId = res[0].get('algoId')
                    self.order_algo[symbol] = algoId
                    print("algo_order_place_success")
                    continue
                else:
                    self.close_position(symbol, mode, sz)
                    print(res[0].get('sMsg'), symbol, slPx, sl_tg, tpPx, tp_tg, avgpx)
                    continue

            if i['uplRatio'] and symbol in self.strike_sym_ls:
                if Decimal(i['uplRatio']) >= Decimal('0.85') * Decimal("1.05"):  # Profit
                    price = i['markPx']
                    self.close_position(symbol, mode, price, sz)

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
                            order = self.tradeAPI.get_orders_history(instType="SWAP")
                            order = deal_message(order)
                            cw = check_switch(order, "opoopen", "opoclose")
                            if cw != self.trade_switch and len(self.strike_sym_ls) >= setting.opportunity_max_pos:
                                self.trade_switch = not self.trade_switch
                            self.avg_switch = False
                            return
                        res = json.loads(res)
                        if 'event' in res:
                            continue
                        elif res.get('arg') and 'data' in res:
                            symbol = res.get('arg')['instId']
                            data = res.get('data')
                            sever_time = self.get_local_timestamp()
                            if sever_time % setting.update_interval <= 10:  #if new interval update time < 10s,that new kline update ,then update data
                                self.avg_switch = False
                            if not self.avg_switch:
                                self.avg_switch = True
                                q = Queue()
                                g_thread = threading.Thread(target=self.get_price, args=(self.symbol_ls, q))
                                g_thread.start()
                                g_thread.join()
                                self.price_dict = q.get()
                                continue
                            if g_thread.is_alive():
                                continue
                            if not self.trade_switch and symbol in self.order_dict:
                                self.cancel_wait_order()
                                continue
                            # Determine whether there are opening position
                            with self.lock:
                                if isinstance(self.fluctuation_values, list) and self.trade_switch == True:
                                    if sym_idx == len(self.fluctuation_values) - 1:
                                        sym_idx = 0
                                    elif self.fluctuation_values[sym_idx] == symbol and symbol in self.ignore_temp:
                                        sym_idx = sym_idx + 1
                                        continue
                                    elif self.fluctuation_values[sym_idx] == symbol and symbol not in self.ignore_temp and symbol not in setting.Black_list and symbol not in self.all_positions:
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
                        with self.pv_lock:
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
                if tag == "opoopen":
                    self.strike_sym_ls.append(symbol)
                    try:
                        self.wx.push_order(symbol, "做多")
                        self.wx_switch = True
                    except Exception as e:
                        print(e)
                    if len(self.strike_sym_ls) < setting.opportunity_max_pos:
                        self.trade_switch = True
                    if symbol in self.order_dict:
                        del self.order_dict[symbol]
                    print("Purchase transaction")

                elif tag == "opoclose":
                    self.strike_sym_ls.remove(symbol)
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if self.profit_switch == False and Decimal(i['pnl']) > 0:  # Stop profit transactions
                        try:
                            self.wx.push_order(symbol, "止盈", i['pnl'])
                        except Exception as e:
                            print(e)
                    elif self.profit_switch == True and Decimal(i['pnl']) > 0:
                        self.profit_switch = False
                        self.position_time = 0
                        try:
                            self.wx.push_order(symbol, "动态止盈", i['pnl'])
                        except Exception as e:
                            print(e)
                    elif Decimal(i['pnl']) < 0:  # Stop loss transactions
                        try:
                            self.wx.push_order(symbol, "止损", 0, i['pnl'])
                        except Exception as e:
                            print(e)
                    self.ignore_temp = []
                    self.trade_switch = True
                elif Decimal(i['pnl']) < 0 and symbol in self.strike_sym_ls:
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if len(self.strike_sym_ls) == 1:
                        self.strike_sym_ls.remove(symbol)
                        try:
                            self.wx.push_order(symbol, "爆仓", 0, i['pnl'])
                        except Exception as e:
                            print(e)
                        self.ignore_temp = []
                        self.trade_switch = True
            elif i.get('state') == 'filled' and i['side'] == 'sell':  # Sales transaction
                symbol = i['instId']
                if tag == "opoopen":
                    self.strike_sym_ls.append(symbol)
                    try:
                        self.wx.push_order(symbol, "做空", 0)
                        self.wx_switch = True
                    except Exception as e:
                        print(e)
                    if len(self.strike_sym_ls) < setting.opportunity_max_pos:
                        self.trade_switch = True
                    if symbol in self.order_dict:
                        del self.order_dict[symbol]
                    print("Sales transaction")

                elif tag == "opoclose":
                    self.strike_sym_ls.remove(symbol)
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if self.profit_switch == False and Decimal(i['pnl']) > 0:  # Stop profit transactions
                        try:
                            self.wx.push_order(symbol, "止盈", i['pnl'])
                        except Exception as e:
                            print(e)
                    elif self.profit_switch == True and Decimal(i['pnl']) > 0:
                        self.profit_switch = False
                        self.position_time = 0
                        try:
                            self.wx.push_order(symbol, "动态止盈", i['pnl'])
                        except Exception as e:
                            print(e)
                    elif Decimal(i['pnl']) < 0:  # Stop loss transactions
                        try:
                            self.wx.push_order(symbol, "止损", i['pnl'])
                        except Exception as e:
                            print(e)
                    self.ignore_temp = []
                    self.trade_switch = True
                elif Decimal(i['pnl']) < 0 and symbol in self.strike_sym_ls:
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if len(self.strike_sym_ls) == 1:
                        self.strike_sym_ls.remove(symbol)
                        try:
                            self.wx.push_order(symbol, "爆仓", i['pnl'])
                        except Exception as e:
                            print(e)
                        self.ignore_temp = []
                        self.trade_switch = True
            else:
                continue
            if symbol in self.all_positions:
                self.all_positions.remove(symbol)
            print(self.trade_switch)
    @retry_on_exception_sync
    def close_position(self, symbol, mode, sz):  # close_position  symbol, mode, price, sz
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
                                  ordType='market', sz=sz)
        code = res.get('code')
        if code != '0':
            print("sus-market-close-error:" + res)
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
                    self.one_day_trade = setting.one_day_trade
                elif (len(self.fluctuation_values) / 2) % count_below_avg > 2:
                    self.load_interval = setting.load_interval + 10
                    self.Trigger_slip = setting.Trigger_slip
                    self.one_day_trade = setting.one_day_trade
                else:
                    cal_number = avg_abs_value + 1
                    self.Trigger_slip = setting.Trigger_slip * 1.01
                    self.one_day_trade = setting.one_day_trade * 1.25
                    self.load_interval = setting.load_interval

    def run(self):
        if not setting.opportunity_trade_switch:
            return
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
