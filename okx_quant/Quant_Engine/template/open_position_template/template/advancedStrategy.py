"""
高级策略类
提供各种复杂的交易策略算法
"""
import numpy as np
from Quant_Engine.template.open_position_template.target import ArrayManager


class AdvancedStrategy:

    def turtle_trading(self, am: ArrayManager, entry_period: int = 20, exit_period: int = 10, atr_period: int = 14, atr_multiplier: float = 2.0) -> int:
        """海龟交易系统
        入场：价格突破N日高点或低点
        出场：价格突破N/2日低点或高点，或者根据ATR的止损
        """

        if am.count < max(entry_period, exit_period, atr_period):
            return False
        
        # 计算高低点突破
        entry_high = am.high_array[-entry_period-1:-1].max()
        entry_low = am.low_array[-entry_period-1:-1].min()
        exit_high = am.high_array[-exit_period-1:-1].max()
        exit_low = am.low_array[-exit_period-1:-1].min()
        
        # 计算当前价和ATR
        current_price = am.close[-1]
        atr_value = am.atr(atr_period)
        
        # 入场信号
        if current_price > entry_high:
            return 1  # 做多
        elif current_price < entry_low:
            return 0  # 做空
        
        return False

    def ichimoku_cloud(self, am: ArrayManager, tenkan_period: int = 9, kijun_period: int = 26, 
                       senkou_span_b_period: int = 52, displacement: int = 26) -> int:
        """一目均衡表策略
        价格在云层上方，转换线上穿基准线做多
        价格在云层下方，转换线下穿基准线做空
        """
        if am.count < max(tenkan_period, kijun_period, senkou_span_b_period) + displacement:
            return False
        
        # 计算转换线(Tenkan-sen)、基准线(Kijun-sen)
        high_tenkan = am.high_array[-tenkan_period:].max()
        low_tenkan = am.low_array[-tenkan_period:].min()
        tenkan_sen = (high_tenkan + low_tenkan) / 2
        
        high_kijun = am.high_array[-kijun_period:].max()
        low_kijun = am.low_array[-kijun_period:].min()
        kijun_sen = (high_kijun + low_kijun) / 2
        
        # 计算先行带1(Senkou Span A)
        senkou_span_a = (tenkan_sen + kijun_sen) / 2
        
        # 计算先行带2(Senkou Span B)
        high_senkou_b = am.high_array[-senkou_span_b_period:].max()
        low_senkou_b = am.low_array[-senkou_span_b_period:].min()
        senkou_span_b = (high_senkou_b + low_senkou_b) / 2
        
        # 获取26周期前的先行带1和先行带2值
        prev_a = (am.high_array[-tenkan_period-displacement:-displacement].max() + 
                 am.low_array[-tenkan_period-displacement:-displacement].min() + 
                 am.high_array[-kijun_period-displacement:-displacement].max() + 
                 am.low_array[-kijun_period-displacement:-displacement].min()) / 4
        
        prev_b = (am.high_array[-senkou_span_b_period-displacement:-displacement].max() + 
                 am.low_array[-senkou_span_b_period-displacement:-displacement].min()) / 2
        
        current_price = am.close[-1]
        
        # 计算前一天的指标值
        high_tenkan_prev = am.high_array[-tenkan_period-1:-1].max()
        low_tenkan_prev = am.low_array[-tenkan_period-1:-1].min()
        tenkan_sen_prev = (high_tenkan_prev + low_tenkan_prev) / 2
        
        high_kijun_prev = am.high_array[-kijun_period-1:-1].max()
        low_kijun_prev = am.low_array[-kijun_period-1:-1].min()
        kijun_sen_prev = (high_kijun_prev + low_kijun_prev) / 2
        
        # 交易信号
        if current_price > max(prev_a, prev_b) and tenkan_sen_prev < kijun_sen_prev and tenkan_sen > kijun_sen:
            return 1  # 价格在云层上方且转换线上穿基准线，做多
        elif current_price < min(prev_a, prev_b) and tenkan_sen_prev > kijun_sen_prev and tenkan_sen < kijun_sen:
            return 0  # 价格在云层下方且转换线下穿基准线，做空
        
        return False

    def elder_triple_screen(self, am: ArrayManager, ma_period: int = 50, macd_fast: int = 12, 
                          macd_slow: int = 26, macd_signal: int = 9, rsi_period: int = 14,
                          oversold: int = 30, overbought: int = 70) -> int:
        """三重滤网交易系统
        第一重：判断趋势方向（基于长期MA）
        第二重：使用震荡指标寻找回调机会（MACD）
        第三重：使用短期指标寻找入场时机（RSI）
        """
        if am.count < max(ma_period, macd_slow + macd_signal, rsi_period):
            return False
        
        # 第一重滤网：趋势方向
        ma = am.sma(ma_period, array=True)
        trend = 1 if am.close[-1] > ma[-1] else -1
        
        # 第二重滤网：MACD判断回调
        macd, signal, hist = am.macd(macd_fast, macd_slow, macd_signal, array=True)
        macd_signal = 1 if hist[-1] > 0 else -1
        
        # 第三重滤网：RSI判断超买超卖
        rsi = am.rsi(rsi_period, array=True)
        rsi_signal = 0
        if rsi[-1] < oversold:
            rsi_signal = 1  # 超卖
        elif rsi[-1] > overbought:
            rsi_signal = -1  # 超买
        
        # 综合三重滤网结果
        if trend == 1 and macd_signal == 1 and (rsi_signal == 1 or rsi_signal == 0):
            return 1  # 多头趋势，MACD看涨，RSI非超买，做多
        elif trend == -1 and macd_signal == -1 and (rsi_signal == -1 or rsi_signal == 0):
            return 0  # 空头趋势，MACD看跌，RSI非超卖，做空
        
        return False

    def price_action_strategy(self, am: ArrayManager, lookback: int = 3) -> int:
        """价格行为策略
        识别吞没形态、包孕形态、十字星等K线形态
        """
        if am.count < lookback + 1:
            return False
        
        # 获取最近的K线数据
        open_prices = am.open_array[-lookback:]
        close_prices = am.close_array[-lookback:]
        high_prices = am.high_array[-lookback:]
        low_prices = am.low_array[-lookback:]
        
        # 计算K线实体大小和上下影线
        body = abs(close_prices[-1] - open_prices[-1])
        upper_shadow = high_prices[-1] - max(open_prices[-1], close_prices[-1])
        lower_shadow = min(open_prices[-1], close_prices[-1]) - low_prices[-1]
        
        # 检查是否是十字星（实体小，上下影线长）
        is_doji = body < (high_prices[-1] - low_prices[-1]) * 0.1
        
        # 检查吞没形态（当前K线的实体完全覆盖前一个K线的实体）
        bullish_engulfing = (open_prices[-1] < close_prices[-2] and 
                           close_prices[-1] > open_prices[-2] and
                           close_prices[-1] > open_prices[-1])
        
        bearish_engulfing = (open_prices[-1] > close_prices[-2] and 
                           close_prices[-1] < open_prices[-2] and
                           close_prices[-1] < open_prices[-1])
        
        # 检查锤子线和上吊线
        hammer = (lower_shadow > body * 2 and upper_shadow < body * 0.5 and
                body > 0 and close_prices[-1] > open_prices[-1])
        
        hanging_man = (lower_shadow > body * 2 and upper_shadow < body * 0.5 and
                     body > 0 and close_prices[-1] < open_prices[-1])
        
        # 产生交易信号
        if bullish_engulfing or hammer:
            return 1  # 看涨信号
        elif bearish_engulfing or hanging_man:
            return 0  # 看跌信号
        
        return False

    def mean_reversion(self, am: ArrayManager, lookback: int = 20, std_dev: float = 2.0) -> int:
        """均值回归策略
        价格偏离均值超过标准差倍数时反向交易
        """
        if am.count < lookback:
            return False
        
        # 计算移动平均和标准差
        prices = am.close_array[-lookback:]
        mean = np.mean(prices)
        std = np.std(prices)
        
        current_price = am.close[-1]
        
        # 计算z-score（价格偏离均值的标准差倍数）
        z_score = (current_price - mean) / std
        
        # 生成交易信号
        if z_score > std_dev:
            return 0  # 价格过高，回归预期，做空
        elif z_score < -std_dev:
            return 1  # 价格过低，回归预期，做多
        
        return False

    def pattern_recognition(self, am: ArrayManager, lookback: int = 5) -> int:
        """图表形态识别策略
        识别头肩顶、三重顶底、三角形等形态
        """
        if am.count < lookback * 3:
            return False
        
        # 获取价格数据
        highs = am.high_array[-lookback*3:]
        lows = am.low_array[-lookback*3:]
        
        # 简化的头肩顶形态识别
        if len(highs) >= 5:
            # 检测左肩、头部和右肩的高点
            potential_patterns = []
            
            for i in range(len(highs) - 4):
                # 左肩-头部-右肩的高点
                left_shoulder = highs[i]
                head = highs[i+2]
                right_shoulder = highs[i+4]
                
                # 确认颈线位置
                neck_line = min(lows[i+1], lows[i+3])
                
                # 头肩顶形态: 左肩和右肩高点接近，头部高点高于肩部
                if (abs(left_shoulder - right_shoulder) / left_shoulder < 0.05 and
                    head > left_shoulder * 1.02 and head > right_shoulder * 1.02):
                    potential_patterns.append(("HEAD_AND_SHOULDERS", neck_line))
        
            # 如果检测到头肩顶形态且当前价格突破颈线
            if potential_patterns and am.close[-1] < potential_patterns[0][1]:
                return 0  # 看跌信号
                
        # 简化的双顶形态识别
        if len(highs) >= 3:
            for i in range(len(highs) - 2):
                first_top = highs[i]
                second_top = highs[i+2]
                middle_trough = lows[i+1]
                
                # 双顶形态：两个高点接近，中间有明显低点
                if (abs(first_top - second_top) / first_top < 0.03 and
                    first_top > middle_trough * 1.02 and 
                    second_top > middle_trough * 1.02):
                    if am.close[-1] < middle_trough:
                        return 0  # 看跌信号
        
        # 简化的双底形态
        if len(lows) >= 3:
            for i in range(len(lows) - 2):
                first_bottom = lows[i]
                second_bottom = lows[i+2]
                middle_peak = highs[i+1]
                
                # 双底形态：两个低点接近，中间有明显高点
                if (abs(first_bottom - second_bottom) / first_bottom < 0.03 and
                    middle_peak > first_bottom * 1.02 and 
                    middle_peak > second_bottom * 1.02):
                    if am.close[-1] > middle_peak:
                        return 1  # 看涨信号
                    
        return False

    def adaptive_market_classifier(self, am: ArrayManager, lookback: int = 50, 
                                 fast_period: int = 10, slow_period: int = 30,
                                 vol_period: int = 20) -> int:
        """自适应市场分类器策略
        根据市场状态（趋势/震荡）选择不同交易策略
        """
        if am.count < max(lookback, slow_period, vol_period):
            return False
        
        # 计算价格波动率
        returns = np.diff(am.close_array[-lookback-1:]) / am.close_array[-lookback-1:-1]
        volatility = np.std(returns) * np.sqrt(252)  # 年化波动率
        
        # 计算短期和长期移动平均
        fast_ma = am.sma(fast_period, array=True)
        slow_ma = am.sma(slow_period, array=True)
        
        # 计算ADX指标评估趋势强度
        adx = am.adx(14, array=True)
        
        # 判断市场状态
        is_trending = adx[-1] > 25  # ADX > 25表示存在强趋势
        
        if is_trending:
            # 趋势市场：使用均线交叉策略
            if fast_ma[-2] < slow_ma[-2] and fast_ma[-1] > slow_ma[-1]:
                return 1  # 做多信号
            elif fast_ma[-2] > slow_ma[-2] and fast_ma[-1] < slow_ma[-1]:
                return 0  # 做空信号
        else:
            # 震荡市场：使用布林带反转策略
            upper, lower = am.boll(20, 2.0, array=True)
            
            if am.close[-1] > upper[-1]:
                return 0  # 接近上轨，做空信号
            elif am.close[-1] < lower[-1]:
                return 1  # 接近下轨，做多信号
        
        return False

    def volume_weighted_macd(self, am: ArrayManager, fast: int = 12, slow: int = 26, 
                          signal: int = 9, volume_factor: float = 0.5) -> int:
        """成交量加权MACD策略
        传统MACD基础上增加成交量权重因子
        """
        if am.count < slow + signal:
            return False
        
        # 获取价格和成交量数据
        closes = am.close_array[-slow-signal:]
        volumes = am.volume_array[-slow-signal:]
        
        # 计算成交量加权价格
        vw_price = closes * (1 + volume_factor * (volumes / volumes.mean() - 1))
        
        # 计算EMA
        ema_fast = np.zeros_like(vw_price)
        ema_slow = np.zeros_like(vw_price)
        
        # 计算初始EMA值
        ema_fast[0] = vw_price[0]
        ema_slow[0] = vw_price[0]
        
        # 计算EMA序列
        for i in range(1, len(vw_price)):
            ema_fast[i] = (vw_price[i] * (2 / (fast + 1)) + 
                          ema_fast[i-1] * (1 - 2 / (fast + 1)))
            ema_slow[i] = (vw_price[i] * (2 / (slow + 1)) + 
                          ema_slow[i-1] * (1 - 2 / (slow + 1)))
        
        # 计算MACD线
        macd_line = ema_fast - ema_slow
        
        # 计算信号线
        signal_line = np.zeros_like(macd_line)
        signal_line[0] = macd_line[0]
        
        for i in range(1, len(macd_line)):
            signal_line[i] = (macd_line[i] * (2 / (signal + 1)) + 
                             signal_line[i-1] * (1 - 2 / (signal + 1)))
        
        # 计算柱状图
        histogram = macd_line - signal_line
        
        # 生成交易信号
        if macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]:
            return 1  # MACD金叉，做多
        elif macd_line[-2] > signal_line[-2] and macd_line[-1] < signal_line[-1]:
            return 0  # MACD死叉，做空
        
        return False

    def vwap_strategy(self, am: ArrayManager, lookback: int = 20, deviation: float = 0.01) -> int:
        """VWAP策略
        价格与成交量加权平均价的偏离度作为交易信号
        """
        if am.count < lookback:
            return False
        
        # 获取高开低收和成交量数据
        highs = am.high_array[-lookback:]
        lows = am.low_array[-lookback:]
        closes = am.close_array[-lookback:]
        volumes = am.volume_array[-lookback:]
        
        # 计算典型价格
        typical_prices = (highs + lows + closes) / 3
        
        # 计算VWAP
        vwap = np.sum(typical_prices * volumes) / np.sum(volumes)
        
        # 计算当前价格与VWAP的偏离度
        current_price = am.close[-1]
        deviation_pct = (current_price - vwap) / vwap
        
        # 生成交易信号
        if deviation_pct > deviation:
            return 0  # 价格高于VWAP一定比例，做空
        elif deviation_pct < -deviation:
            return 1  # 价格低于VWAP一定比例，做多
        
        return False 