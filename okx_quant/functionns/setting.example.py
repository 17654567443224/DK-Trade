from enum import Enum
class Interval(Enum):
    CANDLE_3M = "3M"
    CANDLE_1M = "1M"
    CANDLE_1W = "candle1W"
    CANDLE_1D = "candle1D"
    CANDLE_2D = "candle2D"
    CANDLE_3D = "candle3D"
    CANDLE_5D = "candle5D"
    CANDLE_12H = "candle12H"
    CANDLE_6H = "candle6H"
    CANDLE_4H = "candle4H"
    CANDLE_2H = "candle2H"
    CANDLE_1H = "candle1H"
    CANDLE_30m = "candle30m"
    CANDLE_15m = "candle15m"
    CANDLE_5m = "candle5m"
    CANDLE_3m = "candle3m"
    CANDLE_1m = "candle1m"
# 2. 将项目加入pythonpath中,当前工程名字为data-slo
# export PYTHONPATH=$PYTHONPATH:/home/ubuntu/okx_quant
# 代理  不用置为None 改client的代码 _request
Black_list = ['BNB-USDT-SWAP']  # 黑名单
proxies= {
    'http': 'http://127.0.0.1:7897',
    'https': 'http://127.0.0.1:7897'
}

quick_trade_switch = 50  #  ，如果不是最后一次开仓会过滤杠杆倍数低于50的币
load_interval = 10  # 根据几根kline计算avg，默认根据10跟线来计算是否达到开仓条件（）
symbol_count = None  # 过滤交易对截取前n个，默认None不截取（根据每日交易额one_day_trade计算，如果只想交易主流b的话就截取）
liqpx_slip = 0.0004  # 强平提前止损百分比，0.0005，防爆仓提前挂单止损，但是遇到强插针还是有爆仓风险
Trigger_slip = 0.0005  # 触发价提前百分比0.0005，挂单（包含止盈）的触发价，防止挂不上止盈止损
order_wait_time = 120  # 订单成交的等待时间120，超时自动取消订单
order_fee = 0.0002  # taker手续费
sim = True  # 实盘模拟，体现在资金策略的sz
flag = '0'  # 0实盘，1模拟盘，下面把apikey和secretkey以及passphrase改成自己的其他别动
if flag == '0':
    public_url = "wss://ws.okx.com:8443/ws/v5/public"
    private_url = "wss://ws.okx.com:8443/ws/v5/private"
    mark_klprice = "wss://ws.okx.com:8443/ws/v5/business"
    api_key = "YOUR_LIVE_API_KEY"          # 在OKX后台创建API Key
    secret_key = "YOUR_LIVE_SECRET_KEY"    # API Secret Key
    passphrase = "YOUR_LIVE_PASSPHRASE"    # API Passphrase
else:
    public_url = "wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999"
    private_url = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
    mark_klprice = "wss://wspap.okx.com:8443/ws/v5/business?brokerId=9999"
    api_key = "YOUR_PAPER_API_KEY"         # 模拟盘 API Key
    secret_key = "YOUR_PAPER_SECRET_KEY"   # 模拟盘 Secret Key
    passphrase = "YOUR_PAPER_PASSPHRASE"   # 模拟盘 Passphrase
interval = Interval.CANDLE_15m  # 时间粒度的枚举类型，按照上面的interval枚举类来写
rest_interval = '15m'  # 1m/3m/5m/15m/30m/1H/2H/4H  计算数据使用的线的时间粒度，1分钟/5分钟/15分钟/.....
update_interval = 900  # 单位秒，更新 Interval.CANDLE_15m 的时间间隔，更新线数据的间隔时间，15m就是每隔15分钟更新一次数据，也就是900秒
position_update = 450  # 动态止盈的时间450，如果仓位长时间处于小范围波动且收益大于动态止盈最低值就会平仓提速
profit_min = 0.35  # 动态止盈最低值0.35 成交价
float_val = 0.05  # 动态止盈波动值0.05，触发价
one_day_trade = 200000000  # 过滤每日成交量低的交易对，单位人民币（好像是）200000000
max_retries = 5  # 没用
quick_tradingview = 0.02  # 获取最近10根kline ，纯趋势单边， 幅度大于？
profit_per = 0.65  # 利润百分比0.65，默认百分之65止盈
stop_loss = -0.50  #  止损百分比  没什么用-0.49，-百分之49止损
Incremental_multiplier = 3  # 仓位递增倍数，默认3，比如1，3，9，27，81
max_fail_count = 243  ##  最后一次开仓的份数：1，3，9，27，81，243
total_fail_count = 365  ## 一共分成多少份1+3+9+27+81+243
fail_count_reset = True  # 重设失败次数，默认为True，不会根据历史仓位来初始化仓位份数，即初始仓位份数为1，如果设置为False会根据历史仓位计算初始仓位份数
steady_switch = False  # 稳健模式，初始本金为300
proportion = 0.8  # 本金分配比例
add_extra = 2  # 增加容错（从第几次开始进行倍投） 2==3

# 没用
opportunity_trade_switch = True  # 机会策略
opportunity_interval = '1D'
opportunity_proportion = 0.2  # 本金分配比例
opportunity_max_pos = 5  # 最大持仓个数，也是该策略的本金平均分配份数

sustainable_trade_switch = True  # 永续策略
sustainable_extra_fail = 2  # 额外重试次数
sustainable_lever_min = 50  # 最低杠杆 修改时一定修改sustainable_profit_per sustainable_stop_loss
sustainable_profit_per = 0.20  # 止盈
sustainable_stop_loss = -0.25  # 止损
sustainable_proportion = 0.2  # 本金分配比例
sustainable_extra = 3  # 增加容错（从第几次开始进行倍投）

quick_trading_switch = True  # 高频策略
quick_circulate_switch = True  # 是否循环
quick_lever_max = 50  # 最高杠杆 100 >= 4% 50 >= 2%
quick_fee_percent = 0.002  # 手续费占比
quick_profit_per = 0.08  #  止盈（除去手续费之后）0.11
quick_stop_loss = -0.08  # 止损 0.075
quick_proportion = 0.3  # 本金分配比例
quick_extra = 2  # 增加容错（从第几次开始进行倍投）

user = ["YOUR_WECHAT_PHONE_NUMBER"]  # wx机器人推送仓位信息时艾特的人，填入想艾特的人的手机号即可
Wx_Webhook_url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_WEBHOOK_KEY'  # 微信机器人webhook地址
Wx_Webhook_warning = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_WARNING_WEBHOOK_KEY'

# 以下内容没测试，稳定性未知，请勿将spot_switch设置为True
# proxy_host = "127.0.0.1"  # set it to your proxy_host 如果没有就设置为"", 如果有就设置为你的代理主机如：127.0.0.1
# proxy_port = 7897  # set it to your proxy_port  设置你的代理端口号如: 1087, 没有你修改为0,但是要保证你能访问api.binance.com这个主机。

spot_switch = False
spot_value = 0.2  # 与主策略的资金比例
spot_level = 10
spot_count = 10  # 最大多少个spot订单
spot_profit = 0.01  # 默认15个点止盈
