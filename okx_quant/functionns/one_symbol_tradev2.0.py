
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
import sys
import math
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
    def __init__(self):
        self.load_interval = setting.load_interval  # 根据几根kline计算avg
        self.liqpx_slip = setting.liqpx_slip  # 强平提前止损百分比，默认百分之五
        self.Trigger_slip = setting.Trigger_slip  # 触发价提前百分比
        self.order_wait_time = setting.order_wait_time  # 订单成交的等待时间120
        self.quick_tradingview = setting.quick_tradingview # 获取最近10根kline ，纯趋势单边， 幅度大于？
        self.profit_per = setting.profit_per  # 利润百分比
        self.stop_loss = setting.stop_loss  #  止损百分比
        self.position_update = setting.position_update  # 动态止盈的时间450
        self.profit_min = setting.profit_min  # 动态止盈最低值0.35
        self.float_val = setting.float_val  # 动态止盈波动值0.05
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
        self.strike_sym_ls = []  # 成交的订单
        self.order_ls = []  # 历史仓位信息
        self.order_dict = {}  # 订单字典（发出的订单，成交未知）
        self.order_algo = {}  # 止盈止损订单字典
        self.fluctuation_values = {}  # kline波动值字典，有无...
        self.get_pnl_ls()
        self.price_dict = None
        self.multiplier = self.iniy_multiplier()
        self.init_ba = self.get_banlance_all()
        self.symbol_ls_pr = []
        self.trade_switch = True
        self.ignore_temp = []
        self.profit_switch = False
        self.position_time = 0

    @retry_on_exception_sync
    def cancel_wait_order(self):
        result = deal_message(self.tradeAPI.get_order_list(instType='SWAP', uly='', instFamily='', instId='', ordType='limit', state='', after='',
                                         before='', limit=''))

        if result:
            for i in result:
                if i.get('state') == 'live':
                    ordId = i.get('ordId')
                    sym = i.get('instId')
                    sym_swap = sym + '-SWAP'
                    u_time = int(i.get('uTime')) / 1000
                    e_time = int(int(self.get_server_time()) / 1000) - int(u_time)
                    time.sleep(0.1)
                    if e_time > self.order_wait_time and sym_swap in self.order_dict[sym] and i['algoId'] == "":
                        res = deal_message(self.tradeAPI.cancel_order(sym, ordId=ordId))
                        if res[0].get('sMsg') == "":
                            print("撤单成功")
                            self.trade_switch = True
                            if sym in self.order_dict:
                                del self.order_dict[sym]
                        else:
                            print("撤单失败")
            return 1

    def get_pnl_ls(self):
        #  限速十秒一次	 String	否	平仓类型1：部分平仓;2：完全平仓;3：强平;4：强减; 5：ADL自动减仓;  缓存
        while True:
            try:
                print("获取历史仓位")
                res = deal_message(
                    self.accountAPI.get_positions_history(instType='SWAP', instId='', mgnMode='isolated', type='2',
                                                          after=self.get_server_time(), before='',
                                                          limit='', posId=''))
                if res:
                    for i in res:
                        r = i.get('pnl')
                        self.order_ls.append(r)
                    print("历史仓位获取完成", self.order_ls)
                    break
            except:
                print("网络卡顿")
                time.sleep(10)

    def get_price(self, symbol: list, q: Queue):  # load_interval：根据多少跟kline计算
        """
        返回symbol和avg组成的字典
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
                time.sleep(2)
            while True:  # 无限循环直到获取成功
                try:
                    result = deal_message(self.marketAPI.get_markprice_candlesticks(instId=i, limit=self.load_interval, bar=setting.rest_interval))
                    break  # 成功获取，退出无限循环
                except:
                    time.sleep(0.2)  # 2秒延迟再次尝试
                    continue  # 重新尝试
            max_high_price = max(Decimal(res_max[2]) for res_max in result)
            min_low_price = min(Decimal(res_min[3]) for res_min in result)
            max_low_price = max(Decimal(res_min[3]) for res_min in result)  # 最低价里面的最高价o h l c
            min_high_price = min(Decimal(res_max[2]) for res_max in result)  # 最高价里面的最低价
            cal_price = (max_high_price + min_low_price) / Decimal(2)
            if (max_high_price - min_high_price) > Decimal(self.quick_tradingview)*cal_price and (max_low_price - min_low_price) > Decimal(self.quick_tradingview)*cal_price:
                max_high_price = Decimal(result[0][2])
                min_low_price = Decimal(result[0][3])
            cal_ls.append((max_high_price - min_low_price) / ((max_high_price + min_low_price) / Decimal(2)))
            price_ls.append([max_high_price, min_low_price])
        self.fluctuation_values = dict(zip(symbol, cal_ls))
        print("成功获取交易对")
        sym_avg_dict = dict(zip(symbol, price_ls))
        print(sym_avg_dict)
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
            print("监控交易对")
            thread = threading.Thread(target=self.run_public_thread, args=(symbol_ls, interval.value,))
            thread.start()
            thread.join()

    def run_public_thread(self, symbol_ls, interval):
        self.start_time = time.time()
        print("异步启动")
        asyncio.run(self.subscribe_symbol(symbol_ls, interval, ))

    async def subscribe_symbol(self, symbol: list, interval):
        channels = []
        for s in symbol:
            channels.append({"channel": "mark-price-" + interval, "instId": str(s)})
        print("订阅数据")
        await self.subscribe_without_login(channels, url=setting.mark_klprice)

    # data:实时价格 result:key:symbol val:max,min   symbol：实时交易对  data: [['1697550300000', '28231.1', '28280.2', '28128.3', '28247.6', '0']]
    async def cal_tradingview(self, result, symbol, data):
        if symbol in result:
            if symbol not in self.strike_sym_ls and symbol not in self.order_dict:
                if Decimal(data[0][2]) > Decimal(result[symbol][0]) and Decimal(data[0][3]) > Decimal(result[symbol][1]):  # 0：时间戳 1：o 2：h 3：l 4：c
                    price = Decimal(data[0][2]) * Decimal(0.9995)
                    price = self.match_precision(Decimal(price), Decimal(data[0][2]))  # price：str
                    trading_view = 1  # 多
                    print("触发开多")
                    await self.trading(trading_view, symbol, price)
                    return
                elif Decimal(data[0][3]) < Decimal(result[symbol][1]) and Decimal(data[0][2]) > Decimal(result[symbol][0]):
                    trading_view = 0  # 空
                    print("触发开空")
                    price = Decimal(data[0][3]) * Decimal(1.0005)
                    price = self.match_precision(Decimal(price), Decimal(data[0][3]))
                    await self.trading(trading_view, symbol, price)
                    return
                else:
                    self.trade_switch = True

    @retry_on_exception_sync
    def get_banlance_all(self):  #  获取总余额
        banlance_all = Decimal(deal_message(self.accountAPI.get_account(ccy='USDT'))[0]['details'][0]['cashBal'])
        return banlance_all

    @retry_on_exception_sync
    def get_banlance_avail(self):  #  获取可用余额
        banlance_avail = Decimal(deal_message(self.accountAPI.get_account(ccy='USDT'))[0]['details'][0]['availBal'])
        return banlance_avail

    def get_position_tiers(self, symbol, lever, usdt, price):  # 获取仓位档位
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

    def match_precision(self, dec1: Decimal, dec2: Decimal):  # 精度转化
        precision = abs(dec2.as_tuple().exponent)
        format_str = "{:." + str(precision) + "f}"
        result_str = format_str.format(dec1)
        return result_str

    @retry_on_exception_sync
    def convert_contract_coin(self, symbol, val, price, order_type):  # 张币转化 price:限价 val：usdt数 order_type:  open开仓  close：平仓
        cv_co = deal_message(self.publicAPI.convert_contract_coin(instId=f'{symbol}-SWAP', sz=val, px=str(price), opType=order_type,unit='usds'))
        return cv_co[0].get('sz')

    @retry_on_exception_sync
    def dynamic_param(self, symbol):
        symbol = self.remove_swap(symbol) + '-SWAP'
        result = deal_message(
            self.marketAPI.get_markprice_candlesticks(instId=symbol, limit=5, bar=setting.rest_interval))
        max_high_price = max(Decimal(res_max[2]) for res_max in result)
        min_low_price = min(Decimal(res_min[3]) for res_min in result)
        # max_low_price = max(Decimal(res_min[3]) for res_min in result)  # 最低价里面的最高价o h l c
        # min_high_price = min(Decimal(res_max[2]) for res_max in result)  # 最高价里面的最低价
        sum_price = (max_high_price - min_low_price) / ((max_high_price + min_low_price) / Decimal(2))
        # 通过指数函数映射结果到权重范围内
        weight = 1 / math.exp(-sum_price)  # 指数函数
        weight_d = 1 / weight
        sum_val = Decimal((1 - weight_d)).log10()
        sum_val = abs(math.ceil(sum_val))  # 取绝对值并向上取整
        self.liqpx_slip = setting.liqpx_slip * weight
        self.order_wait_time = setting.order_wait_time / sum_val
        self.profit_per = setting.profit_per * (sum_val / 100 + 1)
        self.stop_loss = setting.stop_loss
        self.position_update = setting.position_update - 10 * sum_val
        self.profit_min = setting.profit_min + 0.05 * sum_val
        self.float_val = setting.float_val + 0.005 * sum_val

    @retry_on_exception_sync
    def trade_logic(self, trading_view, bv, lever, symbol, price, ba):  # 交易逻辑
        if self.init_ba / Decimal(setting.total_fail_count) * Decimal(self.multiplier) > bv:
            self.trade_switch = True
            print("余额不足", self.multiplier)
            return
        self.dynamic_param(symbol)
        usdt = self.init_ba / Decimal(setting.total_fail_count) * Decimal(self.multiplier)
        sz = self.get_position_tiers(symbol, lever, usdt, price)
        if sz == -1:
            self.ignore_temp.append(symbol+'-SWAP')
            self.trade_switch = True
            return
        if trading_view == 1:  # 多
            result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                  mgnMode='isolated', posSide='long')  # 设置杠杆
            res = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='buy', posSide='long', px=str(price),
                                               ordType='limit', sz=sz, banAmend='',
                                               quickMgnType='manual')
            order_id = deal_message(res)[0].get('ordId')
            code = res.get('code')
            if code != '0':
                self.trade_switch = True
                return
            self.order_dict[symbol+'-SWAP'] = order_id
            print("开多", res, symbol)
            return
        elif trading_view == 0:  # 空
            result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                  mgnMode='isolated', posSide='short')  # 设置杠杆
            res = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='sell',
                                            posSide='short',
                                            ordType='limit', sz=sz, banAmend='', px=str(price),
                                            quickMgnType='manual')
            order_id = deal_message(res)[0].get('ordId')
            code = res.get('code')
            if code != '0':
                self.trade_switch = True
                return
            self.order_dict[symbol+'-SWAP'] = order_id
            print("开空", res, symbol)
            return
        self.trade_switch = True

    def iniy_multiplier(self):
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
                    multiplier = multiplier * 3
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

    @retry_on_exception_decorator
    async def trading(self, tradingview, symbol, price):  # 1.获取账户余额  2.获取交易对最大可开杠杆倍数和开仓数量
        symbol = self.remove_swap(symbol)
        bv = self.get_banlance_avail()
        ba = self.get_banlance_all()
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
        print(f"准备开仓,余额：{bv}")

    def order_monitor(self):
        order_thread = threading.Thread(target=self.run_in_thread)
        order_thread.start()
        if not order_thread.is_alive():
            return self.order_monitor()

    def run_position(self, result):
        for i in result:
            symbol = i['instId']
            if symbol in self.strike_sym_ls:  # self.strike_sym_ls????????
                liqpx = i['liqPx']
                avgpx = i['avgPx']
                avgpx = Decimal(avgpx)
                mode = i['posSide']
                sz = i['availPos']
                pos_time = int(int(i['pTime']) / 1000)
                if mode == 'long':
                    side = 'sell'
                    posSide = 'long'
                    slPx = avgpx - (abs(Decimal(avgpx) - Decimal(liqpx)) + Decimal(self.liqpx_slip)*avgpx)  # 11+
                    sl_tg = slPx + Decimal(avgpx)*Decimal(self.Trigger_slip)
                    tpPx = avgpx + (abs(Decimal(avgpx) - Decimal(liqpx)) + Decimal(self.liqpx_slip)*avgpx)
                    tp_tg = tpPx - Decimal(avgpx)*Decimal(self.Trigger_slip)
                elif mode == 'short':
                    side = 'buy'
                    posSide = 'short'
                    slPx = avgpx + (abs(Decimal(avgpx) - Decimal(liqpx)) - Decimal(self.liqpx_slip)*avgpx)
                    sl_tg = slPx - Decimal(avgpx) * Decimal(self.Trigger_slip)
                    tpPx = avgpx - (abs(Decimal(avgpx) - Decimal(liqpx)) - Decimal(self.liqpx_slip)*avgpx)
                    tp_tg = tpPx + Decimal(avgpx)*Decimal(self.Trigger_slip)
                else:
                    continue
                if symbol not in self.order_algo:
                    slPx = self.match_precision(slPx, avgpx)
                    sl_tg = self.match_precision(sl_tg, avgpx)
                    tpPx = self.match_precision(tpPx, avgpx)
                    tp_tg = self.match_precision(tp_tg, avgpx)
                    result = self.tradeAPI.place_algo_order(symbol, 'isolated', side, ordType='oco',
                                                       sz=sz, posSide=posSide, tpTriggerPx=str(tp_tg), tpOrdPx=str(tpPx),slTriggerPx=str(sl_tg),slOrdPx=str(slPx),
                                                      tpTriggerPxType='mark', slTriggerPxType='mark')
                    res = deal_message(result)
                    print(res)
                    if res[0].get('sCode') == '0':
                        algoId = res[0].get('algoId')
                        self.order_algo[symbol] = algoId
                        print("止盈止损下单成功")
                        break
                    else:
                        print(res[0].get('sMsg'), symbol, slPx, sl_tg, tpPx, tp_tg, avgpx)

                if i['uplRatio']:
                    if Decimal(i['uplRatio']) >= Decimal(self.profit_per):  # 止盈
                        price = i['markPx']
                        self.close_position(symbol, mode, price, sz)

                    elif Decimal(i['uplRatio']) > self.profit_min and Decimal(i['uplRatio']) < self.profit_min + self.float_val:  # 动态止盈
                        if pos_time - self.position_time > self.position_update and self.profit_switch == False:
                            price = i['markPx']
                            self.profit_switch = True
                            self.close_position(symbol, mode, price, sz)

                        elif self.position_time == 0:
                            self.position_time = pos_time

                    elif Decimal(i['uplRatio']) <= Decimal(self.stop_loss):  # 止损
                        price = i['markPx']
                        res = self.close_position(symbol, mode, price, sz)

                    else:
                        self.position_time = 0

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
        # print('全量数据bids为：' + str(bids))
        # print('档数为：' + str(len(bids)))
        # print('全量数据asks为：' + str(asks))
        # print('档数为：' + str(len(asks)))
        return bids, asks, instrument_id

    def update_bids(self, res, bids_p):
        # 获取增量bids数据
        bids_u = res['data'][0]['bids']
        # print('增量数据bids为：' + str(bids_u))
        # print('档数为：' + str(len(bids_u)))
        # bids合并
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
            # print('合并后的bids为：' + str(bids_p) + '，档数为：' + str(len(bids_p)))
        return bids_p

    def update_asks(self, res, asks_p):
        # 获取增量asks数据
        asks_u = res['data'][0]['asks']
        # print('增量数据asks为：' + str(asks_u))
        # print('档数为：' + str(len(asks_u)))
        # asks合并
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
            # print('合并后的asks为：' + str(asks_p) + '，档数为：' + str(len(asks_p)))
        return asks_p

    def sort_num(self, n):
        if n.isdigit():
            return int(n)
        else:
            return float(n)

    def check(self, bids, asks):
        # 获取bid档str
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
        # 获取ask档str
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
        # 拼接str
        num = ''
        if len(bid_l) == len(ask_l):
            for m in range(len(bid_l)):
                num += bid_l[m] + ':' + ask_l[m] + ':'
        elif len(bid_l) > len(ask_l):
            # bid档比ask档多
            for n in range(len(ask_l)):
                num += bid_l[n] + ':' + ask_l[n] + ':'
            for l in range(len(ask_l), len(bid_l)):
                num += bid_l[l] + ':'
        elif len(bid_l) < len(ask_l):
            # ask档比bid档多
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
                                print("连接关闭，正在重连……", e)
                                break
                        # print(self.get_timestamp() + res)
                        if time.time() - self.start_time >= setting.update_interval*10:
                            self.avg_switch = False
                            return
                        res = json.loads(res)
                        print(self.trade_switch)
                        if 'event' in res:
                            continue
                        elif res.get('arg') and 'data' in res:
                            symbol = res.get('arg')['instId']
                            data = res.get('data')
                            sever_time = self.get_local_timestamp()
                            if sever_time % setting.update_interval <= 10:  # 如果新的interval更新时间小于10秒，则认为新的kline出现，更新数据
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
                            if not self.trade_switch:
                                self.cancel_wait_order()
                                continue
                            # 判断有无开仓条件
                            if isinstance(self.fluctuation_values, list) and self.trade_switch == True:
                                if sym_idx == len(self.fluctuation_values) - 1:
                                    sym_idx = 0
                                elif self.fluctuation_values[sym_idx] == symbol and symbol in self.ignore_temp:
                                    sym_idx = sym_idx + 1
                                    continue
                                elif self.fluctuation_values[sym_idx] == symbol and symbol not in self.ignore_temp:
                                    self.trade_switch = False
                                    await self.cal_tradingview(self.price_dict, symbol, data)
                                elif count == len(self.fluctuation_values) - sym_idx - 1:
                                    sym_idx = sym_idx + 1
                                    count = 0
                                else:
                                    count = count + 1

            except Exception as e:
                print(e)
                print("pb连接断开，正在重连……")
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
                                print("连接关闭，正在重连……")
                                break
                        res = json.loads(res)
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
                print("pv连接断开，正在重连……", e)
                continue

    def deal_order(self, data):
        for i in data:
            symbol = i.get('instId')
            if i.get('state') == 'filled' and i['side'] == 'buy':  #  买单成交
                if symbol not in self.strike_sym_ls:
                    self.strike_sym_ls.append(symbol)
                    print("买单成交")

                elif symbol in self.strike_sym_ls:
                    self.strike_sym_ls = [x for x in self.strike_sym_ls if x != symbol]
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if self.profit_switch == False and Decimal(i['pnl']) > 0:  # 止盈成交
                        self.multiplier = 1
                    elif self.profit_switch == True and Decimal(i['pnl']) > 0:
                        self.profit_switch = False
                        self.profit_min = self.profit_min + 0.1
                    elif Decimal(i['pnl']) < 0:  # 止损成交
                        self.multiplier = self.multiplier * 3
                    self.ignore_temp = []
                    self.trade_switch = True
            elif i.get('state') == 'filled' and i['side'] == 'sell':  # 卖单成交
                symbol = i['instId']
                if symbol not in self.strike_sym_ls:
                    self.strike_sym_ls.append(symbol)
                    print("卖单成交")

                elif symbol in self.strike_sym_ls:
                    self.strike_sym_ls = [x for x in self.strike_sym_ls if x != symbol]
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if self.profit_switch == False and Decimal(i['pnl']) > 0:  # 止盈成交
                        self.multiplier = 1
                    elif self.profit_switch == True and Decimal(i['pnl']) > 0:
                        self.profit_switch = False
                        self.profit_min = self.profit_min + 0.1
                    elif Decimal(i['pnl']) < 0:  # 止损成交
                        self.multiplier = self.multiplier * 3
                    self.ignore_temp = []
                    self.trade_switch = True
            else:
                continue
            if symbol in self.order_dict:
                del self.order_dict[symbol]

    @retry_on_exception_sync
    def close_position(self, symbol, mode, price, sz):  # 平仓  symbol, mode, price, sz
        """
        开多：买入开多（side 填写 buy； posSide 填写 long ）
        开空：卖出开空（side 填写 sell； posSide 填写 short ）
        平多：卖出平多（side 填写 sell；posSide 填写 long ）
        平空：买入平空（side 填写 buy； posSide 填写 short ）
        """

        if mode == 'long':
            side = 'sell'
            posSide = 'long'
        elif mode == 'short':
            side = 'buy'
            posSide = 'short'
        else:
            return
        res = self.tradeAPI.place_order(instId=symbol, tdMode='isolated', side=side,
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
                                print("连接关闭，正在重连……")
                                break

                        print(self.get_timestamp() + res)

            except Exception as e:
                print("连接断开，正在重连……")
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
        load_interval = 10  # 根据几根kline计算avg
        liqpx_slip = 0.0009  # 强平提前止损百分比，默认百分之五
        Trigger_slip = 0.0009  # 触发价提前百分比
        order_wait_time = 120  # 订单成交的等待时间120
        quick_tradingview = 0.02 # 获取最近10根kline ，纯趋势单边， 幅度大于？
        profit_per = 1  # 利润百分比
        stop_loss = -1  #  止损百分比
        position_update = 5  # 动态止盈的时间450
        profit_min = 0.15  # 动态止盈最低值0.35
        float_val = 0.05  # 动态止盈波动值0.05
        one_day_trade = 200000000
        """
        if not self.avg_switch:
            if isinstance(self.fluctuation_values, dict):
                temp = self.fluctuation_values
                self.fluctuation_values = sorted(self.fluctuation_values, key=self.fluctuation_values.get)  # 波动排序的key
                # 计算绝对值平均值
                abs_values = [abs(value) for value in temp.values()]
                avg_abs_value = sum(abs_values) / len(abs_values)
                # 计算小于平均值的值的个数
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
        self.symbol_monitor(setting.interval)

if __name__ == '__main__':
    asd = websocket_funs()
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