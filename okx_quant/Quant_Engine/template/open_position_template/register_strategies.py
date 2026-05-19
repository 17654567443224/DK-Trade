"""
策略注册工具脚本
用于将自定义交易策略注册到数据库中
"""

from Quant_Engine.template.open_position_template.template.advancedStrategy import AdvancedStrategy
from Quant_Engine.template.open_position_template.template.machineLearningStrategy import MachineLearningStrategy
from Quant_Engine.template.open_position_template.template.easyStrategy import EasyStrategy 
import inspect
import pymysql
import json
from typing import Dict, Any, List


def register_strategies_to_db(host: str = "localhost", user: str = "root", 
                             password: str = "lxw2866", database: str = "dk-qaunt"):
    """
    将高级策略和机器学习策略注册到数据库中
    
    参数:
        host: 数据库主机地址
        user: 数据库用户名
        password: 数据库密码
        database: 数据库名称
    
    返回:
        bool: 是否注册成功
    """
    try:
        # 连接到数据库
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        
        # 注册高级策略
        advanced_success = register_advanced_strategy(cursor)
        print(f"高级策略注册{'成功' if advanced_success else '失败'}")
        
        # 注册机器学习策略
        ml_success = register_ml_strategy(cursor)
        print(f"机器学习策略注册{'成功' if ml_success else '失败'}")
        
        # 提交事务并关闭连接
        conn.commit()
        cursor.close()
        conn.close()
        
        return advanced_success and ml_success
    
    except Exception as e:
        print(f"注册策略时发生错误: {e}")
        return False


