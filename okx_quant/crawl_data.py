import pandas as pd
import time
from datetime import datetime
import requests
import pytz
from tzlocal import get_localzone_name
from threading import Thread
import pymysql
pd.set_option('expand_frame_repr', False)
BINANCE_SPOT_LIMIT = 1000
BINANCE_FUTURE_LIMIT = 1500
LOCAL_TZ = pytz.timezone(get_localzone_name())
def conn_database():
    connection = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="lxw2866",
        database="market_data",
        charset="utf8mb4"
    )
    cursor = connection.cursor()
    return connection, cursor

def conn_strategy_database():
    """连接到策略数据库"""
    connection = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="lxw2866",
        database="dk-qaunt",
        charset="utf8mb4"
    )
    cursor = connection.cursor()
    return connection, cursor

def query_table():
    connection, cursor = conn_database()
    # 查询所有表名
    cursor.execute("SHOW TABLES;")
    # 获取表名列表
    tables = cursor.fetchall()
    return tables

def creat_table(table_name):
    connection, cursor =conn_database()
    # 创建表（如果不存在）
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name}  (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp DECIMAL(13) NOT NULL,
        open DECIMAL(18, 9) NOT NULL,
        high DECIMAL(18, 9) NOT NULL,
        low DECIMAL(18, 9) NOT NULL,
        close DECIMAL(18, 9) NOT NULL,
        volume DECIMAL(16, 4) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    print("Table created successfully.")
    cursor.close()
    connection.close()

def create_strategy_position_table():
    """创建用户策略持仓表"""
    connection, cursor = conn_strategy_database()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_strategy_position  (
        id BIGINT NOT NULL AUTO_INCREMENT COMMENT 'id',
        strategy_id BIGINT NOT NULL COMMENT '策略id',
        symbol VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '交易对',
        sz VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '数量',
        entry_price VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '开仓价格',
        tp VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '止盈价格',
        sl VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '止损价格',
        createTime DATETIME NOT NULL COMMENT '创建时间',
        PRIMARY KEY (id) USING BTREE
    ) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;
    """
    cursor.execute(create_table_query)
    print("User strategy position table created successfully.")
    cursor.close()
    connection.close()

def create_strategy_orders_table():
    """创建用户策略订单表"""
    connection, cursor = conn_strategy_database()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_strategy_orders  (
        id BIGINT NOT NULL AUTO_INCREMENT COMMENT 'id',
        strategy_id BIGINT NOT NULL COMMENT '策略id',
        symbol VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '交易对',
        type VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '开平类型',
        entry_price VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '开仓均价',
        price VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '平仓均价',
        sz VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '数量',
        time DATETIME NOT NULL COMMENT '平仓时间',
        pnl VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '收益',
        pnl_ratio VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '收益率',
        exit_type VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL COMMENT '平仓类型',
        PRIMARY KEY (id) USING BTREE
    ) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;
    """
    cursor.execute(create_table_query)
    print("User strategy orders table created successfully.")
    cursor.close()
    connection.close()

def insert_data(table_name, data):
    connection, cursor = conn_database()
    insert_query = f"""
    INSERT INTO {table_name} (timestamp, open, high, low, close, volume)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    batch_size = 100000
    for i in range(0, len(data), batch_size):
        # 获取当前批次的数据
        batch_data = [
            (record[0], record[1], record[2], record[3], record[4], record[7])
            for record in data[i:i + batch_size]
        ]

        # 批量插入当前批次数据
        cursor.executemany(insert_query, batch_data)
        connection.commit()  # 每插入一批次的数据提交一次事务
        print(f"Inserted batch {i // batch_size + 1} of {batch_size} records")
    # 提交事务并关闭连接
    connection.commit()
    cursor.close()
    connection.close()

def generate_datetime(timestamp: float) -> datetime:
    """
    :param timestamp:
    :return:
    """
    dt = datetime.fromtimestamp(timestamp / 1000)
    dt = LOCAL_TZ.localize(dt)
    return dt


def get_binance_data(symbol: str, exchange: str, start_time: str, end_time: str, interval: str):
    """
    crawl binance exchange data
    :param symbol: BTCUSDT.
    :param exchange: spot、usdt_future, inverse_future.
    :param start_time: format :2020-1-1 or 2020-01-01 year-month-day
    :param end_time: format: 2020-1-1 or 2020-01-01 year-month-day
    :param gate_way the gateway name for binance is:BINANCE_SPOT, BINANCE_USDT, BINANCE_INVERSE
    :return:
    """

    api_url = ''
    save_symbol = symbol
    gateway = "BINANCE_USDT"
    if exchange == 'spot':
        print("spot")
        limit = BINANCE_SPOT_LIMIT
        save_symbol = symbol.lower()
        gateway = 'BINANCE_SPOT'
        api_url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'

    elif exchange == 'usdt_future':
        print('usdt_future')
        limit = BINANCE_FUTURE_LIMIT
        gateway = "BINANCE_USDT"
        api_url = f'https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}'

    elif exchange == 'inverse_future':
        print("inverse_future")
        limit = BINANCE_FUTURE_LIMIT
        gateway = "BINANCE_INVERSE"
        f'https://dapi.binance.com/dapi/v1/klines?symbol={symbol}&interval={interval}&limit={limit}'

    else:
        raise Exception('the exchange name should be one of ：spot, usdt_future, inverse_future')

    start_time = int(datetime.strptime(start_time, '%Y-%m-%d').timestamp() * 1000)
    end_time = int(datetime.strptime(end_time, '%Y-%m-%d').timestamp() * 1000)

    while True:
        try:
            print(start_time)
            url = f'{api_url}&startTime={start_time}'
            print(url)
            datas = requests.get(url=url, timeout=100, proxies=proxies).json()

            """
            [
                [
                    1591258320000,      // open time
                    "9640.7",           // open price
                    "9642.4",           // highest price
                    "9640.6",           // lowest price
                    "9642.0",           // close price(latest price if the kline is not close)
                    "206",              // volume
                    1591258379999,      // close time
                    "2.13660389",       // turnover
                    48,                 // trade count 
                    "119",              // buy volume
                    "1.23424865",       //  buy turnover
                    "0"                 // ignore
                ]

            """
            table_name = symbol + f"_{interval}"
            insert_data(table_name, datas)

            # exit the loop, if close time is greater than the current time
            if (datas[-1][0] > end_time) or datas[-1][6] >= (int(time.time() * 1000) - 60 * 1000):
                break

            start_time = datas[-1][0]

        except Exception as error:
            print(error)
            time.sleep(10)

def download_future(symbol, interval, start, end):
    """
    download binance future data, config your start date and end date(format: year-month-day)
    :return:
    start & end: xxxx-xx-xx
    """

    t1 = Thread(target=get_binance_data, args=(symbol, 'usdt_future', start, end, interval))
    t1.start()
    t1.join()



if __name__ == '__main__':

    """
    @important Note:
    read the code before running it. the software crawl the binance data then save into the sqlite database.
    you may need to change the start date and end date.

    set the proxy_host and proxy_port: if you can directly connect to the binance exchange, 
    then set the proxy_host to None and proxy_port to empty string ""
    you can use the command ping api.binance.com to check whether your network works

    @重要提示：
    如果你的网络不能直连binance.com交易所，你需要设置proxy_host 和 proxy_port, 具体的设置看你代理的主机和端口。如果能直连的话，
    就设置proxy_host = None, proxy_port = ""
    你可以在终端运行输入命令看看自己的网络能否连接交易所： ping api.binance.com
    """

    # set your proxy_host
    # 如果没有就设置为 None, 如果有就设置为你的代理主机如：127.0.0.1
    proxy_host = "127.0.0.1"

    # set it to your proxy_port
    # 设置你的代理端口号如: 1087, 没有你修改为0,但是要保证你能访问api.binance.com这个主机。
    proxy_port = 7897

    proxies = "127.0.0.1"
    if proxy_host and proxy_port:
        proxy = f'http://{proxy_host}:{proxy_port}'
        proxies = {'http': proxy, 'https': proxy}
    creat_table(table_name="BTCUSDT_4h")
    download_future(symbol="BTCUSDT", interval="4h")  # crawl usdt_future data. 下载合约的数据
