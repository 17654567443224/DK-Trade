import requests
import json
from random import Random
from collections import defaultdict
from datetime import datetime
from deal_data import api_fun
import setting
import concurrent.futures


# noinspection PyTypeChecker
class wx_robot:
    def __init__(self, user:list, strategy_type:str):
        self.user = user
        self.price_dict = defaultdict(list)
        self.last_added_time = defaultdict(datetime)
        self.sug = ["多", "空"]
        self.profit_count = 0
        self.loss_count = 0
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)  # 设置最大线程数
        self.strategy_type = strategy_type
    def request_markdown(self, text):
        url = setting.Wx_Webhook_url
        headers = {'Content-Type': 'application/json'}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"{text}"
            }
        }
        response = requests.post(url, json=data, headers=headers)
        self.response_text(response)

    def request_text(self, text, user:list, mode=False):
        if mode == False:
            url = setting.Wx_Webhook_url
            data = {
                "msgtype": "text",
                "text": {
                    "content": f"{text}",
                    "mentioned_mobile_list": user
                }
            }
        else:
            url = setting.Wx_Webhook_warning
            data = {
                "msgtype": "text",
                "text": {
                    "content": f"{text}"
                }
            }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        self.response_text(response)
    def request_text_self(self, text, user:list, mode=False):
        if mode == False:
            ad = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c93a1cb4-5822-4d7c-a203-acd8ded2e6ec'
            data = {
                "msgtype": "text",
                "text": {
                    "content": f"{text}",
                    "mentioned_mobile_list": user
                }
            }
        else:
            ad = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c93a1cb4-5822-4d7c-a203-acd8ded2e6ec'
            data = {
                "msgtype": "text",
                "text": {
                    "content": f"{text}"
                }
            }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(ad, json=data, headers=headers)
        self.response_text(response)
    def response_text(self, response):
        try:
            res = json.loads(response.text)
            if res.get("errcode") != 0:
                print(f"error: {res}")
        except Exception as e:
            print(e)

    def normal_text(self, msg):
        text = f"""日志信息
====={msg}=====
        """
        self.executor.submit(self.request_text, text, self.user)

    def push_order(self, symbol, order_type, multiplier=0, pnl=0):
        if order_type == "止盈":
            self.profit_count += 1
        elif order_type == "止损":
            self.loss_count += 1
        al = self.profit_count + self.loss_count
        try:
            cal = float(self.profit_count / al) * 100
            cal = round(cal, 2)
        except:
            cal = 0
        text = f"""***订单成交***
策略类型: {self.strategy_type}
交易对：{symbol}
成交类型：{order_type}
订单倍数：{multiplier}
收益：{pnl}
订单总数：{al}
盈利总数：{self.profit_count}
亏损总数：{self.loss_count}
胜率：{cal}%
"""
        self.executor.submit(self.request_text, text, self.user)

    def push_position(self, symbol, liqpx, avgpx, mode, lever, uplRatio):
        uplRatio = uplRatio * 100
        text = f"""***仓位信息推送***
策略类型: {self.strategy_type}
交易对：{symbol}
方向：{mode}
杠杆倍数：{lever}
爆仓价格：{liqpx}
开仓均价：{avgpx}
收益百分比：{uplRatio}%
可以平仓提速！！！
        """
        self.executor.submit(self.request_text, text, self.user)

    def price_monitor(self, symbol, max_change, type_, warning):
        user_ = [""]
        type_m = ""
        rand = Random()
        sug = self.sug[rand.randint(0, 1)]
        now = datetime.now()
        if type_ == "建仓":
            type_m = "做多"
        else:
            type_m = "做空"
        if symbol not in self.price_dict or len(self.price_dict[symbol]) < 2:
            if symbol in self.price_dict and all(
                    (now - timestamp).total_seconds() >= 15 * 60 for _, timestamp in self.price_dict[symbol]):
                self.price_dict[symbol].append((max_change, now))
                text = f"""***价格监控***
---更新信息---
交易对：{symbol}
涨跌幅：{max_change}%
警报等级：{warning}
亏闷了还是赚麻了？0.o
                                """
                self.executor.submit(self.request_text, text, user_, mode=True)
            elif symbol not in self.price_dict:
                text = f"""***价格监控***
---发现狗庄{type_}币种---
交易对：{symbol}
涨跌幅：{max_change}%
警报等级：{warning}
开仓建议：{sug}(投资建议仅供参考)
本人建议：{type_m}(投资建议仅供参考)
                                            """
                self.price_dict[symbol] = [(max_change, now)]
                self.executor.submit(self.request_text, text, user_, mode=True)
        elif len(self.price_dict[symbol]) == 2:
            text = f"""***价格监控***
---发现狗庄{type_}币种---
交易对：{symbol}
涨跌幅：{max_change}%
警报等级：{warning}
开仓建议：{sug}(投资建议仅供参考)
本人建议：{type_m}(投资建议仅供参考)
                            """
            self.price_dict[symbol] = [(max_change, now)]
            self.executor.submit(self.request_text, text, user_, mode=True)

    def start(self):
        self._start()
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        text = f"""***策略开始运行***
运行时间：{formatted_time}
        """
        self.executor.submit(self.request_text, text, self.user, mode=True)

    def _start(self):
        text = api_fun()
        self.executor.submit(self.request_text_self, text, ['15548719961'])
# user = ["15548719961"]
# a = wx_robot(user=user)
# a.price_monitor("111",12,"砸盘")