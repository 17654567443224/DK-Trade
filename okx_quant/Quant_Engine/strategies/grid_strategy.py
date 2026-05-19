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


class GridStrategy(Base_Template):
    """
    网格交易策略
    
    策略说明：
    - 在价格区间内等距设置网格
    - 价格下跌到网格线时买入
    - 价格上涨到网格线时卖出
    - 可以同时持有多个网格仓位
    
    参数说明：
    - sz: ArrayManager的数据窗口大小
    - interval: K线周期
    - account: 账户信息
    - ws: WebSocket连接
    - grid_upper_price: 网格上限价格
    - grid_lower_price: 网格下限价格
    - grid_number: 网格数量
    - symbol_selection: 外部选股策略
    - profit_loss: 外部止盈止损策略
    - fund: 外部资金管理策略
    """
    
    def __init__(
            self,
            id,
            account: dict,
            grid_upper_price: float,
            grid_lower_price: float,
            ws: WebSocketProducer,
            grid_number: int = 10,
            sz=100,
            interval=Interval.CANDLE_15m.value,
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
        self.grid_upper_price = grid_upper_price
        self.grid_lower_price = grid_lower_price
        self.grid_number = grid_number
        
        # 计算网格间距
        self.grid_interval = (grid_upper_price - grid_lower_price) / grid_number
        
        # 初始化网格价格列表
        self.grid_prices = [
            grid_lower_price + i * self.grid_interval 
            for i in range(grid_number + 1)
        ]
        
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
            
        # 记录每个网格的状态
        self.grid_positions = {}  # 格式：{grid_index: position_info}

    def default_symbol_selection(self) -> List[str]:
        """
        默认选股策略：按24小时成交量选择交易对
        """
        try:
            symbols = self.symbol_selector.filter_symbolByVolCcy24h(trade=100000000, mode="value")  # 1亿交易额
            if symbols:
                return symbols

        except Exception as e:
            print(f"选股异常: {e}")
            return []

    def default_profit_loss(self, symbol: str, td: int, price: float) -> Tuple[float, float]:
        """
        默认止盈止损策略：基于网格间距的动态止盈止损
        """
        try:
            # 对于网格策略，止盈价格为上一个网格线，止损价格为下一个网格线
            current_grid = self._find_current_grid(price)
            
            if td == 1:  # 做多
                tp_price = self.grid_prices[current_grid + 1]
                sl_price = price * 0.95  # 设置一个保护性止损
            else:  # 做空
                tp_price = self.grid_prices[current_grid - 1]
                sl_price = price * 1.05  # 设置一个保护性止损
                
            return tp_price, sl_price
        except Exception as e:
            print(f"止盈止损计算异常: {e}")
            return price * 1.02, price * 0.98

    def default_fund(self, td: int, symbol: str, price: float, lever: float = None) -> Tuple[float, float]:
        """
        默认资金管理策略：将总资金平均分配到每个网格，考虑杠杆因素
        """
        try:
            # 使用传入的杠杆或默认杠杆
            leverage = Decimal(str(lever)) if lever is not None else Decimal(str(self.lever))
            
            # 计算每个网格可用资金
            total_available = self.account["balance"]
            per_grid_amount = total_available / Decimal(str(self.grid_number))
            
            # 考虑杠杆因素计算实际可开的仓位数量
            leveraged_amount = per_grid_amount * leverage
            volume = leveraged_amount / Decimal(str(price))
            
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

    def _find_current_grid(self, price: float) -> int:
        """
        找到当前价格所在的网格索引
        """
        for i in range(len(self.grid_prices) - 1):
            if self.grid_prices[i] <= price < self.grid_prices[i + 1]:
                return i
        return -1

    def op_method(self, am: ArrayManager):
        """
        网格交易开仓策略：基于价格在不同网格区间的位置做出交易决策
        """
        if not am.inited:
            return False
            
        current_price = am.close_array[-1]
        current_grid = self._find_current_grid(current_price)
        
        if current_grid == -1:
            return False
            
        # 检查是否已经在当前网格有仓位
        if current_grid in self.grid_positions:
            return False
            
        # 判断价格相对于上一次成交价的位置
        for symbol, position in self.account["position"].items():
            last_trade_price = position["entry_price"]
            if current_price > last_trade_price:
                # 价格上涨，在网格线卖出
                if abs(current_price - self.grid_prices[current_grid + 1]) < self.grid_interval * 0.1:
                    return 0  # 做空信号
            else:
                # 价格下跌，在网格线买入
                if abs(current_price - self.grid_prices[current_grid]) < self.grid_interval * 0.1:
                    return 1  # 做多信号
            return False
        
        # 首次进入交易，根据价格位置决定买入或卖出
        if current_price < (self.grid_lower_price + self.grid_upper_price) / 2:
            return 1  # 价格在中间价格以下，做多
        else:
            return 0  # 价格在中间价格以上，做空

    def _check_exit_condition(self, symbol: str, td, price: float):
        """
        重写父类的止盈止损检查方法，适应网格交易特点
        """
        position = self.account["position"][symbol]
        current_grid = self._find_current_grid(price)
        
        if current_grid == -1:
            return
            
        if position["posSide"] == "long":
            # 多仓在上一个网格线止盈
            if price >= self.grid_prices[current_grid + 1]:
                self._close_position(symbol, price, "take_profit")
            # 保护性止损
            elif price <= position["sl"]:
                self._close_position(symbol, price, "stop_loss")
        else:
            # 空仓在下一个网格线止盈
            if price <= self.grid_prices[current_grid - 1]:
                self._close_position(symbol, price, "take_profit")
            # 保护性止损
            elif price >= position["sl"]:
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