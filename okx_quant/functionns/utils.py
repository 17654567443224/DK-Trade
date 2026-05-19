import json
import os
import functools
import time
import traceback

from okx.exceptions import OkxAPIException


# 处理服务端消息
def deal_message(msg):
    j_d = json.dumps(msg)
    j_l = json.loads(j_d)
    data = j_l.get('data')
    return data

def check_and_create_file(filename):
    # 检查文件夹是否存在，如果不存在则创建
    if not os.path.exists('Cache'):
        os.makedirs('Cache')

    # 拼接文件路径
    filepath = os.path.join('Cache', filename)

    # 检查文件是否存在
    if os.path.exists(filepath):
        return True
    else:
        # 如果文件不存在则创建
        with open(filepath, 'w') as f:
            f.write('')
        return False

def get_usdt_cny():
    import okx.Market_api as Market
    marketAPI = Market.MarketAPI(True)
    result = deal_message(marketAPI.get_exchange_rate())
    return result[0]['usdCny']

def check_switch(data, open_str, close_str):
    for i in data:
        if i.get('tag') == open_str:
            return False
        elif i.get('tag') == close_str:
            return True


def retry_on_exception_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        switch = True
        while switch:
            try:
                switch = False  # 初始设置为False，除非抛出异常
                return await func(*args, **kwargs)  # 执行原函数并返回其值
            except Exception as e:
                if isinstance(e, OkxAPIException):
                    return
                # print(f"异步{e}")
                switch = True  # 如果抛出异常，将switch设置为True
    return wrapper

import functools


def retry_on_exception_sync(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        switch = True
        last_exception = None  # 用于存储上一次的异常信息
        while switch:
            try:
                switch = False  # 初始设置为False，除非抛出异常
                return func(*args, **kwargs)  # 执行原函数并返回其值
            except Exception as e:
                # 提取异常信息，包括文件名和行号
                tb = traceback.extract_tb(e.__traceback__)[-1]
                error_location = f"File \"{tb.filename}\", line {tb.lineno}, in {tb.name}"

                # 检查是否与上一次的异常信息一致
                if last_exception != str(e):
                    print(f"同步 {e} ({error_location})")
                    last_exception = str(e)  # 更新last_exception
                if isinstance(e, OkxAPIException):
                    if e.code == '50011':
                        time.sleep(2)
                    print("retry", e, e.code, e.status_code)
                    return
                switch = True  # 如果抛出异常，将switch设置为True

    return wrapper

