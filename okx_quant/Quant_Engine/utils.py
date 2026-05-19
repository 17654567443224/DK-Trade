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

def compare_with_operator(a, b, operator):
    # 字典映射操作符
    operators = {
        ">": lambda x, y: x > y,
        "<": lambda x, y: x < y,
        "=": lambda x, y: x == y,
        ">=": lambda x, y: x >= y,
        "<=": lambda x, y: x <= y,
    }

    # 获取对应操作符的函数
    if operator in operators:
        return operators[operator](a, b)
    else:
        raise ValueError("Invalid operator")


from functools import wraps, lru_cache
from inspect import signature
from typing import get_type_hints, Union


@lru_cache(maxsize=100)
def get_cached_type_hints(func):
    return get_type_hints(func)


def enforce_types(func):
    type_hints = get_cached_type_hints(func)
    sig = signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        for name, value in bound_args.arguments.items():
            if name in type_hints and value is not None:
                target_type = type_hints[name]
                try:
                    # 处理 Union 类型
                    if getattr(target_type, "__origin__", None) is Union:
                        for t in target_type.__args__:
                            try:
                                bound_args.arguments[name] = t(value)
                                break
                            except (TypeError, ValueError):
                                continue
                        else:
                            raise TypeError(
                                f"参数 '{name}' 无法转换为 {target_type}，"
                                f"输入值: {value} ({type(value)})"
                            )
                    else:
                        bound_args.arguments[name] = target_type(value)
                except (TypeError, ValueError) as e:
                    raise TypeError(
                        f"参数类型错误 - {name}: "
                        f"需要 {target_type}, 实际得到 {type(value)}"
                    ) from e

        return func(*bound_args.args, **bound_args.kwargs)

    return wrapper