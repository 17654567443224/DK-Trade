import sys
import asyncio
import base64
import datetime
import hmac
import json
import time
from functionns import setting
import requests
import websockets
import threading
from functionns import deal_data
from typing import Optional
import okx.Market_api as Market
import okx.Account_api as Account
import okx.Public_api as Public
from decimal import Decimal, getcontext

# 设置精度
getcontext().prec = 16
from enum import Enum

from AI.chat import run
from functionns.utils import deal_message, retry_on_exception_sync, check_switch
from queue import Queue
import okx.Trade_api as Trade
import math
from functionns.wx_webhook import wx_robot
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


class algo_score:
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
        self.order_algo = {}  # Dict of stop loss and stop loss orders
        self.fluctuation_values = {}  # kline_dym_dice，if ...
        self.get_pnl_ls()
        self.price_dict = None
        self.multiplier = self.iniy_multiplier()
        self.init_ba = self.get_banlance_all()
        self.trade_switch = True
        self.lock = threading.Lock()
        self.pv_lock = threading.Lock()
        self.ignore_temp = []
        self.profit_switch = False
        self.position_time = 0
        self.target_long_switch = False
        self.target_short_switch = False
        self.wx = wx_robot(user, "algosroce")
        self.wx_switch = False
        self.symbol_temp = []
        self.all_positions = []
        self.open_tag = "scoreopen"
        self.close_tag = "scoreclose"
        self.loss_long = []
        self.loss_short = []
        self.position_temp = []

    @retry_on_exception_sync
    def cancel_wait_order(self):
        time.sleep(0.1)
        result = deal_message(
            self.tradeAPI.get_order_list(instType='SWAP', uly='', instFamily='', instId='', ordType='limit', state='',
                                         after='',
                                         before='', limit=''))
        if result:
            for i in result:
                if i.get('state') == 'live':
                    ordId = i.get('ordId')
                    sym = i.get('instId')
                    tag = i.get('tag')
                    u_time = int(i.get('cTime')) / 1000
                    e_time = int(time.time()) - int(u_time)
                    if e_time > self.order_wait_time and sym in self.order_dict and i[
                        'algoId'] == '' and tag == self.open_tag:
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
                    res = self.marketAPI.get_markprice_candlesticks(instId=i, limit=self.load_interval,
                                                                    bar=setting.rest_interval)
                    code = res.get('code')
                    if code == '0':
                        result = deal_message(res)
                        break
                    else:
                        print(res)
                        symbol.remove(i)
                        break
                except:
                    time.sleep(2)
                    continue
            self.spot_price_dict[i] = result
            max_high_price = max(Decimal(res_max[2]) for res_max in result)
            min_low_price = min(Decimal(res_min[3]) for res_min in result)
            max_low_price = max(Decimal(res_min[3]) for res_min in result)  # max(low)o h l c
            min_high_price = min(Decimal(res_max[2]) for res_max in result)  # min(max)
            cal_price = (max_high_price + min_low_price) / Decimal(2)
            if (max_high_price - min_high_price) > Decimal(self.quick_tradingview) * cal_price and (
                    max_low_price - min_low_price) > Decimal(self.quick_tradingview) * cal_price:
                max_high_price = max_high_price * (Decimal("1") - Decimal(self.liqpx_slip))
                min_low_price = min_low_price * (Decimal("1") + Decimal(self.liqpx_slip))
            cal_ls.append((max_high_price - min_low_price) / min_low_price)
            price_ls.append([max_high_price, min_low_price])
        self.fluctuation_values = dict(zip(symbol, cal_ls))
        sym_avg_dict = dict(zip(symbol, price_ls))
        self.Dynamic_tuning()
        q.put(sym_avg_dict)

    def symbol_monitor(self, interval: Interval):
        """
        base: mark_price_?interval
        :return:
        """
        order_thread = self.order_monitor()
        while True:
            symbol_ls = deal_data.get_symbol(only_symbol=True, count=setting.symbol_count)
            if not symbol_ls:
                time.sleep(5)
                continue
            self.symbol_ls = symbol_ls
            if not order_thread.is_alive():
                print("pv_thread_error")
                order_thread = self.order_monitor()
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

    def calculate_liquidation_price(self, initial_margin_rate, notional_value, num_contracts, entry_price,
                                    maintenance_margin_rate, fee_rate, position_type):
        """
        计算USDT保证金合约的多仓或空仓强平价格，使用高精度 Decimal。

        参数:
        - initial_margin_rate (Decimal): 最低初始保证金率（如 Decimal('0.05') 表示 5%）。
        - notional_value (Decimal): 面值（每张合约的名义价值）。
        - num_contracts (int): 合约张数（正数表示多仓，负数表示空仓）。
        - entry_price (Decimal): 开仓均价。
        - maintenance_margin_rate (Decimal): 维持保证金率（如 Decimal('0.005') 表示 0.5%）。
        - fee_rate (Decimal): 手续费率（如 Decimal('0.0004') 表示 0.04%）。
        - position_type (str): 持仓类型 ("long" 表示多仓, "short" 表示空仓)。

        返回:
        - Decimal: 强平价格。
        """
        # 转换参数为 Decimal 类型（确保输入为数字或字符串）
        initial_margin_rate = Decimal(initial_margin_rate)
        notional_value = Decimal(notional_value)
        entry_price = Decimal(entry_price)
        maintenance_margin_rate = Decimal(maintenance_margin_rate)
        fee_rate = Decimal(fee_rate)
        num_contracts = Decimal(num_contracts)
        # 计算保证金余额
        margin_balance = abs(num_contracts) * notional_value * entry_price * initial_margin_rate

        # 根据持仓类型计算强平价格
        if position_type == 1:  # 多仓
            denominator = abs(num_contracts) * notional_value * (maintenance_margin_rate + fee_rate - 1)
            if denominator == 0:
                raise ZeroDivisionError("Denominator is zero during long liquidation price calculation.")
            liquidation_price = (margin_balance - abs(num_contracts) * notional_value * entry_price) / denominator
        elif position_type == 0:  # 空仓
            denominator = abs(num_contracts) * notional_value * (maintenance_margin_rate + fee_rate + 1)
            if denominator == 0:
                raise ZeroDivisionError("Denominator is zero during short liquidation price calculation.")
            liquidation_price = (margin_balance + abs(num_contracts) * notional_value * entry_price) / denominator
        else:
            raise ValueError("Invalid position type. Use 'long' for多仓 or 'short' for空仓.")

        return liquidation_price

    # data:live pricing result:key:symbol val:max,min   symbol：live_symbol  data: [['1697550300000', '28231.1', '28280.2', '28128.3', '28247.6', '0']]
    def cal_tradingview(self, result, symbol, data):
        self.target_long_switch = False
        self.target_short_switch = False
        if symbol in result:
            if symbol not in self.strike_sym_ls and symbol not in self.order_dict:
                if Decimal(data[0][2]) > Decimal(result[symbol][0]) and Decimal(data[0][3]) > Decimal(
                        result[symbol][1]):  # 0：timestamp 1：o 2：h 3：l 4：c
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
                    time_stamp = new_res[0][0]
                    ts = int(Decimal(new_res[0][0]) / Decimal('1000'))
                    time_ = int(time.time()) - ts
                    if time_ < 240:
                        new_res = new_res[1:]

                    target_long_temp = []
                    target_short_temp = []
                    total_long = 0
                    total_short = 0
                    for i in range(0, len(all_res) - 1):  # [0,1,2,3,4,5]
                        high_target = Decimal(all_res[i][2]) - Decimal(all_res[i + 1][2])
                        low_target = Decimal(all_res[i][3]) - Decimal(all_res[i + 1][3])
                        target_short_temp.append(low_target)
                        target_long_temp.append(high_target)
                        total_long = total_long + high_target
                        total_short = total_short + low_target
                    avg_total_long = total_long / Decimal(len(target_long_temp))
                    avg_total_short = total_short / Decimal(len(target_short_temp))
                    for i in target_long_temp:
                        if abs(i) < avg_total_long / Decimal('2'):
                            target_long_temp.remove(i)
                    if min(target_long_temp) > 0:
                        self.target_long_switch = True

                    for i in target_short_temp:
                        if i > avg_total_short / Decimal('2'):
                            target_short_temp.remove(i)
                    if max(target_short_temp) < 0:
                        self.target_short_switch = True

                    if (Decimal(new_res[0][2]) - Decimal(new_res[1][2])) / (
                            Decimal(new_res[0][2]) - Decimal(new_res[0][3])) > 0.382 or self.target_long_switch == True:
                        price = Decimal(data[0][2]) * Decimal(0.9995)  # 0.9995
                        price = self.match_precision(Decimal(price), Decimal(data[0][2]))  # price：str
                        trading_view = 1  # long
                        print("Trigger_long", symbol)
                        self.trading(trading_view, symbol, price, time_stamp)
                        return
                    elif (Decimal(new_res[1][3]) - Decimal(new_res[0][3])) / (
                            Decimal(new_res[0][2]) - Decimal(new_res[0][3])) > 0.618 or self.target_short_switch == True:
                        trading_view = 0  # short
                        print("Trigger_short", symbol)
                        price = Decimal(data[0][3]) * Decimal(1.0005)  # 1.0005
                        price = self.match_precision(Decimal(price), Decimal(data[0][3]))
                        self.trading(trading_view, symbol, price, time_stamp)
                        return
                elif Decimal(data[0][3]) < Decimal(result[symbol][1]) and Decimal(data[0][2]) < Decimal(
                        result[symbol][0]):
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
                    time_stamp = new_res[0][0]
                    ts = int(Decimal(new_res[0][0]) / Decimal('1000'))
                    time_ = int(time.time()) - ts
                    if time_ < 240:
                        new_res = new_res[1:]
                    target_long_temp = []
                    target_short_temp = []
                    total_long = 0
                    total_short = 0
                    for i in range(0, len(all_res) - 1):  # [0,1,2,3,4,5]
                        high_target = Decimal(all_res[i][2]) - Decimal(all_res[i + 1][2])
                        low_target = Decimal(all_res[i][3]) - Decimal(all_res[i + 1][3])
                        target_short_temp.append(low_target)
                        target_long_temp.append(high_target)
                        total_long = total_long + high_target
                        total_short = total_short + low_target
                    avg_total_long = total_long / Decimal(len(target_long_temp))
                    avg_total_short = total_short / Decimal(len(target_short_temp))
                    for i in target_long_temp:
                        if abs(i) < avg_total_long / Decimal('2'):
                            target_long_temp.remove(i)
                    if min(target_long_temp) > 0:
                        self.target_long_switch = True

                    for i in target_short_temp:
                        if i > avg_total_short / Decimal('2'):
                            target_short_temp.remove(i)
                    if max(target_short_temp) < 0:
                        self.target_short_switch = True
                    if (Decimal(new_res[1][3]) - Decimal(new_res[0][3])) / (
                            Decimal(new_res[0][2]) - Decimal(new_res[0][3])) > 0.382 or self.target_short_switch == True:
                        trading_view = 0  # short
                        print("Trigger_short", symbol)
                        price = Decimal(data[0][3]) * Decimal(1.0005)  # 1.0005
                        price = self.match_precision(Decimal(price), Decimal(data[0][3]))
                        self.trading(trading_view, symbol, price, time_stamp)
                        return
                    elif (Decimal(new_res[0][2]) - Decimal(new_res[1][2])) / (
                            Decimal(new_res[0][2]) - Decimal(new_res[0][3])) > 0.618 or self.target_long_switch == True:
                        price = Decimal(data[0][2]) * Decimal(0.9995)  # 0.9995
                        price = self.match_precision(Decimal(price), Decimal(data[0][2]))  # price：str
                        trading_view = 1  # long
                        print("Trigger_long", symbol)
                        self.trading(trading_view, symbol, price, time_stamp)
                        return

        self.trade_switch = True

    @retry_on_exception_sync
    def get_banlance_all(self):
        banlance_all = Decimal(deal_message(self.accountAPI.get_account(ccy='USDT'))[0]['details'][0]['cashBal'])
        return banlance_all

    @retry_on_exception_sync
    def get_banlance_avail(self):
        if setting.steady_switch:
            return Decimal('45')
        banlance_avail = Decimal(deal_message(self.accountAPI.get_account(ccy='USDT'))[0]['details'][0]['availBal'])
        return banlance_avail

    def get_position_tiers(self, symbol, lever, usdt, price, ctVal, tradingview):
        switch = True
        while switch == True:
            try:
                switch = False
                symbol = self.remove_swap(symbol)
                result = deal_message(self.publicAPI.get_tier(instType='SWAP', instFamily=symbol, tdMode='isolated'))
                for i in result:
                    if i['maxSz'] is None or i['minSz'] is None:
                        continue
                    elif Decimal(i['maxLever']) == Decimal(
                            lever):  # and Decimal(usdt) < Decimal(i['maxSz']) and Decimal(usdt) > Decimal(i['minSz'])
                        val = Decimal(usdt) * Decimal(lever)
                        size = self.convert_contract_coin(symbol, order_type='open', price=price, val=str(val))
                        if Decimal(size) <= Decimal(i['maxSz']) and Decimal(size) >= Decimal(i['minSz']):
                            imr = i['imr']
                            mmr = i['mmr']
                            liq_price = self.calculate_liquidation_price(imr, ctVal, size, price, mmr,
                                                                         setting.order_fee, tradingview)
                            return size, liq_price
                    elif Decimal(i['maxLever']) < Decimal(lever):
                        lever = i['maxLever']
                        continue
                return -1
            except Exception as e:
                print("get_position_tiers" + str(e))
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
    def convert_contract_coin(self, symbol, val, price,
                              order_type):  # transform_sheet_coin price:limit val：usdt order_type:  open  close
        symbol = self.remove_swap(symbol)
        cv_co = deal_message(
            self.publicAPI.convert_contract_coin(instId=f'{symbol}-SWAP', sz=val, px=str(price), opType=order_type,
                                                 unit='usds'))
        return cv_co[0].get('sz')

    def catch_error_sCode(self, code: str):
        if code == '51004':
            self.wx.normal_text("挂单超过杠杆上限")
        elif code == '51005':
            self.wx.normal_text("委托数量大于单笔上限")
        elif code == '51008':
            self.wx.normal_text("余额不足")

    def check_pending(self, symbol):
        result = deal_message(
            self.tradeAPI.get_order_list(instType='SWAP', uly='', instFamily='', instId='', ordType='limit', state='',
                                         after='',
                                         before='', limit=''))
        if result:
            for i in result:
                if i.get('state') == 'live':
                    sym = i.get('instId')
                    if sym == symbol:
                        return False
        return True

    @retry_on_exception_sync
    def trade_logic(self, trading_view, bv, lever, symbol, price, ba, ctVal, avg_val,
                    algo):  # trade_logic  tradingview, bv, lever, symbol, price, ba, ctVal
        pos_val = math.log(self.multiplier, setting.Incremental_multiplier)  # 27 3**3
        if pos_val <= setting.add_extra:  # 2
            usdt = bv / Decimal(setting.total_fail_count)
        else:
            usdt = bv / Decimal(setting.total_fail_count) * Decimal(self.multiplier) / Decimal(
                setting.Incremental_multiplier) ** Decimal(setting.add_extra)

        if usdt > ba * Decimal(setting.proportion):
            self.trade_switch = True
            print("account_empty", self.multiplier, ba)
            return
        sz = self.get_position_tiers(symbol, lever, usdt, price, ctVal, trading_view)
        live = self.check_pending(symbol + '-SWAP')
        if not live:
            self.trade_switch = True
            return
        price = Decimal(price)
        if sz == -1 or sz == '0':
            self.ignore_temp.append(symbol + '-SWAP')
            self.trade_switch = True
            return
        liq_price = Decimal(sz[1])
        sz = sz[0]
        val = avg_val / (abs(price - liq_price) / price)
        los_loss = avg_val * Decimal(lever) / Decimal(self.stop_loss)
        los_perfit = avg_val * Decimal(lever) / Decimal(self.profit_per)
        stop_loss = self.stop_loss
        stop_perfit = self.profit_per
        if algo != trading_view and self.multiplier != 1:
            if val > Decimal(100) / Decimal(lever):
                self.trade_switch = True
                return
            if los_loss > 1:
                stop_loss = Decimal(self.stop_loss) + los_loss * Decimal(0.01)

        elif algo == trading_view and self.multiplier != setting.max_fail_count:
            if los_perfit > 1:
                stop_perfit = Decimal(self.profit_per) + los_perfit * Decimal(0.01)

        trading_fee = Decimal(sz) * price * Decimal(setting.order_fee) * Decimal(ctVal)  # 张数*价格*面值*费率 100u-0.06
        fee_percent = trading_fee / (usdt * Decimal(lever))
        if trading_view == 1:  # 多
            slPx, sl_tg, tpPx, tp_tg = self.oco(symbol, trading_view, price, liq_price, lever, sz, stop_loss, stop_perfit)
            result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                  mgnMode='isolated', posSide='long')  # set lever
            """
            tpOrdKind 止盈订单类型condition: 条件单limit: 限价单默认为condition
            tpOrdPx 止盈委托价
            对于条件止盈单，如果填写此参数，必须填写 止盈触发价
            对于限价止盈单，需填写此参数，不需要填写止盈触发价
            委托价格为-1时，执行市价止盈
            """
            res = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='buy', posSide='long',
                                            px=str(price), tag=self.open_tag,
                                            ordType='limit', sz=sz, attachAlgoClOrdId=self.close_tag, tpOrdPx=tpPx, tpTriggerPx=tp_tg, tpTriggerPxType='mark', tpOrdKind='limit',
                                            slOrdPx=slPx, slTriggerPx=sl_tg, slTriggerPxType='mark'
                                            )
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
            self.order_dict[symbol + '-SWAP'] = order_id
            print("long_order", symbol, self.trade_switch, ",fee:", trading_fee, fee_percent)
            return
        elif trading_view == 0:  # short
            slPx, sl_tg, tpPx, tp_tg = self.oco(symbol, trading_view, price, liq_price, lever, sz, stop_loss,
                                                stop_perfit)
            result = self.accountAPI.set_leverage(instId=f'{symbol}-SWAP', lever=lever,
                                                  mgnMode='isolated', posSide='short')  # set_lever
            res = self.tradeAPI.place_order(instId=f'{symbol}-SWAP', tdMode='isolated', side='sell', tag=self.open_tag,
                                            posSide='short',
                                            ordType='limit', sz=sz, px=str(price), attachAlgoClOrdId=self.close_tag, tpOrdPx=tpPx, tpTriggerPx=tp_tg, tpTriggerPxType='mark', tpOrdKind='limit',
                                            slOrdPx=slPx, slTriggerPx=sl_tg, slTriggerPxType='mark')
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
            self.order_dict[symbol + '-SWAP'] = order_id
            print("short_order", symbol, self.trade_switch, ",fee:", trading_fee, fee_percent)
            self.oco(symbol, trading_view, price, liq_price, lever, sz, stop_loss, stop_perfit)
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
                if self.order_ls[i] == '0':
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
    def trading(self, tradingview, symbol, price, ts):  # 1.get_banlance  2.get_max_lever and position_cont(usdt)
        symbol = self.remove_swap(symbol)
        bv = self.get_banlance_avail()
        ba = self.get_banlance_all()
        if not setting.steady_switch:
            bv = bv * Decimal(setting.proportion)
        if int(ba) < 10:
            exit()
        result = deal_message(self.publicAPI.get_instruments(instType='SWAP', instFamily=symbol))
        lever = result[0]['lever']
        ctVal = result[0]['ctVal']
        intervals = ["15m", "1H", "4H"]
        table = symbol + '-SWAP'
        pre = run(intervals=intervals, limits=[200, 200, 200], tables=table, ts=ts)

        """
            {
                'symbol': res['table'],
                'interval': res['interval'],
                'limit': res['limit'],
                'below_avg_changes': below_avg_changes,  # 存储筛选出的涨跌幅
                'avg_change_up': avg_change_up,
                'avg_change_down': avg_change_down
            }
            up_down * 
        """
        score = 0
        # td 25  algo 25 pos 25 per/lost pos 25
        ll = len(self.loss_long)
        ls = len(self.loss_short)
        if ll + ls >= 10:
            positive_count = sum(1 for num in self.position_temp if num > 0)
            perfit_percent = positive_count / len(self.position_temp)
            perfit_rate = perfit_percent * 25
            if tradingview == 0:
                percent_pos = ll / ls if ls != 0 else 25
            else:
                percent_pos = ls / ll if ll != 0 else 25
            if percent_pos > 2:
                pos_score = 25
            else:
                pos_score = percent_pos * 12.5
        else:
            pos_score = 0
            perfit_rate = 0

        avg_temp = []
        percent_temp = []
        avg_avg = []
        for i, data in enumerate(pre):
            if data['below_avg_changes']:
                avg = sum(data['below_avg_changes']) / len(data['below_avg_changes'])
                max_dt = max(data['below_avg_changes'])
                min_dt = min(data['below_avg_changes'])
                avg_avg.append(avg)
                if max_dt - min_dt > avg * 2:
                    avg = avg / 2 ** i

                avg_temp.append(avg)
            if data['avg_change_up'] and data['avg_change_down']:
                percent = data['avg_change_up'] / abs(data['avg_change_down'])
                percent_temp.append(percent)

        positive_count = sum(1 for x in avg_avg if x > 0)  # 正数的数量
        negative_count = sum(1 for x in avg_avg if x < 0)  # 负数的数量
        if tradingview == 1:
            percent_avg = positive_count / negative_count if negative_count != 0 else 0
        else:
            percent_avg = negative_count / positive_count if positive_count != 0 else 0
        if percent_avg > 2:
            avg_score = 25
        else:
            avg_score = percent_avg * 12.5

        avg_val = (sum(avg_temp) / len(avg_temp))
        count_above_1 = sum(1 for i in percent_temp if i >= 1)
        if count_above_1 > len(percent_temp):  # 判断是否为 "long"
            algo = 1
        else:
            algo = 0
        if setting.quick_trade_switch is not None:
            if int(lever) < setting.quick_trade_switch and self.multiplier != setting.max_fail_count:
                self.ignore_temp.append(symbol + '-SWAP')
                self.trade_switch = True
                return

        score = 25 + pos_score + avg_score + perfit_rate
        if algo == tradingview:
            score = score + 25
        if self.multiplier <= setting.total_fail_count:
            if pos_score == 0:
                total_score = 50
                per = score / total_score
                if per < 0.35:
                    tradingview = 1 if tradingview == 0 else 0
                elif 0.23 <= per < 0.6:
                    self.trade_switch = True
                    self.ignore_temp.append(symbol + '-SWAP')
                    return
            else:
                total_score = 100
                per = score / total_score
                if per < 0.35:
                    tradingview = 1 if tradingview == 0 else 0
                elif 0.35 <= per < 0.6:
                    self.trade_switch = True
                    self.ignore_temp.append(symbol + '-SWAP')
                    return
        else:
            if pos_score == 0:
                total_score = 50
                per = score / total_score
                if per < 0.35:
                    tradingview = 1 if tradingview == 0 else 0
                elif 0.35 <= per < 0.75:
                    self.trade_switch = True
                    self.ignore_temp.append(symbol + '-SWAP')
                    return
            else:
                total_score = 100
                per = score / total_score
                if per < 0.35:
                    tradingview = 1 if tradingview == 0 else 0
                elif 0.35 <= per < 0.75:
                    self.trade_switch = True
                    self.ignore_temp.append(symbol + '-SWAP')
                    return

        avg_val = Decimal(avg_val)
        self.trade_logic(tradingview, bv, lever, symbol, price, ba, ctVal, avg_val, algo)

    def get_float(self, num):
        position = abs(num.as_tuple().exponent)  # 获取小数部分的长度
        result = Decimal(10) ** -position  # 计算最后一位的位权
        return result

    def order_monitor(self):
        order_thread = threading.Thread(target=self.run_in_thread)
        order_thread.start()
        return order_thread

    def oco(self, symbol, tradingview, avgpx, liqpx, lever, sz, stop_loss, stop_perfit):
        symbol = symbol + "-SWAP"
        ft = self.get_float(avgpx)
        if tradingview == 1:
            side = 'sell'
            posSide = 'long'
            slPx = avgpx * (Decimal("1") + Decimal(stop_loss) / Decimal(lever))  # 10 sl负数
            sl_tg = slPx + ft * 5
            if slPx < liqpx or sl_tg < liqpx:
                slPx = avgpx - (abs(Decimal(avgpx) - Decimal(liqpx)) - Decimal(self.liqpx_slip) * avgpx)
                sl_tg = slPx + ft * 5
            tpPx = avgpx * (Decimal("1") + Decimal(stop_perfit) / Decimal(lever))  # 50 = 0.02 = 1.02
            tp_tg = tpPx - ft * 5
        elif tradingview == 0:
            side = 'buy'
            posSide = 'short'
            slPx = avgpx * (Decimal("1") - Decimal(stop_loss) / Decimal(lever))
            sl_tg = slPx - ft * 5
            if slPx > liqpx or sl_tg > liqpx:
                slPx = avgpx + (abs(Decimal(avgpx) - Decimal(liqpx)) - Decimal(self.liqpx_slip) * avgpx)
                sl_tg = slPx - ft * 5
            tpPx = avgpx * (Decimal("1") - Decimal(stop_perfit) / Decimal(lever))
            tp_tg = tpPx + ft * 5
        else:
            return
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
        return slPx, sl_tg, tpPx, tp_tg


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
            markPx = i['markPx']
            markPx = Decimal(markPx)
            pos_time = int(int(i['pTime']) / 1000)  # least_time

            if symbol not in self.all_positions:
                self.all_positions.append(symbol)

            if i['uplRatio'] and symbol in self.strike_sym_ls:
                if Decimal(i['uplRatio']) >= Decimal(self.profit_per) * Decimal("1.05"):  # Profit
                    price = i['markPx']
                    self.close_position(symbol, mode, sz)

                elif Decimal(i['uplRatio']) > self.profit_min and Decimal(i['uplRatio']) < self.profit_min + self.float_val and self.multiplier < setting.max_fail_count:  # trends_Stop Loss
                    if self.position_time == 0:
                        self.position_time = pos_time
                    elif pos_time - self.position_time > self.position_update and self.profit_switch == False:
                        price = i['markPx']
                        self.profit_switch = True
                        self.close_position(symbol, mode, sz)
                elif Decimal(i['uplRatio']) <= Decimal(self.stop_loss):  # stop_loss
                    price = i['markPx']
                    res = self.close_position(symbol, mode, sz)

                else:
                    self.position_time = 0

            if Decimal(i['uplRatio']) > Decimal('0.3') and self.multiplier == 1 and self.wx_switch == True:
                upr = Decimal(i['uplRatio']).quantize(Decimal('0.00'))
                self.wx.push_position(symbol, liqpx, avgpx, mode, lever, upr)
                self.wx_switch = False

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
                            cw = check_switch(order, self.open_tag, self.close_tag)
                            if cw and self.trade_switch == False:
                                self.trade_switch = True
                            self.avg_switch = False
                            print("change_trade_switch:", self.trade_switch)
                            return
                        res = json.loads(res)
                        if 'event' in res:
                            continue
                        elif res.get('arg') and 'data' in res:
                            symbol = res.get('arg')['instId']
                            data = res.get('data')
                            sever_time = self.get_local_timestamp()
                            if sever_time % setting.update_interval <= 10:  # if new interval update time < 10s,that new kline update ,then update data
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
                            # Determine whether there are opening position
                            with self.lock:
                                if isinstance(self.fluctuation_values, list) and self.trade_switch == True:
                                    if sym_idx == len(self.fluctuation_values) - 1:
                                        sym_idx = 0
                                    elif self.fluctuation_values[sym_idx] == symbol and symbol in self.ignore_temp:
                                        sym_idx = sym_idx + 1
                                        continue
                                    elif self.fluctuation_values[
                                        sym_idx] == symbol and symbol not in self.ignore_temp and symbol not in self.symbol_temp and symbol not in setting.Black_list and symbol not in self.all_positions:
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
                                print("pvconn_close，retry……", e)
                                break
                        except Exception as e:
                            print("pverror", e)
                        try:
                            res = json.loads(res)
                        except:
                            print(res)
                        try:
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
                            print("code_error", e)
            except Exception as e:
                print("pv_conn_break，retry……", e)
                continue

    def deal_order(self, data):
        for i in data:
            symbol = i.get('instId')
            tag = i.get('tag')
            source = i.get('source')
            category = i.get('category')
            if i.get('state') == 'filled' and i['side'] == 'buy':  # Purchase transaction
                if tag == self.open_tag:
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
                    if symbol in self.order_dict:
                        del self.order_dict[symbol]

                elif self.trade_switch == False and tag == self.close_tag:
                    self.strike_sym_ls = []
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if self.profit_switch == False and Decimal(i['pnl']) > 0:  # Stop profit transactions
                        self.multiplier = 1
                        try:
                            self.wx.push_order(symbol, "止盈", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                    elif self.profit_switch == True and Decimal(i['pnl']) > 0:
                        self.profit_switch = False
                        self.profit_min = self.profit_min + 0.01
                        self.position_time = 0
                        try:
                            self.wx.push_order(symbol, "动态止盈", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                    elif Decimal(i['pnl']) < 0:  # Stop loss transactions
                        self.multiplier = self.multiplier * setting.Incremental_multiplier
                        try:
                            self.wx.push_order(symbol, "止损", self.multiplier, i['pnl'])
                            if len(self.loss_long + self.loss_short) > 9:
                                self.loss_short.pop(0)  # 移除最早添加的元素
                            self.loss_short.append(self.multiplier)  # 添加新的值
                        except Exception as e:
                            print(e)
                    self.position_temp.append(float(i['pnl']))
                    self.profit_per = setting.profit_per
                    self.stop_loss = setting.stop_loss
                    self.ignore_temp = []
                    self.trade_switch = True
                elif self.trade_switch == False and symbol in self.strike_sym_ls and category == 'full_liquidation':
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if len(self.strike_sym_ls) == 1:
                        self.strike_sym_ls.remove(symbol)
                        self.multiplier = self.multiplier * setting.Incremental_multiplier
                        try:
                            self.wx.push_order(symbol, "爆仓", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                        if len(self.loss_long + self.loss_short) > 9:
                            self.loss_short.pop(0)  # 移除最早添加的元素
                        self.position_temp.append(float(i['pnl']))
                        self.loss_short.append(self.multiplier)  # 添加新的值
                        self.ignore_temp = []
                        self.trade_switch = True
                        self.profit_per = setting.profit_per
                        self.stop_loss = setting.stop_loss
            elif i.get('state') == 'filled' and i['side'] == 'sell':  # Sales transaction
                symbol = i['instId']
                if tag == self.open_tag:
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
                    if symbol in self.order_dict:
                        del self.order_dict[symbol]

                elif self.trade_switch == False and tag == self.close_tag:
                    self.strike_sym_ls = []
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if self.profit_switch == False and Decimal(i['pnl']) > 0:  # Stop profit transactions
                        self.multiplier = 1
                        try:
                            self.wx.push_order(symbol, "止盈", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                    elif self.profit_switch == True and Decimal(i['pnl']) > 0:
                        self.profit_switch = False
                        self.profit_min = self.profit_min + 0.01
                        self.position_time = 0
                        try:
                            self.wx.push_order(symbol, "动态止盈", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                    elif Decimal(i['pnl']) < 0:  # Stop loss transactions
                        self.multiplier = self.multiplier * setting.Incremental_multiplier
                        try:
                            self.wx.push_order(symbol, "止损", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                        self.loss_long.append(self.multiplier)  # 添加新的值
                        if len(self.loss_long + self.loss_short) > 9:
                            self.loss_long.pop(0)  # 移除最早添加的元素
                    self.position_temp.append(float(i['pnl']))
                    self.profit_per = setting.profit_per
                    self.stop_loss = setting.stop_loss
                    self.ignore_temp = []
                    self.trade_switch = True
                elif self.trade_switch == False and symbol in self.strike_sym_ls and category == 'full_liquidation':
                    if symbol in self.order_algo:
                        del self.order_algo[symbol]
                    if len(self.strike_sym_ls) == 1:
                        self.strike_sym_ls.remove(symbol)
                        self.multiplier = self.multiplier * setting.Incremental_multiplier
                        try:
                            self.wx.push_order(symbol, "爆仓", self.multiplier, i['pnl'])
                        except Exception as e:
                            print(e)
                        self.ignore_temp = []
                        self.trade_switch = True
                        self.profit_per = setting.profit_per
                        self.stop_loss = setting.stop_loss
                    self.position_temp.append(float(i['pnl']))
                    self.loss_long.append(self.multiplier)  # 添加新的值
                    if len(self.loss_long + self.loss_short) > 9:
                        self.loss_long.pop(0)  # 移除最早添加的元素

            else:
                continue
            if symbol in self.all_positions:
                self.all_positions.remove(symbol)
            if len(self.position_temp) > 10:
                self.position_temp.pop(0)
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
        res = self.tradeAPI.place_order(instId=symbol, tdMode='isolated', side=side, tag=self.close_tag,
                                        posSide=posSide,
                                        ordType='market', sz=sz)
        code = res.get('code')
        if code != '0':
            print("default-market-close-error:", res)

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
                self.fluctuation_values = sorted(self.fluctuation_values,
                                                 key=self.fluctuation_values.get)  # Fluctuation sorting key
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
        self.symbol_monitor(setting.interval)


if __name__ == '__main__':
    asd = algo_score(setting.user)
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