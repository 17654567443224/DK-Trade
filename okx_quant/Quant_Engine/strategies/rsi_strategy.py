from typing import List, Union, Tuple
import numpy as np
from datetime import datetime
from decimal import Decimal
from Quant_Engine.Common.constants import Exchange, Interval
from Quant_Engine.Common.object import BarData
from Quant_Engine.template.open_position_template.target import ArrayManager
from Quant_Engine.WebSocketManager import WebSocketProducer
from Quant_Engine.strategies.Base_Template import Base_Template
from Quant_Engine.utils import deal_message
from Quant_Engine.template.symbols_selection.priceTimeInterval import priceTimeInterval


class RSIStrategy(Base_Template):
    """
    RSI（相对强弱指标）交易策略
    
    策略说明：
    - RSI > 超买线时，等待RSI回落后产生做空信号
    - RSI < 超卖线时，等待RSI回升后产生做多信号
    
    参数说明：
    - sz: ArrayManager的数据窗口大小
    - interval: K线周期
    - account: 账户信息
    - ws: WebSocket连接
    - rsi_period: RSI计算周期
    - overbought: 超买阈值
    - oversold: 超卖阈值
    - symbol_selection: 外部选股策略
    - profit_loss: 外部止盈止损策略
    - fund: 外部资金管理策略
    """
    
    def __init__(
            self,
            id,
            account: dict,
            ws: WebSocketProducer,
            sz=100,
            interval=Interval.CANDLE_15m.value,
            rsi_period: int = 14,
            overbought: float = 70,
            oversold: float = 30,
            symbol_selection=None,
            profit_loss=None,
            fund=None,
            funSymbol_selection=None,
            funOpen_position=None,
            funProfit_loss=None,
            funFund=None
    ):
        super().__init__(id, account, ws, sz, interval)
        
        # 策略参数
        self.rsi_period = rsi_period
        self.overbought = overbought
        self.oversold = oversold
        
        # 外部策略配置
        self.funSymbol_selection = funSymbol_selection or {'func': 'default_symbol_selection', 'args': {}}
        self.funProfit_loss = funProfit_loss or {'func': 'default_profit_loss', 'args': {}}
        self.funFund = funFund or {'func': 'default_fund', 'args': {}}
        
        # 策略实例和方法绑定
        if symbol_selection and hasattr(symbol_selection, self.funSymbol_selection['func']):
            self.ss_method = getattr(symbol_selection, self.funSymbol_selection['func'])
        else:
            self.ss_method = self.default_symbol_selection
            
        if profit_loss and hasattr(profit_loss, self.funProfit_loss['func']):
            self.pl_method = getattr(profit_loss, self.funProfit_loss['func'])
        else:
            self.pl_method = self.default_profit_loss
            
        if fund and hasattr(fund, self.funFund['func']):
            self.fd_method = getattr(fund, self.funFund['func'])
        else:
            self.fd_method = self.default_fund
            
        # 初始化选股器
        self.symbol_selector = priceTimeInterval(symbol_count=20, update_interval=240)  # 4小时更新一次

    def default_symbol_selection(self) -> List[str]:
        """
        默认选股策略：按24小时成交量选择交易对
        """
        try:
            symbols = self.symbol_selector.filter_symbolByVolCcy24h(trade=100000000)  # 1亿交易额
            if symbols:
                return symbols

        except Exception as e:
            print(f"选股异常: {e}")
            return []

    def default_profit_loss(self, symbol: str, td: int, price: float) -> Tuple[float, float]:
        """
        默认止盈止损策略：基于ATR的动态止盈止损
        """
        try:
            # 使用2倍ATR作为止盈止损范围
            atr = self.bars[symbol].atr(14, array=True)[-1]
            
            if td == 1:  # 做多
                tp_price = price + (atr * 2)
                sl_price = price - (atr * 1)
            else:  # 做空
                tp_price = price - (atr * 2)
                sl_price = price + (atr * 1)
                
            return tp_price, sl_price
        except Exception as e:
            print(f"止盈止损计算异常: {e}")
            return price * 1.02, price * 0.98

    def default_fund(self, td: int, symbol: str, price: float, lever: float = None) -> Tuple[float, float]:
        """
        默认资金管理策略：基于RSI强度的动态仓位，考虑杠杆因素
        """
        try:
            # 获取当前RSI值
            rsi = self.bars[symbol].rsi(self.rsi_period)[-1]
            
            # 使用传入的杠杆或默认杠杆
            leverage = Decimal(str(lever)) if lever is not None else Decimal(str(self.lever))
            
            # 根据RSI强度调整仓位
            if td == 1:  # 做多
                strength = (self.oversold - rsi) / self.oversold
            else:  # 做空
                strength = (rsi - self.overbought) / (100 - self.overbought)
                
            # 计算基础仓位大小（最大使用账户余额的20%）
            base_position = self.account["balance"] * Decimal('0.2') * Decimal(str(abs(strength)))
            
            # 考虑杠杆因素计算实际可开的仓位数量
            leveraged_position = base_position * leverage
            volume = leveraged_position / Decimal(str(price))
            
            # 计算强平价格（维持保证金率假设为0.5%）
            maintenance_margin_rate = Decimal('0.005')
            if td == 1:  # 做多
                liq_price = Decimal(str(price)) * (Decimal('1') - Decimal('1')/leverage + maintenance_margin_rate)
            else:  # 做空
                liq_price = Decimal(str(price)) * (Decimal('1') + Decimal('1')/leverage - maintenance_margin_rate)
            
            return float(volume), float(liq_price)
        except Exception as e:
            print(f"资金管理异常: {e}")
            return -1, 0

    def op_method(self, am: ArrayManager):
        """
        RSI开仓策略：基于RSI的超买超卖信号
        """
        if not am.inited:
            return False
            
        # 计算RSI
        rsi_array = am.rsi(self.rsi_period, array=True)
        rsi = rsi_array[-1]
        prev_rsi = rsi_array[-2]
            
        # 生成交易信号
        if prev_rsi <= self.oversold and rsi > self.oversold:
            # RSI从超卖区上穿，做多信号
            return 1
        elif prev_rsi >= self.overbought and rsi < self.overbought:
            # RSI从超买区下穿，做空信号
            return 0
            
        return False

    def _check_exit_condition(self, symbol: str, td, price: float):
        """
        检查止盈止损条件
        """
        if symbol not in self.account["position"]:
            return
            
        position = self.account["position"][symbol]
        tp_price = position["tp"]
        sl_price = position["sl"]
        pos_side = position["posSide"]
        
        # 根据持仓方向确定td值
        td = 1 if pos_side == "long" else 0
        
        # 检查是否触发止盈止损
        if pos_side == "long":
            if price >= tp_price:  # 触发止盈
                self._close_position(symbol, price, "take_profit")
            elif price <= sl_price:  # 触发止损
                self._close_position(symbol, price, "stop_loss")
        else:  # 空仓
            if price <= tp_price:  # 触发止盈
                self._close_position(symbol, price, "take_profit")
            elif price >= sl_price:  # 触发止损
                self._close_position(symbol, price, "stop_loss")

    def symbol_selection(self):
        """
        调用选股方法
        """
        try:
            if not hasattr(self, 'ss_method'):
                return self.default_symbol_selection()
            
            if self.ss_method is None:
                return self.default_symbol_selection()
                
            args = self.funSymbol_selection.get('args', {})
            return self.ss_method(**args)
        except Exception as e:
            print(f"选股异常: {e}")
            return [] 