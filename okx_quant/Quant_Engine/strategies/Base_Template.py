import json
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, time
from decimal import Decimal
from queue import Empty
from typing import List, Union, Tuple
import time
import numpy as np
import pandas as pd

from Quant_Engine.Common.constants import Exchange, Interval
from Quant_Engine.Common.object import BarData
from Quant_Engine.WebSocketManager import WebSocketProducer
from Quant_Engine.template.open_position_template.target import ArrayManager
import okx.Market_api as Market
from Quant_Engine.utils import retry_on_exception_sync, deal_message
from crawl_data import download_future, conn_database, conn_strategy_database, creat_table, create_strategy_position_table, \
    create_strategy_orders_table


class Base_Template(ABC):
    def __init__(self, id, lever, account, ws:WebSocketProducer, sz=100, interval=Interval.CANDLE_15m.value, max_positions=10, funSymbol_selection=None, funOpen_position=None, funProfit_loss=None, funFund=None):
        self.id = id
        self.ws = ws
        self.lever = lever
        self.sz = sz  # ArrayManager的sz
        self.interval = interval  # 时间粒度（1m,5m,15m等等）
        self.account = account  # 账户信息
        self.max_positions = max_positions
        self.funSymbol_selection = funSymbol_selection
        self.funOpen_position = funOpen_position
        self.funProfit_loss = funProfit_loss
        self.funFund = funFund
        self.marketAPI = Market.MarketAPI(True)
        if not self.account['position']:
            self.account['position'] = {}
        if not self.account['orders']:
            self.account['orders'] = {}
        self.data_queue = self.ws.register_consumer()  # 注册ws来接收数据
        self.running = False
        self.init_balance = float(self.account["balance"])
        self.bars = {}
        self.symbol_ls = []
        self.account["balance"] = Decimal(self.account["balance"])
        self.account["orderFee"] = float(self.account["orderFee"])
        self.latest_prices = {}  # 存储最新的ticker价格
        
        # 初始化策略方法
        self.ss_method = self.symbol_selection  # 默认使用子类的 symbol_selection 方法
        self.pl_method = None  # 默认使用子类的止盈止损方法
        self.fd_method = None  # 资金管理方法默认为 None
        
        # 确保创建策略相关的数据库表
        try:
            create_strategy_position_table()
            create_strategy_orders_table()
        except Exception as e:
            print(f"创建策略相关数据库表失败: {e}")

    def run(self):
        """启动模拟引擎
        """
        self.running = True
        while self.running:
            try:
                # 1. 获取实时数据 (非阻塞)
                res = self.data_queue.get_nowait()
                if 'event' in res:
                    continue

                elif res.get('arg') and 'data' in res:
                    # 调用选股方法
                    ss = self.ss_method(**self.funSymbol_selection['args'])
                    if ss:
                        self.symbol_ls = ss
                    mode = res.get('arg')['channel']
                    symbol = res.get('arg')['instId']
                    if "candle" in mode:
                        if symbol in self.symbol_ls:
                            data = res.get('data')
                            bar = BarData(gateway_name=Exchange.OKX, symbol=symbol, exchange=Exchange.OKX,
                                          datetime=data[0][0], interval=self.interval,
                                          volume=data[0][5], turnover=data[0][7], open_price=data[0][1], high_price=data[0][2],
                                          low_price=data[0][3], close_price=data[0][4]
                                          )
                            if symbol in self.bars:
                                am: ArrayManager = self.bars[symbol]
                                am.update_bar(bar)
                                if not am.inited:
                                    continue
                                self._process_data(am, symbol)
                                continue
                            am = ArrayManager(self.sz)
                            am.update_bar(bar)
                            self.bars[symbol] = am
                    elif mode == "tickers":
                        if symbol in self.account["position"]:
                            data = res.get('data')
                            price = float(data[0]['last'])
                            # 更新最新ticker价格
                            self.latest_prices[symbol] = Decimal(str(price))
                            td = self.account["position"][symbol]["posSide"]
                            self._check_exit_condition(symbol, td, price)
            except Empty:
                continue  # 无新数据时跳过

    @abstractmethod
    def symbol_selection(self, **kwargs):
        """
        选股策略
        :return:
        """

    def _process_data(self, am: ArrayManager, symbol):
        pos = self.account["position"]
        # 4. 检查开仓信号
        if symbol in pos:
            return
        td = self.op_method(am=am)
        print(len(pos))
        if td is not False and len(pos) < self.max_positions:
            self._execute_order(symbol, td)

    @abstractmethod
    def op_method(self, am:ArrayManager):
        """开仓策略"""

    def _execute_order(self, symbol: str, td:int):
        """执行开仓逻辑"""
        price = self.get_ticker(symbol)
        asks, bids = self.get_orderBook(symbol)
        if asks == 0 or bids == 0:
            return
        # 1. 计算止盈止损
        tp_price, sl_price = self.pl_method(symbol, td, price)
        tp_price = self.match_precision(tp_price, price)
        sl_price = self.match_precision(sl_price, price)

        # 2. 计算开仓数量
        sz = self.fd_method(
            td=td,
            symbol=symbol,
            price=price,
        )
        if sz == -1 or sz == '0' or not sz:
            return
        liq_price = sz[1]
        if sz[0] == -1 or sz[0] == '0' or sz[0] == 0 or sz[0] is False:
            return
        lever = sz[2]
        if td == 0:
            posSide = "short"
            order_type = "sell"
            if sl_price > sz[1]:
                sl_price = sz[1]
        else:
            posSide = "long"
            order_type = "buy"
            if sl_price < sz[1]:
                sl_price = sz[1]
        # price, sz = self.match_order(price, volume=sz[0], order_type=order_type, asks=asks, bids=bids) 延迟太高，误差太大，算法有问题（数据推送的是张数）暂时取消
        price = self.match_precision(price, sl_price)
        if price is False or sz is False:
            return
        # 3. 更新账户状态
        sz = sz[0]
        order_price = Decimal(str(sz)) / Decimal(lever)
        if self.account["balance"] < order_price:
            return
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        self.account["position"][symbol] = {
            "sz": sz,
            "lever": lever,
            "entry_price": price,
            "liq_price": liq_price,
            "tp": tp_price,
            "sl": sl_price,
            "open_time": formatted_time,
            "posSide": posSide
        }

        # 4. 写入持仓数据到数据库
        try:
            # 获取策略ID
            strategy_id = self.id

            # 连接数据库
            connection, cursor = conn_strategy_database()

            # 准备SQL语句和参数
            insert_sql = """
                INSERT INTO user_strategy_position 
                (strategy_id, symbol, lever, sz, entry_price, tp, sl, liq_price, createTime) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
            """
            params = (
                strategy_id,
                symbol,
                lever,
                str(sz),
                str(price),
                str(tp_price),
                str(sl_price),
                str(liq_price),
                formatted_time
            )

            # 执行SQL
            cursor.execute(insert_sql, params)
            connection.commit()

            cursor.close()
            connection.close()

        except Exception as e:
            print(f"数据库写入持仓信息失败: {e}")

    @retry_on_exception_sync
    def get_ticker(self, symbol):
        res = deal_message(self.marketAPI.get_ticker(instId=symbol))
        data = res[0]
        price = Decimal(data["last"])  #
        self.latest_prices[symbol] = price  # 更新缓存
        return price

    def match_precision(self, dec1: Decimal, dec2: Decimal):  # match_precision
        precision = abs(dec2.as_tuple().exponent)
        format_str = "{:." + str(precision) + "f}"
        result_str = format_str.format(dec1)
        return Decimal(result_str)

    @retry_on_exception_sync
    def get_orderBook(self, symbol):
        res = self.marketAPI.get_orderbook(instId=symbol, sz=5)
        res = deal_message(res)
        data = res[0]
        asks = data["asks"]
        bids = data["bids"]
        return asks, bids

    @abstractmethod
    def _check_exit_condition(self, symbol, td, price):
        """
        检查止盈止损
        :param symbol: 交易对
        :param price: 价格
        :return:
        """

    def _close_position(self, symbol: str, exit_price: float, exit_type: str):
        """平仓操作"""
        entry_price = Decimal(self.account["position"][symbol]["entry_price"])
        lever = self.account["position"][symbol]["lever"]
        liq_price = self.account["position"][symbol]["liq_price"]
        position = self.account["position"].pop(symbol)
        posSide = position["posSide"]
        pnl = 0
        pnl_ratio = 0
        # asks, bids = self.get_orderBook(symbol)
        # if asks == 0 or bids == 0:
        #     return
        sz = Decimal(str(position["sz"]))  # 已含杠杆的开仓价值

        if posSide == "long":
            # close, vol = self.match_order(Decimal(exit_price), Decimal(sz), order_type="sell", asks=asks, bids=bids)延迟太高，误差太大，算法有问题（数据推送的是张数）暂时取消

            # # 滑点调整（可选）
            # if Decimal(close) < Decimal(exit_price):
            #     close = (Decimal('1') - (Decimal(Decimal(exit_price)) - Decimal(close)) / Decimal(exit_price) * Decimal(
            #         '0.005')) * Decimal(close)

            # 强平检查（平仓价低于强平价时惩罚）
            if Decimal(exit_price) < Decimal(liq_price):
                exit_price = Decimal(exit_price) * Decimal('0.9995')
            exit_price = self.match_precision(exit_price, entry_price)
            # 计算盈亏和盈亏率（无需杠杆）
            pnl = (Decimal(exit_price) - entry_price) / entry_price * sz
            pnl_ratio = pnl / (sz / Decimal(lever))

        elif posSide == "short":
            # close, vol = self.match_order(Decimal(exit_price), Decimal(sz), order_type="buy", asks=asks, bids=bids)延迟太高，误差太大，算法有问题（数据推送的是张数）暂时取消

            # # 滑点调整（可选）
            # if Decimal(exit_price) < Decimal(close):
            #     close = (Decimal('1') + (Decimal(close) - Decimal(exit_price)) / Decimal(exit_price) * Decimal(
            #         '0.005')) * Decimal(close)

            # 强平检查（平仓价高于强平价时惩罚）
            if Decimal(exit_price) < Decimal(liq_price):
                exit_price = Decimal(exit_price) * Decimal('1.0005')
            exit_price = self.match_precision(exit_price, entry_price)
            # 计算盈亏和盈亏率（无需杠杆）
            pnl = (entry_price - Decimal(exit_price)) / entry_price * sz
            pnl_ratio = pnl / (sz / Decimal(lever))
        
        # 使用Decimal计算账户余额更新
        fee = Decimal(str(self.account["orderFee"])) * Decimal(str(position["sz"]))
        self.account["balance"] = self.account["balance"] + pnl - fee * Decimal('2')
        
        # 计算收益率
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        key = symbol + "/" + formatted_time
        # 记录平仓订单
        self.account["orders"][key] = {
            "type": "close",
            "entry_price": entry_price,
            "price": exit_price,
            "sz": position["sz"],
            "lever": lever,
            "time": time.time(),
            "pnl": float(pnl),  # 转为float以便后续处理
            "pnl_ratio": float(pnl_ratio),
            "exit_type": exit_type
        }
        
        # 写入平仓订单数据到数据库
        try:
            # 获取策略ID
            strategy_id = self.id
            
            # 连接数据库
            connection, cursor = conn_strategy_database()
            
            # 准备SQL语句和参数
            insert_sql = """
                INSERT INTO user_strategy_orders 
                (strategy_id, symbol, lever, type, entry_price, price, sz, time, pnl, pnl_ratio, exit_type) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            params = (
                strategy_id,
                symbol,
                lever,
                "close",  # type固定为close
                str(position["entry_price"]),
                str(exit_price),
                str(position["sz"]),
                formatted_time,
                str(float(pnl)),
                str(pnl_ratio),
                exit_type
            )
            
            # 执行SQL
            cursor.execute(insert_sql, params)
            connection.commit()
            
            # 同时删除对应的持仓记录
            delete_sql = """
                DELETE FROM user_strategy_position 
                WHERE strategy_id = %s AND symbol = %s
            """
            cursor.execute(delete_sql, (strategy_id, symbol))
            connection.commit()
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            print(f"数据库写入订单信息失败: {e}")

    def match_order(self, price, volume, order_type: str, asks: List[List[Union[str, float]]],
                    bids: List[List[Union[str, float]]]) -> Tuple[float, float]:
        """
        根据传入的价格、张数和买卖类型来判断订单是否能够成交，
        如果无法成交则匹配价格最相近的订单。
        :param price: 传入的价格
        :param volume: 传入的数量（张数）
        :param order_type: 订单类型，'buy' 或 'sell'，分别代表买单和卖单
        :param asks: 当前的卖单（asks）列表
        :param bids: 当前的买单（bids）列表
        :return: 返回成交的价格和成交数量，如果不能成交，返回最接近的价格。
        """
        # 安全检查，防止空的订单簿
        if not asks or not bids:
            return False, False
            
        if order_type == "buy":
            # 对买单，寻找卖单（asks）中最低的价格
            for ask in asks:
                ask_price = Decimal(ask[0])
                ask_volume = Decimal(ask[1])

                # 如果卖单的价格低于或等于买单的价格，且卖单数量足够
                if ask_price <= price and ask_volume >= volume:
                    return ask_price, volume

            # 防止无法找到合适的卖单
            try:
                # 如果没有直接能成交的卖单，寻找最接近的卖单
                valid_asks = [ask for ask in asks if Decimal(ask[0]) <= price]
                if valid_asks:
                    closest_ask = min(valid_asks, key=lambda x: float(x[0]))
                    closest_price = Decimal(closest_ask[0])
                    closest_volume = Decimal(closest_ask[1])
                    return closest_price, min(volume, closest_volume)
                else:
                    # 如果没有价格低于买单价格的卖单，找一个最低的卖单
                    closest_ask = min(asks, key=lambda x: Decimal(x[0]))
                    closest_price = Decimal(closest_ask[0])
                    closest_volume = Decimal(closest_ask[1])
                    return closest_price, min(volume, closest_volume)
            except Exception as e:
                print(f"买单匹配失败: {e}")
                return False, False

        elif order_type == "sell":
            # 对卖单，寻找买单（bids）中最高的价格
            for bid in bids:
                bid_price = Decimal(bid[0])
                bid_volume = Decimal(bid[1])

                # 如果买单的价格高于或等于卖单的价格，且买单数量足够
                if bid_price >= price and bid_volume >= volume:
                    return bid_price, volume

            # 防止无法找到合适的买单
            try:
                # 如果没有直接能成交的买单，寻找最接近的买单
                valid_bids = [bid for bid in bids if Decimal(bid[0]) >= price]
                if valid_bids:
                    closest_bid = max(valid_bids, key=lambda x: Decimal(x[0]))
                    closest_price = Decimal(closest_bid[0])
                    closest_volume = Decimal(closest_bid[1])
                    return closest_price, min(volume, closest_volume)
                else:
                    # 如果没有价格高于卖单价格的买单，找一个最高的买单
                    closest_bid = max(bids, key=lambda x: Decimal(x[0]))
                    closest_price = Decimal(closest_bid[0])
                    closest_volume = Decimal(closest_bid[1])
                    return closest_price, min(volume, closest_volume)
            except Exception as e:
                print(f"卖单匹配失败: {e}")
                return False, False
        else:
            return False, False

    def stop(self):
        """停止模拟并生成报告"""
        self.running = False
        self.ws.remove_consumer(self.data_queue)
        return self.generate_report()

    def generate_report(self):
        """生成策略绩效报告（包含胜率、最大回撤、最大收益等）"""
        # 从订单记录中重建equity数据
        equity_data = []
        current_balance = self.init_balance
        
        # 将订单按时间排序
        ordered_trades = []
        for key, order in self.account["orders"].items():
            ordered_trades.append({
                "timestamp": order["time"],
                "pnl": order["pnl"]
            })
        
        # 按时间戳排序
        ordered_trades.sort(key=lambda x: x["timestamp"])
        
        # 构建equity曲线
        for trade in ordered_trades:
            current_balance += trade["pnl"]
            equity_data.append({
                "timestamp": trade["timestamp"],
                "equity": current_balance
            })
        
        # 获取最终余额（包含未平仓头寸）
        final_balance = self._calculate_final_balance()
        
        # 如果没有交易记录，或者只有一个记录，创建有效的equity数据集
        if len(equity_data) < 2:
            # 添加初始余额点
            start_time = time.time() - 86400  # 一天前
            equity_data = [
                {
                    "timestamp": start_time,
                    "equity": self.init_balance
                },
                {
                    "timestamp": time.time(),
                    "equity": final_balance
                }
            ]
        else:
            # 添加当前时间的最终余额
            equity_data.append({
                "timestamp": time.time(),
                "equity": final_balance
            })
        
        # 转换为DataFrame
        df_equity = pd.DataFrame(equity_data)
        df_orders = pd.DataFrame(self.account["orders"].values()) if self.account["orders"] else pd.DataFrame()

        # 计算total_pnlRatio - 使用final_balance而不是account["balance"]
        total_pnl_ratio = (final_balance - self.init_balance) / self.init_balance if self.init_balance > 0 else 0.0
        
        # 计算关键指标
        report = {
            "final_balance": final_balance,
            "max_drawdown": self._calculate_max_drawdown(df_equity),
            "win_rate": self._calculate_win_rate(df_orders) if not df_orders.empty else 0.0,
            "max_profit": self._calculate_max_profit(df_orders) if not df_orders.empty else 0.0,
            "max_loss": self._calculate_max_loss(df_orders) if not df_orders.empty else 0.0,
            "total_trades": len(df_orders),
            "sharpe_ratio": self._calculate_sharpe(df_equity),
            "annualized_return": self._calculate_annualized_return(df_equity),
            "total_pnlRatio": total_pnl_ratio,
        }
        res = json.dumps(report, indent=2)
        return res

    # ====================== 指标计算辅助函数 ====================== #
    def _calculate_final_balance(self):
        """计算最终余额（含未平仓持仓的浮动盈亏）"""
        balance = self.account["balance"]
        for symbol, position in self.account["position"].items():
            # 优先使用缓存的ticker价格
            if symbol in self.latest_prices:
                current_price = self.latest_prices[symbol]
            else:
                # 如果缓存中没有，则使用get_ticker获取实时价格
                try:
                    current_price = self.get_ticker(symbol)
                except Exception as e:
                    # 如果获取实时价格失败，则使用入场价格作为后备
                    print(f"获取{symbol}实时价格失败: {e}，使用入场价格")
                    current_price = Decimal(str(position["entry_price"]))
                
            position_size = Decimal(str(position["sz"]))
            entry_price = Decimal(str(position["entry_price"]))
            
            # 根据仓位方向计算浮动盈亏
            if position["posSide"] == "long":
                # 多头: 盈亏 = 仓位价值 * (当前价格 - 入场价格) / 入场价格
                pnl = position_size * (current_price - entry_price) / entry_price
            else:
                # 空头: 盈亏 = 仓位价值 * (入场价格 - 当前价格) / 入场价格
                pnl = position_size * (entry_price - current_price) / entry_price
            
            balance += pnl
            
        return float(balance)  # 返回float类型以便json序列化

    def _calculate_win_rate(self, df_orders):
        """计算胜率（盈利交易占比）"""
        if df_orders.empty:
            return 0.0
        win_count = len(df_orders[df_orders["pnl"] > 0])
        return win_count / len(df_orders)

    def _calculate_max_profit(self, df_orders):
        """计算单次最大盈利"""
        return df_orders["pnl"].max() if not df_orders.empty else 0.0

    def _calculate_max_loss(self, df_orders):
        """计算单次最大亏损"""
        return df_orders["pnl"].min() if not df_orders.empty else 0.0

    def _calculate_annualized_return(self, df_equity):
        """计算年化收益率"""
        if len(df_equity) < 2:
            return 0.0
        
        # 修复时间戳计算 - 不需要除以1000*86400，因为time.time()返回的是秒
        time_diff = df_equity["timestamp"].iloc[-1] - df_equity["timestamp"].iloc[0]
        days = time_diff / 86400  # 直接转换秒到天
        
        # 计算总收益率
        total_return = (df_equity["equity"].iloc[-1] / df_equity["equity"].iloc[0]) - 1
        
        # 如果交易时间不足一天，直接返回非年化收益率
        if days < 1:
            return total_return
            
        # 否则计算年化收益率
        return (1 + total_return) ** (365 / days) - 1

    # 保留原有最大回撤和夏普比率计算
    def _calculate_max_drawdown(self, df: pd.DataFrame) -> float:
        if len(df) < 2:
            return 0.0
        df["peak"] = df["equity"].cummax()
        df["drawdown"] = (df["equity"] - df["peak"]) / df["peak"]
        return float(df["drawdown"].min())  # 确保返回float而不是numpy类型

    def _calculate_sharpe(self, df: pd.DataFrame, risk_free=0.0) -> float:
        if len(df) < 2:
            return 0.0
            
        # 计算每日收益率
        returns = df["equity"].pct_change().dropna()
        
        if returns.empty:
            return 0.0
            
        # 避免标准差为0的情况
        std_dev = returns.std()
        if std_dev == 0 or np.isnan(std_dev):
            return 0.0
            
        # 计算夏普比率并确保返回有效数值
        sharpe = (returns.mean() - risk_free) / std_dev * np.sqrt(252)
        
        # 检查并修复无效值
        if np.isnan(sharpe) or np.isinf(sharpe):
            return 0.0
            
        return float(sharpe)  # 确保返回float而不是numpy类型

    def backtesting(self, symbol: str, interval: str, start: str, end: str):
        """执行回测逻辑"""
        # 1. 加载历史数据
        self.load_data(symbol, interval, start, end)

        # 2. 从数据库读取历史数据
        connection, cursor = conn_database()
        table_name = f"{symbol}_{interval}"
        cursor.execute(f"SELECT timestamp, open, high, low, close, volume FROM {table_name} ORDER BY timestamp ASC")
        historical_data = cursor.fetchall()
        connection.close()
        self.bars = {}

        # 4. 按时间顺序处理历史数据
        for record in historical_data:
            # 构造BarData对象
            bar = BarData(
                gateway_name=Exchange.OKX,
                symbol=symbol,
                exchange=Exchange.OKX,
                datetime=datetime.fromtimestamp(record[0] / 1000),
                interval=self.interval,
                open_price=float(record[1]),
                high_price=float(record[2]),
                low_price=float(record[3]),
                close_price=float(record[4]),
                volume=float(record[5]),
                turnover=float(record[5]) * float(record[4])  # 假设成交额为volume*close
            )

            # 更新ArrayManager
            if symbol not in self.bars:
                self.bars[symbol] = ArrayManager(self.sz)
            am = self.bars[symbol]
            am.update_bar(bar)

            # 模拟实时处理
            self._process_data(am, symbol)

            # 4. 生成详细报告（不再强制平仓）
        report = json.loads(self.generate_report())
        return json.dumps(report, indent=2, default=str)

    def load_data(self, symbol, interval, start, end):
        """智能加载数据：检查现有数据范围，仅下载缺失部分"""
        table_name = f"{symbol}_{interval}"

        # 1. 创建表（如果不存在）
        creat_table(table_name=table_name)

        # 2. 查询数据库现有时间范围
        connection, cursor = conn_database()
        try:
            # 获取最早和最晚时间戳
            cursor.execute(f"""
                SELECT MIN(timestamp), MAX(timestamp) 
                FROM {table_name}
            """)
            min_ts, max_ts = cursor.fetchone()

            # 处理全新表的情况
            existing_start = datetime.fromtimestamp(min_ts / 1000).strftime('%Y-%m-%d') if min_ts else None
            existing_end = datetime.fromtimestamp(max_ts / 1000).strftime('%Y-%m-%d') if max_ts else None

            # 3. 确定需要下载的时间段
            required_start_dt = datetime.strptime(start, '%Y-%m-%d')
            required_end_dt = datetime.strptime(end, '%Y-%m-%d')

            download_ranges = []

            # 情况1：数据库无数据
            if not existing_start:
                download_ranges.append((start, end))

            else:
                existing_start_dt = datetime.strptime(existing_start, '%Y-%m-%d')
                existing_end_dt = datetime.strptime(existing_end, '%Y-%m-%d')

                # 需要补充早于现有数据的部分
                if required_start_dt < existing_start_dt:
                    download_ranges.append((
                        start,
                        (existing_start_dt - timedelta(days=1)).strftime('%Y-%m-%d')
                    ))

                # 需要补充晚于现有数据的部分
                if required_end_dt > existing_end_dt:
                    download_ranges.append((
                        (existing_end_dt + timedelta(days=1)).strftime('%Y-%m-%d'),
                        end
                    ))

            # 4. 执行增量下载
            for dl_start, dl_end in download_ranges:
                print(f"Downloading missing data: {dl_start} to {dl_end}")
                download_future(symbol, interval, dl_start, dl_end)

        finally:
            cursor.close()
            connection.close()
