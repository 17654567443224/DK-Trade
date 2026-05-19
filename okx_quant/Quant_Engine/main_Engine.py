import importlib.util
import sys
import threading
import okx.Market_api as Market
from Quant_Engine.WebSocketManager import WebSocketProducer
from functionns import setting
from Quant_Engine.Common.constants import Interval
from Quant_Engine.Common.object import Strategy_Message, Base_Message

from Quant_Engine.logEngine import logEngine
from Quant_Engine.simulation_Engine import SimulationEngine
from flask import Flask, jsonify, request
app = Flask(__name__)

class Main_Engine:
    def __init__(self, symbols_ls: list, kline_mode):
        self.symbols_ls = symbols_ls
        self.kline_mode = kline_mode
        self.init_interval = Interval.CANDLE_15m.value
        self.pb_isRunning = False
        self.pv_isRunning = False
        self.ws: WebSocketProducer = None
        self.ws_pv: WebSocketProducer = None
        self.user_strategies = {}
        self.log = logEngine("Main_Engine_error")
        self.logger = self.log.create_logger()

    def get_symbol(self):
        marketAPI = Market.MarketAPI(True)
        sym = marketAPI.get_tickers(instType='SWAP')
        if len(sym) > 0 and isinstance(sym, dict):
            datas = sym.get('data', [])
            return datas

    def init_engine(self, data):
        symbol_dict = self.get_symbol()
        if not symbol_dict:
            print("初始化失败")
            return "交易对初始化失败"
        self.symbols_ls = [k["instId"] for k in symbol_dict]
        self.subscribe_pb(url=setting.mark_klprice, url_ticker=setting.public_url)
        print("初始化成功")
        return "初始化成功"

    def subscribe_pb(self, url, url_ticker, symbols=None, interval: Interval = None):
        if not self.pb_isRunning:
            sub_param = self.build_sub_param(self.init_interval, self.symbols_ls)
            ws = WebSocketProducer("public", url, url_ticker,sub_param)
            ws.start()
            self.ws = ws
            self.pb_isRunning = True
        else:
            if symbols and interval:
                set_A = set(self.symbols_ls)
                set_B = set(symbols)
                symbols = set_A - set_B
                sub_param = self.build_sub_param(interval, symbols)
                self.ws.sub_param.append(sub_param)

    def load_class_from_file(self, file_path, class_name):
        """
        根据文件路径动态加载模块，并返回指定的类。
        :param file_path: 文件路径
        :param class_name: 类名
        :return: 类对象
        """
        # 提取模块名（去掉路径和扩展名）
        module_name = file_path.split("/")[-2].split(".")[0]

        # 加载模块
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None:
            self.logger.error(f"Could not load module from {file_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # 获取类
        if hasattr(module, class_name):
            return getattr(module, class_name)
        else:
            self.logger.error(f"Class '{class_name}' not found in module '{module_name}'")

    def add_strategy(self, data):
        """
        添加策略
        data:
        {
        ...
        action:
        userId:
        owner:
        account:java需校验金额
        max_position:
        args:{
            pv: 匹配路径信息{path:匹配路径信息, class:类信息, args:参数}
            symbol_selection:{path:匹配路径信息, class:类信息，args:参数}
            open_position:{path:匹配路径信息, class:类信息， args:参数}
            profit_loss:{path:匹配路径信息, class:类信息， args:参数}
            fund:{path:匹配路径信息, class:类信息， args:参数}
        fun_dict: {
                symbol_selection: 方法名
            }

        }

        """
        try:
            if self.pb_isRunning:
                data = Strategy_Message(data)
                lever = int(data.lever)
                if data.pv:  # 定制策略
                    symbol_selection = self.load_class_from_file(
                        "template/symbols_selection/" + data.symbol_selection['fileName'] + ".py",
                        data.symbol_selection['className'])
                    profit_loss = self.load_class_from_file(
                        "template/profit_loss_template/" + data.profit_loss['fileName'] + ".py",
                        data.profit_loss['className'])
                    fund = self.load_class_from_file("template/fund_template/" + data.fund['fileName'] + ".py",
                                                     data.fund['className'])
                    ss_obj = symbol_selection(**data.symbol_selection['args'])
                    pl_obj = profit_loss(lever=lever, **data.profit_loss['args'])
                    fd_obj = fund(account=data.account, lever=lever, **data.fund['args'])
                    cz = self.load_class_from_file(file_path="strategies/" + data.pv['fileName'] + ".py", class_name=data.pv['className'])
                    obj = cz(id=data.userId, ws=self.ws, account=data.account, lever=lever, max_positions=data.max_position, symbol_selection=ss_obj, profit_loss=pl_obj, fund=fd_obj,
                             funSymbol_selection=data.funSymbol_selection, funProfit_loss=data.funProfit_loss, funFund=data.funFund, **data.pv['args'])
                    self.user_strategies[data.userId] = obj
                    return True
                else:
                    symbol_selection = self.load_class_from_file("template/symbols_selection/" + data.symbol_selection['fileName'] + ".py", data.symbol_selection['className'])
                    open_position = self.load_class_from_file("template/open_position_template/template/" + data.open_position['fileName'] + ".py", data.open_position['className'])
                    profit_loss = self.load_class_from_file("template/profit_loss_template/" + data.profit_loss['fileName'] + ".py", data.profit_loss['className'])
                    fund = self.load_class_from_file("template/fund_template/" + data.fund['fileName'] + ".py", data.fund['className'])

                    ss_obj = symbol_selection(**data.symbol_selection['args'])
                    op_obj = open_position(**data.open_position['args'])
                    pl_obj = profit_loss(lever=lever, **data.profit_loss['args'])
                    fd_obj = fund(data.account, lever, **data.fund['args'])
                    simEng = SimulationEngine(id=data.userId, account=data.account, sz=100, lever=lever, symbol_selection=ss_obj,
                                              open_position=op_obj, profit_loss=pl_obj, fund=fd_obj, ws=self.ws,
                                              interval=Interval.CANDLE_15m.value,
                                              max_positions=data.max_position, funSymbol_selection=data.funSymbol_selection,
                                              funOpen_position=data.funOpen_position, funProfit_loss=data.funProfit_loss,
                                              funFund=data.funFund
                                              )
                    self.user_strategies[data.userId] = simEng
                    return True
            else:
                return "WebSocket 未启动"
        except Exception as e:
            self.logger.error(f"添加策略失败: {e}")
            return f"添加策略失败: {e}"

    def remove_strategy(self, data):
        """
        移除策略
        """
        try:
            msg = Base_Message(data)
            userId = msg.data['userId']
            if userId in self.user_strategies:
                if self.user_strategies[userId]:
                    strategy_instance = self.user_strategies[userId]
                    if strategy_instance.running:
                        report = strategy_instance.stop()
                        return report
                    else:
                        del self.user_strategies[userId]
                        return "策略未启动"
                else:
                    return "请先添加策略"
            else:
                return "策略不存在"
        except Exception as e:
            self.logger.error(f"移除策略失败: {e}")
            return f"移除策略失败: {e}"

    def run_strategy(self, data):
        """
        运行策略
        """
        try:
            msg = Base_Message(data)
            userId = msg.data['id']
            if userId in self.user_strategies:
                if not self.user_strategies[userId]:
                    return "请先添加策略"
                else:
                    thread = threading.Thread(target=self.user_strategies[userId].run)
                    thread.start()
                    return "策略已启动"
            else:
                return "策略不存在"
        except Exception as e:
            self.logger.error(f"运行策略失败: {e}")
            return f"运行策略失败: {e}"

    def operation_information(self, data):
        """
        获取策略运行信息
        """
        try:
            msg = Base_Message(data)
            userId = msg.data['id']
            if userId in self.user_strategies and self.user_strategies[userId].running:
                return self.user_strategies[userId].generate_report()
            else:
                return "策略未添加或未启动"
        except Exception as e:
            self.logger.error(f"获取策略信息失败: {e}")
            return f"获取策略信息失败: {e}"

    def build_sub_param(self, interval: Interval, symbol):
        """
        构建订阅参数
        """
        channels = []
        ticker_channels = []
        for s in symbol:
            ticker_channels.append({"channel": "tickers", "instId": str(s)})

        if self.kline_mode == "mark":
            for s in symbol:
                channels.append({"channel": "mark-price-" + interval, "instId": str(s)})
            return channels, ticker_channels

        elif self.kline_mode == "Kline":
            for s in symbol:
                channels.append({"channel": interval, "instId": str(s)})
            return channels, ticker_channels

    def backtesting(self, data):
        """
        回测策略
        """
        try:
            msg = Base_Message(data)
            userId = msg.data['userId']
            symbol = msg.data['symbol']
            interval = msg.data['interval']
            start = msg.data['start']
            end = msg.data['end']
            if userId in self.user_strategies and self.user_strategies[userId].running:
                return self.user_strategies[userId].backtesting(symbol, interval, start, end)
            else:
                return "策略未添加或未启动"
        except Exception as e:
            self.logger.error(f"回测策略失败: {e}")
            return f"回测策略失败: {e}"

    def get_orders(self, data):
        try:
            msg = Base_Message(data)
            userId = msg.data['userId']
            if userId in self.user_strategies and self.user_strategies[userId].running:
                return self.user_strategies[userId].account["orders"]
        except Exception as e:
            self.logger.error(f"获取orders失败: {e}")
            return f"获取orders失败: {e}"

    def get_positions(self, data):
        try:
            msg = Base_Message(data)
            userId = msg.data['userId']
            if userId in self.user_strategies and self.user_strategies[userId].running:
                return self.user_strategies[userId].account["position"]
        except Exception as e:
            self.logger.error(f"获取position失败: {e}")
            return f"获取position失败: {e}"
# 初始化 Main_Engine
main_engine = Main_Engine(symbols_ls=[], kline_mode="Kline")


# 路由处理函数
@app.route('/engine/simulation', methods=['POST'])
def receive_from_java():
    try:
        data = request.json
        action = data.get('data').get('action')

        # 定义 action 到处理函数的映射
        action_handlers = {
            "init_engine": main_engine.init_engine,
            "add_strategy": main_engine.add_strategy,
            "run_strategy": main_engine.run_strategy,
            "remove_strategy": main_engine.remove_strategy,
            "operation_information": main_engine.operation_information,
            "backtesting": main_engine.backtesting,
            "running_strategies": lambda _: [k for k, v in main_engine.user_strategies.items() if v.running],
            "get_orders": main_engine.get_orders,
            "get_positions": main_engine.get_positions
        }

        if action in action_handlers:
            res = action_handlers[action](data)
        else:
            res = "未找到对应的操作"

        # 统一返回格式
        if isinstance(res, str) and not res.startswith('{'):
            response = {
                "code": 1,
                "message": res,
                "data": "",
            }
        else:
            response = {
                "code": 0,
                "message": "success",
                "data": res,
            }
        return jsonify(response)
    except Exception as e:
        return jsonify({
            "code": 1,
            "message": f"请求处理失败: {e}",
            "data": "",
        })


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=1219)
