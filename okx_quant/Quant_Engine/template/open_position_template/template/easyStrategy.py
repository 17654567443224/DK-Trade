from Quant_Engine.template.open_position_template.target import ArrayManager


class EasyStrategy:

    def dual_moving_average_crossover(self, am: ArrayManager, short_period: int = 10, long_period: int = 30) -> int:
        """当短期均线上穿长期均线时做多，下穿时做空
            双均线交叉策略
        """
        if am.count < long_period:
            return False  # 数据不足

        short_ma = am.sma(short_period, array=True)
        long_ma = am.sma(long_period, array=True)

        if short_ma[-2] < long_ma[-2] and short_ma[-1] > long_ma[-1]:
            return 1  # 金叉，做多
        elif short_ma[-2] > long_ma[-2] and short_ma[-1] < long_ma[-1]:
            return 0  # 死叉，做空
        return False

    def rsi_overbought_oversold(self, am: ArrayManager, rsi_period: int = 14, overbought: int = 70,
                                oversold: int = 30) -> int:
        """RSI > 70做空，RSI < 30做多
        RSI超买超卖策略
        """
        if am.count < rsi_period:
            return False

        rsi = am.rsi(rsi_period, array=True)
        current_rsi = rsi[-1]

        if current_rsi >= overbought:
            return 0
        elif current_rsi <= oversold:
            return 1
        return False

    def macd_crossover(self, am: ArrayManager, fast: int = 12, slow: int = 26, signal: int = 9) -> int:
        """MACD线上穿信号线做多，下穿做空
            MACD金叉死叉策略
        """
        if am.count < slow + signal:
            return False

        macd_line, signal_line, _ = am.macd(fast, slow, signal, array=True)

        if macd_line[-2] < signal_line[-2] and macd_line[-1] > signal_line[-1]:
            return 1
        elif macd_line[-2] > signal_line[-2] and macd_line[-1] < signal_line[-1]:
            return 0
        return False

    def bollinger_breakout(self, am: ArrayManager, period: int = 20, dev: float = 2.0) -> int:
        """价格突破上轨做多，跌破下轨做空
        布林带突破策略
        """
        if am.count < period:
            return False

        upper, lower = am.boll(period, dev, array=True)
        close = am.close_array

        if close[-1] > upper[-1]:
            return 1
        elif close[-1] < lower[-1]:
            return 0
        return False

    def momentum_breakout(self, am: ArrayManager, lookback: int = 20) -> int:
        """价格创N日新高做多，新低做空
            动量突破策略
        """
        if am.count < lookback:
            return False

        highs = am.high_array[-lookback:]
        lows = am.low_array[-lookback:]

        if am.close[-1] > highs.max():
            return 1
        elif am.close[-1] < lows.min():
            return 0
        return False

    def atr_volatility(self, am: ArrayManager, period: int = 14, threshold: float = 0.03) -> int:
        """波动率突然放大时顺势交易
            ATR波动性策略
        """
        if am.count < period + 1:
            return False

        atr = am.atr(period, array=True)
        current_atr = atr[-1]
        prev_atr = atr[-2]

        if current_atr > prev_atr * (1 + threshold) and am.close[-1] > am.open[-1]:
            return 1  # 波动放大且阳线，做多
        elif current_atr > prev_atr * (1 + threshold) and am.close[-1] < am.open[-1]:
            return 0  # 波动放大且阴线，做空
        return False

    def kdj_crossover(self, am: ArrayManager, fastk: int = 9, slowk: int = 3, slowd: int = 3) -> int:
        """K线上穿D线做多，下穿做空
        KDJ超买超卖策略
        """
        if am.count < fastk + slowd:
            return False

        k, d = am.stoch(fastk_period=fastk, slowk_period=slowk, slowk_matype=0,
                        slowd_period=slowd, slowd_matype=0, array=True)

        if k[-2] < d[-2] and k[-1] > d[-1]:
            return 1
        elif k[-2] > d[-2] and k[-1] < d[-1]:
            return 0
        return False

    def sar_reversal(self, am: ArrayManager, acceleration: float = 0.02, maximum: float = 0.2) -> int:
        """价格突破SAR点反转仓位
            SAR抛物线转向策略
        """
        sar = am.sar(acceleration, maximum, array=True)

        if am.close[-1] > sar[-1]:
            return 1  # 价格在SAR上方，做多
        elif am.close[-1] < sar[-1]:
            return 0  # 价格在SAR下方，做空
        return False

    def dmi_trend(self, am: ArrayManager, period: int = 14) -> int:
        """+DI上穿-DI且ADX上升时做多，反之做空
        DMI趋势跟踪策略
        """
        if am.count < period:
            return False

        adx = am.adx(period, array=True)
        plus_di = am.plus_di(period, array=True)
        minus_di = am.minus_di(period, array=True)

        if plus_di[-1] > minus_di[-1] and adx[-1] > adx[-2]:
            return 1
        elif plus_di[-1] < minus_di[-1] and adx[-1] > adx[-2]:
            return 0
        return False

    def volume_price_divergence(self,am: ArrayManager, period: int = 5) -> int:
        """价格新高但成交量下降时做空，新低但成交量上升做多
        量价背离策略
        """
        if am.count < period:
            return False

        closes = am.close_array[-period:]
        volumes = am.volume_array[-period:]

        # 检查价格新高但成交量下降
        if closes[-1] == closes.max() and volumes[-1] < volumes[:-1].mean():
            return 0
        # 检查价格新低但成交量上升
        elif closes[-1] == closes.min() and volumes[-1] > volumes[:-1].mean():
            return 1
        return False

