import asyncio
import base64
import hmac
import json
import okx.Account_api as Account
import zlib
import requests
import websockets
import datetime
import logging
import okx.Public_api as Public
import time
import okx.TradingBot_api as TradingBot
import okx.Market_api as Market
import okx.Trade_api as Trade
from decimal import Decimal



class sym_1m_strategyV1demo():
    symbol_1 = {}
    grid_trade_ls = []
    boom_count = 1
    get_30min_switch = 0
    get_2m_switch = 0
    pos_switch = 0

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.stop = False
        self.accountAPI = Account.AccountAPI(False)
        self.TradingBot = TradingBot.TradingBotAPI(False)
        self.marketAPI = Market.MarketAPI(True)
        self.tradeAPI = Trade.TradeAPI(False)
        self.publicAPI = Public.PublicAPI(False)
        self.timer2 = None
        self.timer1 = None

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

    def login_params(self, timestamp, api_key, passphrase, secret_key):
        message = timestamp + 'GET' + '/users/self/verify'

        mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        sign = base64.b64encode(d)

        login_param = {"op": "login", "args": [{"apiKey": api_key,
                                                "passphrase": passphrase,
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

    async def get_1m_Kline(self, message, sym):
        global get_30min_switch
        global get_2m_switch
        # print(get_2m_switch,get_30min_switch)
        data = json.loads(message)
        datas = data.get('data')
        if datas != None:
            open_price = datas[0][1]
            high_price = datas[0][2]
            low_price = datas[0][3]
            # print(high_price, low_price)
            sym['high_price'] = high_price
            sym['low_price'] = low_price
            if get_30min_switch == 10:  # ?????
                if self.timer2 is None:
                    await self.get_direction_30min()
                    print("创建timer2，自动启动")
            if get_2m_switch == 10:
                if self.timer1 is None:
                    print("创建协程任务，自动启动")
                    await self.get_direction_2m(sym, open_price)

    async def get_direction_30min(self, symbol=setting.symbol):
        global get_30min_switch
        result = self.marketAPI.get_markprice_candlesticks(f'{symbol}-USDT-SWAP', bar='30m', limit=2)
        asd = json.dumps(result)
        qwe = json.loads(asd)
        data = qwe.get('data')
        filtered_data = [d for d in data if d[-1] == '1']
        for data in filtered_data:
            if data[-1] == '1':
                filtered_data = data
                break
        price_high = Decimal(filtered_data[2])  # 获取第1个子列表中第3个元素，即 1678.63
        price_low = Decimal(filtered_data[3])
        open_price = Decimal(filtered_data[1])
        cal = (price_high - price_low) / open_price
        if cal < 1 or (cal > -1 and cal < 0) and get_30min_switch < 11:  ################
            grid_switch = 1  # 开启网格
            await self.grid_trade(grid_switch=grid_switch)
            self.logger.info("网格下单成功")
            get_30min_switch = 11
        else:
            get_30min_switch = 2

    async def get_direction_2m(self, dict, open):
        global get_2m_switch
        high_price = Decimal(dict["high_price"])
        low_price = Decimal(dict["low_price"])
        open_price = Decimal(open)
        cal = (high_price - low_price) / open_price
        cal_dir_high = high_price - open_price
        cal_dir_low = open_price - low_price
        if cal * Decimal('100') > Decimal(
                setting.cal_price) and get_2m_switch < 11:  #######################################
            grid_switch = 0  # 关闭网格   ##############################
            await self.grid_trade(grid_switch=grid_switch)
            trading_view = await self.tk.get_Kline(f'{setting.symbol}-USDT-SWAP')
            print(trading_view)
            await self.trend_trade(trend_switch=trading_view)
            get_2m_switch = 11

    def get_avail_bal(self, ):
        accountAPI = self.accountAPI
        result = accountAPI.get_account('USDT')
        res = json.dumps(result)
        results = json.loads(res)
        data = results.get('data')
        balance_dict = data[0]  # 获取第一个字典
        avail_bal = balance_dict['details'][0]['availBal']  # 获取 availBal 值
        return avail_bal

    def get_15min_mid(self, symbol=setting.symbol):
        result = self.marketAPI.get_markprice_candlesticks(f'{symbol}-USDT-SWAP', bar='15m', limit=1)
        asd = json.dumps(result)
        qwe = json.loads(asd)
        data = qwe.get('data')
        price_high = Decimal(data[0][2])  # 获取第1个子列表中第3个元素，即 1678.63
        price_low = Decimal(data[0][3])
        price_mid = (price_high + price_low) / 2
        return price_mid

    def get_markprice(self, symbol=setting.symbol):
        result = self.publicAPI.get_mark_price('SWAP', instId=f'{symbol}-USDT-SWAP')
        asd = json.dumps(result)
        qwe = json.loads(asd)
        data = qwe.get('data')
        mark_px = data[0]["markPx"]
        return mark_px

    # 标记价格K线频道 Mark Price Candlesticks Channel
    # channels = [{"channel": "mark-price-candle1D", "instId": "BTC-USD-201225"}]

    def get_mark_Kline(self, symbol=setting.symbol):
        channels = [{f"channel": "mark-price-candle1m", "instId": f"{symbol}-USDT-SWAP"}]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = asyncio.ensure_future(self.subscribe_without_login(self.pbc_url, channels))
        self.order()
        loop.run_until_complete(task)

    # 订单频道 Order Channel
    # channels = [{"channel": "orders", "instType": "FUTURES", "uly": "BTC-USD", "instId": "BTC-USD-201225"}]
    def order(self):
        channels = [{"channel": "orders", "instType": "ANY"}]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.subscribe(self.prv_url, self.api_key, self.passphrase, self.secret_key, channels))

    def get_size(self, trade_count, mark_price, symbol=setting.symbol):
        result = self.publicAPI.convert_contract_coin(type='1', instId=f'{symbol}-USDT-SWAP', sz=trade_count,
                                                      px=mark_price,
                                                      unit='usdt')  # 张币转化
        asd = json.dumps(result)
        qwe = json.loads(asd)
        data = qwe.get('data')
        sz = data[0]['sz']
        return sz

    async def trend_trade(self, trend_switch, symbol=setting.symbol):
        global boom_count
        global get_2m_switch
        avail_bal = self.get_avail_bal()
        result = self.accountAPI.set_leverage(instId=f'{symbol}-USDT-SWAP', lever=setting.level, mgnMode='isolated')
        trade_count = Decimal(avail_bal) * (Decimal('1') - Decimal(setting.distribution_ratio)) / setting.max_fail_count
        mark_price = self.get_markprice()
        if trend_switch == 1:  # 做多
            if boom_count <= setting.max_fail_count:
                trade_count_1 = trade_count * Decimal(boom_count)
                tpTriggerPx = Decimal(mark_price) * Decimal('1.0051')  # 止盈
                slTriggerPx = Decimal(mark_price) * Decimal('0.9951')  # 止损
                size = self.get_size(trade_count_1 * setting.level, mark_price)
                result = self.tradeAPI.place_order(instId=f'{symbol}-USDT-SWAP', tdMode='isolated', side='buy',
                                                   ordType='market', sz=size, quickMgnType='manual',
                                                   tpTriggerPx=str(tpTriggerPx), tpOrdPx='-1',
                                                   slTriggerPx=str(slTriggerPx), slOrdPx='-1')
                self.logger.info(f"做多下单成功，boom：0,data:{result},张币转化{size},下单USDT数{trade_count_1}")
            else:
                self.logger.info("GG")
                exit()
        elif trend_switch == 0:  # 做空
            if boom_count <= setting.max_fail_count:
                trade_count_1 = trade_count * Decimal(boom_count)
                tpTriggerPx = Decimal(mark_price) * Decimal('0.9949')  # 止盈
                slTriggerPx = Decimal(mark_price) * Decimal('1.0049')  # 止损
                size = self.get_size(trade_count_1 * setting.level, mark_price)
                result = self.tradeAPI.place_order(instId=f'{symbol}-USDT-SWAP', tdMode='isolated', side='sell',
                                                   ordType='market', sz=size, quickMgnType='manual',
                                                   tpTriggerPx=str(tpTriggerPx), tpOrdPx='-1',
                                                   slTriggerPx=str(slTriggerPx), slOrdPx='-1')
                self.logger.info(f"做空下单成功，boom：0,data:{result},张币转化{size},下单USDT数{trade_count_1}")
            else:
                self.logger.info("GG")
                exit()

    async def grid_trade(self, grid_switch, symbol=setting.symbol):
        # 网格策略下单
        if grid_switch == 1:
            price_15min_mid = self.get_15min_mid()
            maxkPx = price_15min_mid * Decimal('1.01')
            minPx = price_15min_mid * Decimal('0.99')
            trade_account = self.get_avail_bal()
            account = Decimal(trade_account) * Decimal(setting.distribution_ratio)  # ??
            result = self.TradingBot.grid_order_algo(instId=f'{symbol}-USDT-SWAP', algoOrdType='contract_grid',
                                                     maxPx=str(maxkPx), minPx=str(minPx), gridNum='5',
                                                     runType='2', tpTriggerPx='', slTriggerPx='', tag='', baseSz='1',
                                                     sz=str(account), lever='50', direction='neutral')
            asd = json.dumps(result)
            qwe = json.loads(asd)
            algo_id = qwe["data"][0]["algoId"]
            self.grid_trade_ls.append(algo_id)
            with open('../log/data_load_id.txt', 'w') as f:
                f.write(str(self.grid_trade))
                f.close()
            self.logger.info(f"网格开始{result}")
        # 停止策略
        if grid_switch == 0:
            if self.grid_trade:
                algo_id = self.grid_trade_ls[0]
                result = self.TradingBot.grid_stop_order_algo(algoId=algo_id, instId=f'{symbol}-USDT-SWAP',
                                                              algoOrdType='contract_grid',
                                                              stopType='1')
                self.grid_trade_ls.clear()
                self.logger.info(f"网格停止{result}")
                with open('../log/data_load_id.txt', 'w') as f:
                    f.truncate(0)
                    f.close()

    # subscribe channels un_need login
    async def subscribe_without_login(self, url, channels):
        l = []
        global get_30min_switch
        global get_2m_switch
        log_count = 0
        while True:
            try:
                async with websockets.connect(url) as ws:

                    sub_param = {"op": "subscribe", "args": channels}
                    sub_str = json.dumps(sub_param)
                    await ws.send(sub_str)
                    # print(f"send: {sub_str}")

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
                        if self.stop == True:
                            exit()
                        elif channels[0]["channel"] == "mark-price-candle1m":
                            await self.get_1m_Kline(res, self.symbol_1)
                            print(res)
                            if get_30min_switch < 100 and get_2m_switch < 100:
                                get_30min_switch += 1
                                get_2m_switch += 1
                        else:
                            get_2m_switch = 6
                        res = eval(res)
            except Exception as e:
                if log_count == 0:
                    self.logger.warning(f"{e},连接断开，正在重连……")
                    log_count = log_count + 1
                continue

    async def order_message(self, message):
        global get_30min_switch
        global get_2m_switch
        global boom_count
        data = json.loads(message)
        datas = data.get('data')
        if datas != None:
            if datas[0]['state'] == 'filled':
                if Decimal(datas[0]['pnl']) < Decimal('0'):  # 止损单触发
                    boom_count *= 3
                    self.logger.info("止损")
                    get_30min_switch = 6
                    get_2m_switch = 8
                elif Decimal(datas[0]['pnl']) > Decimal('0'):  # 止盈单触发
                    boom_count = 1
                    self.logger.info("止盈")
                    get_30min_switch = 6
                    get_2m_switch = 8
            with open('../log/data_load_count.txt', 'w') as f:
                f.write(str(boom_count))
                f.close()
        else:
            get_2m_switch = 6
            if self.grid_trade_ls:
                print("已有网格")
            else:
                get_30min_switch = 2
            print("暂无订单信息")

    def pos_message(self, message):  ################################
        if message:
            # data = json.loads(message)
            datas = message.get('data')
            trade_count = self.get_avail_bal()
            print(trade_count)
            # if datas is None or not datas:
            if not datas or datas[0]['adl'] == '' or self.pos_switch == 1:
                if Decimal(trade_count) > Decimal(setting.account_balance):
                    self.get_mark_Kline()
                else:
                    get_30min_switch = 11
                    get_2m_switch = 11
                    self.logger.info(f"已有仓位:{datas}")
                    time.sleep(5)
                    self.position()
        elif message is None:
            self.logger.info("等待pos")
            self.position()

    # 查看持仓信息  Get Positions
    # result = accountAPI.get_positions('FUTURES', 'BTC-USD-210402')
    def position(self):
        result = self.accountAPI.get_positions('SWAP')
        self.pos_message(result)
        return result

    # subscribe channels need login
    async def subscribe(self, url, api_key, passphrase, secret_key, channels, pos_switch=None):
        log_count = 0
        while True:
            try:
                async with websockets.connect(url) as ws:
                    # login
                    timestamp = str(self.get_local_timestamp())
                    login_str = self.login_params(timestamp, api_key, passphrase, secret_key)
                    await ws.send(login_str)
                    # print(f"send: {login_str}")
                    res = await ws.recv()
                    # print(res)
                    # subscribe
                    sub_param = {"op": "subscribe", "args": channels}
                    sub_str = json.dumps(sub_param)
                    await ws.send(sub_str)
                    # print(f"send: {sub_str}")

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
                        if channels[0]["channel"] == "orders":
                            await self.order_message(res)
                        else:
                            print(res)
                        # print(res)

            except Exception as e:
                if log_count == 0:
                    self.logger.warning(f"{e},连接断开，正在重连……")
                    log_count = log_count + 1
                continue

    # trade
    async def trade(self, url, api_key, passphrase, secret_key, trade_param):
        while True:
            try:
                async with websockets.connect(url) as ws:
                    # login
                    timestamp = str(self.get_local_timestamp())
                    login_str = self.login_params(timestamp, api_key, passphrase, secret_key)
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
                print(e)
                continue

    # unsubscribe channels
    async def unsubscribe(self, url, api_key, passphrase, secret_key, channels):
        async with websockets.connect(url) as ws:
            # login
            timestamp = str(self.get_local_timestamp())
            login_str = self.login_params(timestamp, api_key, passphrase, secret_key)
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
    async def unsubscribe_without_login(self, url, channels):
        async with websockets.connect(url) as ws:
            # unsubscribe
            sub_param = {"op": "unsubscribe", "args": channels}
            sub_str = json.dumps(sub_param)
            await ws.send(sub_str)
            print(f"send: {sub_str}")

            res = await ws.recv()
            print(f"recv: {res}")

    def run(self):
        try:
            asd = sym_1m_strategyV1demo()
            pos = asd.position()
            print(pos)
        except Exception as e:
            exit()


if __name__ == '__main__':
    a = sym_1m_strategyV1demo()
    a.run()
