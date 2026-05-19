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


class BollingerStrategy(Base_Template):
    """
    布林带交易策略
    
    策略说明：
    - 当价格突破上轨后回落时，产生做空信号
    - 当价格突破下轨后反弹时，产生做多信号
    - 使用布林带宽度来判断市场波动性
    
    参数说明：
    - sz: ArrayManager的数据窗口大小
    - interval: K线周期
    - account: 账户信息
    - ws: WebSocket连接
    - window: 布林带计算周期
    - dev_multiplier: 标准差倍数
    - symbol_selection: 外部选股策略
    - profit_loss: 外部止盈止损策略
    - fund: 外部资金管理策略
    """
    
    def __init__(
            self,
            id,
            lever,
            account: dict,
            ws: WebSocketProducer,
            sz=100,
            interval=Interval.CANDLE_15m.value,
            window: int = 20,
            dev_multiplier: float = 2.0,
            max_positions=None,
            symbol_selection=None,
            profit_loss=None,
            fund=None,
            funSymbol_selection=None,
            funOpen_position=None,
            funProfit_loss=None,
            funFund=None
    ):
        if max_positions is not None:
            super().__init__(id, lever, account, ws, sz, interval, max_positions, funSymbol_selection, funOpen_position, funProfit_loss, funFund)
        else:
            super().__init__(id, lever, account, ws, sz, interval, funSymbol_selection, funOpen_position, funProfit_loss, funFund)
        # 策略参数
        self.window = window
        self.dev_multiplier = dev_multiplier
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
        默认止盈止损策略：基于布林带的动态止盈止损
        """
        try:
            # 获取当前布林带值
            mid = self.bars[symbol].sma(self.window, array=True)
            up, down = self.bars[symbol].boll(self.window, self.dev_multiplier, array=True)
            band_width = up[-1] - down[-1]
            
            if td == 1:  # 做多
                tp_price = price + band_width * 0.5  # 上移半个带宽
                sl_price = max(price - band_width * 0.3, down[-1])  # 下移0.3个带宽，但不低于下轨
            else:  # 做空
                tp_price = price - band_width * 0.5  # 下移半个带宽
                sl_price = min(price + band_width * 0.3, up[-1])  # 上移0.3个带宽，但不高于上轨
                
            return tp_price, sl_price
        except Exception as e:
            print(f"止盈止损计算异常: {e}")
            return price * 1.02, price * 0.98

    def default_fund(self, td: int, symbol: str, price: float, lever: float = None) -> Tuple[float, float]:
        """
        默认资金管理策略：基于布林带位置的动态仓位，考虑杠杆因素
        """
        try:
            # 获取当前布林带值
            mid = self.bars[symbol].sma(self.window, array=True)
            up, low = self.bars[symbol].boll(self.window, self.dev_multiplier, array=True)
            
            # 使用传入的杠杆或默认杠杆
            leverage = Decimal(str(lever)) if lever is not None else Decimal(str(self.lever))
            
            # 计算价格在布林带中的位置（0-1之间）
            if td == 1:  # 做多
                position_ratio = (Decimal(str(price)) - Decimal(str(low[-1]))) / (Decimal(str(up[-1])) - Decimal(str(low[-1])))
                strength = Decimal('1') - position_ratio  # 价格越接近下轨，仓位越大
            else:  # 做空
                position_ratio = (Decimal(str(price)) - Decimal(str(low[-1]))) / (Decimal(str(up[-1])) - Decimal(str(low[-1])))
                strength = position_ratio  # 价格越接近上轨，仓位越大
            
            # 计算基础仓位大小（最大使用账户余额的15%）
            base_position = self.account["balance"] * Decimal('0.15') * strength
            
            # 考虑杠杆因素计算实际可开的仓位数量
            position_size = base_position * leverage
            volume = position_size / Decimal(str(price))
            
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
        布林带开仓策略：基于价格突破布林带上下轨后的回调
        """
        if not am.inited:
            return False
        
        # 计算布林带指标
        mid = am.sma(self.window, array=True)
        up, down = am.boll(self.window, self.dev_multiplier, array=True)
        
        # 获取最近两根K线的收盘价
        close_array = am.close_array
        current_close = close_array[-1]
        prev_close = close_array[-2]
            
        # 生成交易信号
        if prev_close >= up[-2] and current_close < up[-1]:
            # 价格从上轨回落，做空信号
            return 0
        elif prev_close <= down[-2] and current_close > down[-1]:
            # 价格从下轨反弹，做多信号
            return 1
            
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