from Quant_Engine.template.open_position_template.target import ArrayManager
import numpy as np


class MachineLearningStrategy:

    def linear_regression(self, am: ArrayManager, lookback: int = 30, forecast_period: int = 5) -> int:
        """线性回归预测策略
        通过历史价格的线性回归预测未来价格走势
        """
        if am.count < lookback:
            return False
        
        # 获取收盘价历史数据
        prices = am.close_array[-lookback:]
        
        # 构建X和Y数据
        X = np.arange(lookback).reshape(-1, 1)
        y = prices
        
        # 计算线性回归参数 (y = a*x + b)
        a = np.cov(X.flatten(), y)[0, 1] / np.var(X.flatten())
        b = np.mean(y) - a * np.mean(X.flatten())
        
        # 预测未来价格
        future_price = a * (lookback + forecast_period) + b
        current_price = am.close[-1]
        
        # 生成交易信号
        if future_price > current_price * 1.01:  # 预测价格上涨超过1%
            return 1
        elif future_price < current_price * 0.99:  # 预测价格下跌超过1%
            return 0
        
        return False

    def bollinger_regression(self, am: ArrayManager, lookback: int = 20, std_dev: float = 2.0, 
                           forecast_period: int = 5) -> int:
        """布林带回归策略
        结合布林带和线性回归的混合策略
        """
        if am.count < lookback:
            return False
        
        # 计算布林带
        upper, lower = am.boll(lookback, std_dev, array=True)
        
        # 获取价格数据
        prices = am.close_array[-lookback:]
        current_price = am.close[-1]
        
        # 当前布林带位置
        upper_band = upper[-1]
        lower_band = lower[-1]
        middle_band = (upper_band + lower_band) / 2
        
        # 计算价格在布林带中的相对位置 (0-1之间，0表示在下轨，1表示在上轨)
        band_position = (current_price - lower_band) / (upper_band - lower_band) if upper_band != lower_band else 0.5
        
        # 线性回归预测
        X = np.arange(lookback).reshape(-1, 1)
        y = prices
        
        # 计算线性回归参数
        a = np.cov(X.flatten(), y)[0, 1] / np.var(X.flatten())
        b = np.mean(y) - a * np.mean(X.flatten())
        
        # 预测未来价格
        future_price = a * (lookback + forecast_period) + b
        
        # 生成交易信号
        # 价格接近下轨且预测上涨，做多
        if band_position < 0.2 and future_price > current_price:
            return 1
        # 价格接近上轨且预测下跌，做空
        elif band_position > 0.8 and future_price < current_price:
            return 0
        
        return False

    def kalman_filter(self, am: ArrayManager, lookback: int = 20, process_var: float = 1e-4,
                     measure_var: float = 1e-2) -> int:
        """卡尔曼滤波策略
        使用卡尔曼滤波预测价格走势并生成交易信号
        """
        if am.count < lookback:
            return False
        
        # 获取价格数据
        prices = am.close_array[-lookback:]
        
        # 初始化卡尔曼滤波器状态
        x_hat = prices[0]  # 状态估计值
        p = 1.0  # 估计误差协方差
        
        # 定义卡尔曼滤波参数
        q = process_var  # 过程噪声方差
        r = measure_var  # 测量噪声方差
        
        # 存储滤波后的估计值
        filtered_values = np.zeros(lookback)
        filtered_values[0] = x_hat
        
        # 应用卡尔曼滤波
        for t in range(1, lookback):
            # 预测步骤
            x_hat_minus = x_hat
            p_minus = p + q
            
            # 更新步骤
            k = p_minus / (p_minus + r)  # 卡尔曼增益
            x_hat = x_hat_minus + k * (prices[t] - x_hat_minus)
            p = (1 - k) * p_minus
            
            filtered_values[t] = x_hat
        
        # 计算滤波后的趋势
        trend = filtered_values[-1] - filtered_values[-2]
        
        # 生成交易信号
        if trend > 0 and prices[-1] < filtered_values[-1]:
            return 1  # 滤波趋势向上且价格低于滤波值，做多
        elif trend < 0 and prices[-1] > filtered_values[-1]:
            return 0  # 滤波趋势向下且价格高于滤波值，做空
        
        return False

    def seasonal_arima(self, am: ArrayManager, lookback: int = 60, future_bars: int = 5) -> int:
        """季节性ARIMA模型策略
        使用简化的季节性ARIMA模型预测价格走势
        """
        if am.count < lookback:
            return False
        
        # 获取价格数据
        prices = am.close_array[-lookback:]
        
        # 计算简单的差分
        diff = np.diff(prices)
        
        # 使用简化的AR(1)模型
        ar_param = np.corrcoef(diff[:-1], diff[1:])[0, 1]
        
        # 最后一个差分值
        last_diff = diff[-1]
        
        # 简单预测未来价格变动
        predicted_diff = ar_param * last_diff
        
        # 预测未来几个bar的累积变动
        cumulative_change = 0
        temp_diff = last_diff
        for _ in range(future_bars):
            temp_diff = ar_param * temp_diff
            cumulative_change += temp_diff
        
        # 预测价格
        predicted_price = prices[-1] + cumulative_change
        
        # 生成交易信号
        if predicted_price > prices[-1] * 1.01:
            return 1  # 预测价格上涨超过1%，做多
        elif predicted_price < prices[-1] * 0.99:
            return 0  # 预测价格下跌超过1%，做空
        
        return False

    def support_vector_regression(self, am: ArrayManager, lookback: int = 40, 
                              forecast_period: int = 5, c: float = 1.0) -> int:
        """支持向量回归策略
        使用简化的SVR计算方式预测价格趋势
        """
        if am.count < lookback:
            return False
        
        # 获取价格数据
        prices = am.close_array[-lookback:]
        
        # 归一化价格
        min_price = np.min(prices)
        max_price = np.max(prices)
        norm_prices = (prices - min_price) / (max_price - min_price) if max_price > min_price else prices
        
        # 创建特征矩阵（以最近5个值作为特征）
        X = np.zeros((lookback - 5, 5))
        for i in range(lookback - 5):
            X[i] = norm_prices[i:i+5]
        
        y = norm_prices[5:]
        
        # 简化的线性核SVR计算（实际使用时应使用scikit-learn的SVR）
        # 这里使用简单线性回归代替
        X_mean = np.mean(X, axis=0)
        y_mean = np.mean(y)
        
        # 计算回归系数
        numerator = np.sum((X - X_mean) * (y.reshape(-1, 1) - y_mean), axis=0)
        denominator = np.sum((X - X_mean)**2, axis=0)
        coefficients = numerator / (denominator + 1e-8)  # 避免除零
        
        # 预测当前样本之后的值
        last_features = norm_prices[-5:]
        prediction = np.sum(coefficients * last_features)
        
        # 反归一化
        prediction = prediction * (max_price - min_price) + min_price
        current_price = am.close[-1]
        
        # 生成交易信号
        if prediction > current_price * 1.01:
            return 1  # 预测上涨超过1%，做多
        elif prediction < current_price * 0.99:
            return 0  # 预测下跌超过1%，做空
        
        return False 