def register_advanced_strategy(cursor) -> bool:
    """注册高级策略到数据库"""
    try:
        # 创建高级策略实例
        strategy = AdvancedStrategy(None)
        
        # 定义中文名称映射
        cn_names_mapping = {
            "turtle_trading": "海龟交易系统",
            "ichimoku_cloud": "一目均衡表策略",
            "elder_triple_screen": "三重滤网交易系统",
            "price_action_strategy": "价格行为策略",
            "mean_reversion": "均值回归策略",
            "pattern_recognition": "图表形态识别策略",
            "adaptive_market_classifier": "自适应市场分类器策略",
            "volume_weighted_macd": "成交量加权MACD策略",
            "vwap_strategy": "VWAP策略"
        }
        
        # 参数描述映射
        param_desc_mapping = {
            "turtle_trading": {
                "entry_period": "入场周期天数，用于计算突破的高低点，默认20天",
                "exit_period": "出场周期天数，用于计算反向突破的高低点，默认10天",
                "atr_period": "ATR计算周期，用于确定市场波动性，默认14天",
                "atr_multiplier": "ATR乘数，用于设置止损位置的倍数，默认2.0"
            },
            "ichimoku_cloud": {
                "tenkan_period": "转换线周期，计算中期支撑阻力，默认9天",
                "kijun_period": "基准线周期，计算长期支撑阻力，默认26天",
                "senkou_span_b_period": "先行带B周期，计算更长期支撑阻力，默认52天",
                "displacement": "位移未来周期，云层向未来平移的周期数，默认26天"
            },
            "elder_triple_screen": {
                "ma_period": "移动平均周期，用于第一重滤网判断趋势，默认50天",
                "macd_fast": "MACD快线周期，用于第二重滤网，默认12天",
                "macd_slow": "MACD慢线周期，用于第二重滤网，默认26天",
                "macd_signal": "MACD信号线周期，用于第二重滤网，默认9天",
                "rsi_period": "RSI计算周期，用于第三重滤网判断超买超卖，默认14天",
                "oversold": "超卖阈值，低于此值视为超卖，默认30",
                "overbought": "超买阈值，高于此值视为超买，默认70"
            },
            "price_action_strategy": {
                "lookback": "回溯K线数量，用于识别价格形态，默认3根K线"
            },
            "mean_reversion": {
                "lookback": "回溯周期，用于计算均值和标准差，默认20天",
                "std_dev": "标准差倍数，用于确定价格偏离程度的阈值，默认2.0倍"
            },
            "pattern_recognition": {
                "lookback": "图形识别窗口大小，用于检测头肩顶等形态的基本单位，默认5天"
            },
            "adaptive_market_classifier": {
                "lookback": "回溯周期，用于计算总体市场特征，默认50天",
                "fast_period": "快速移动平均周期，用于短期趋势判断，默认10天",
                "slow_period": "慢速移动平均周期，用于长期趋势判断，默认30天",
                "vol_period": "波动率计算周期，用于评估市场波动性，默认20天"
            },
            "volume_weighted_macd": {
                "fast": "快线EMA周期，成交量加权MACD的快速线，默认12天",
                "slow": "慢线EMA周期，成交量加权MACD的慢速线，默认26天",
                "signal": "信号线周期，成交量加权MACD的信号平滑线，默认9天",
                "volume_factor": "成交量权重因子，控制成交量对价格的影响程度，默认0.5"
            },
            "vwap_strategy": {
                "lookback": "VWAP计算周期，成交量加权平均价的计算天数，默认20天",
                "deviation": "偏离度阈值，价格偏离VWAP的百分比阈值，默认0.01(1%)"
            }
        }
        
        # 获取策略类的方法
        methods = [method for method in dir(strategy) if callable(getattr(strategy, method)) 
                  and not method.startswith('__') and method in cn_names_mapping]
        
        # 遍历方法并注册到数据库
        for method_name in methods:
            # 获取方法对象
            method = getattr(strategy, method_name)
            
            # 获取方法的参数
            sig = inspect.signature(method)
            params = sig.parameters
            
            # 排除self和am参数
            args = {name: param.default if param.default is not inspect.Parameter.empty else None 
                   for name, param in params.items() if name not in ['self', 'am']}
            
            # 获取方法的文档
            doc = method.__doc__ or ""
            
            # 构建参数描述
            args_description = {}
            for arg_name in args.keys():
                # 尝试从自定义参数描述中提取
                if method_name in param_desc_mapping and arg_name in param_desc_mapping[method_name]:
                    args_description[arg_name] = param_desc_mapping[method_name][arg_name]
                else:
                    args_description[arg_name] = arg_name  # 默认描述就是参数名
            
            # 插入到数据库
            sql = """
            INSERT INTO open_position_template 
            (file_name, class_name, fun_name, class_args, fun_args, class_args_des, fun_args_des, cn_class_name, cn_fun_name, owner) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(sql, (
                "advancedStrategy.py",
                "AdvancedStrategy",
                method_name,
                json.dumps({}),  # 类参数为空
                json.dumps(args),  # 方法参数
                json.dumps({}),  # 类参数描述为空
                json.dumps(args_description),  # 方法参数描述
                "高级策略",
                cn_names_mapping[method_name],
                1
            ))
        
        return True
        
    except Exception as e:
        print(f"注册高级策略时发生错误: {e}")
        return False


def register_ml_strategy(cursor) -> bool:
    """注册机器学习策略到数据库"""
    try:
        # 创建机器学习策略实例
        strategy = MachineLearningStrategy(None)
        
        # 定义中文名称映射
        cn_names_mapping = {
            "linear_regression": "线性回归预测策略",
            "bollinger_regression": "布林带回归策略",
            "kalman_filter": "卡尔曼滤波策略",
            "seasonal_arima": "季节性ARIMA模型策略",
            "support_vector_regression": "支持向量回归策略"
        }
        
        # 参数描述映射
        param_desc_mapping = {
            "linear_regression": {
                "lookback": "历史数据周期，用于训练线性回归模型的天数，默认30天",
                "forecast_period": "预测未来周期数，向前预测的天数，默认5天"
            },
            "bollinger_regression": {
                "lookback": "历史数据周期，用于计算布林带和回归模型的天数，默认20天",
                "std_dev": "布林带标准差倍数，控制布林带宽度的标准差倍数，默认2.0倍",
                "forecast_period": "预测未来周期数，向前预测的天数，默认5天"
            },
            "kalman_filter": {
                "lookback": "历史数据周期，用于卡尔曼滤波器的天数，默认20天",
                "process_var": "过程噪声方差，控制状态转移的不确定性，默认1e-4",
                "measure_var": "测量噪声方差，控制观测值的不确定性，默认1e-2"
            },
            "seasonal_arima": {
                "lookback": "历史数据周期，用于ARIMA模型训练的天数，默认60天",
                "future_bars": "预测未来K线数，向前预测的K线数量，默认5根"
            },
            "support_vector_regression": {
                "lookback": "历史数据周期，用于SVR模型训练的天数，默认40天",
                "forecast_period": "预测未来周期数，向前预测的天数，默认5天",
                "c": "正则化参数，控制SVR模型的复杂度和惩罚系数，默认1.0"
            }
        }
        
        # 获取策略类的方法
        methods = [method for method in dir(strategy) if callable(getattr(strategy, method)) 
                  and not method.startswith('__') and method in cn_names_mapping]
        
        # 遍历方法并注册到数据库
        for method_name in methods:
            # 获取方法对象
            method = getattr(strategy, method_name)
            
            # 获取方法的参数
            sig = inspect.signature(method)
            params = sig.parameters
            
            # 排除self和am参数
            args = {name: param.default if param.default is not inspect.Parameter.empty else None 
                   for name, param in params.items() if name not in ['self', 'am']}
            
            # 获取方法的文档
            doc = method.__doc__ or ""
            
            # 构建参数描述
            args_description = {}
            for arg_name in args.keys():
                # 尝试从自定义参数描述中提取
                if method_name in param_desc_mapping and arg_name in param_desc_mapping[method_name]:
                    args_description[arg_name] = param_desc_mapping[method_name][arg_name]
                else:
                    args_description[arg_name] = arg_name  # 默认描述就是参数名
            
            # 插入到数据库
            sql = """
            INSERT INTO open_position_template 
            (file_name, class_name, fun_name, class_args, fun_args, class_args_des, fun_args_des, cn_class_name, cn_fun_name, owner) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(sql, (
                "machineLearningStrategy.py",
                "MachineLearningStrategy",
                method_name,
                json.dumps({}),  # 类参数为空
                json.dumps(args),  # 方法参数
                json.dumps({}),  # 类参数描述为空
                json.dumps(args_description),  # 方法参数描述
                "机器学习策略",
                cn_names_mapping[method_name],
                1
            ))
        
        return True
        
    except Exception as e:
        print(f"注册机器学习策略时发生错误: {e}")
        return False


if __name__ == "__main__":
    print("开始注册量化交易策略到数据库...")
    success = register_strategies_to_db()
    
    if success:
        print("所有策略注册成功！")
    else:
        print("部分策略注册失败，请检查日志并重试。") 