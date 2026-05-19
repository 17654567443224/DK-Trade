import ast
from typing import List



from Quant_Engine.Common.constants import Open_Posotion_Element, Sign, bar_property
from ast import literal_eval

from Quant_Engine.template.open_position_template.target import ArrayManager


class Customize:

    def __init__(self, strategy):
        """
        {
            ...
            strategy: decode
                {
                    label: []
                    action: []"if " m / b / e [] 3 需要return 0/1
                    bar: []
                    args:[ 2
                        {
                        手动传入arg
                        ohlc 自动
                        }
                    ]
        }
        """
        self.strategy = strategy

    def creat_strategy(self, am: ArrayManager):
        methods_res = []
        label = self.strategy[Open_Posotion_Element.LABEL.value]
        action = self.strategy[Open_Posotion_Element.ACTION.value]
        bar = self.strategy[Open_Posotion_Element.BAR.value]
        args = self.strategy[Open_Posotion_Element.ARGS.value]
        args = self.build_args(am, args)
        bar = self.build_bars(am, bar)
        if isinstance(label, list):
            for i, j in zip(label, args):
                if hasattr(am, i):
                    method = getattr(am, i, None)
                    res = method(**j)
                    methods_res.append(res)
                else:
                    return False
        if not isinstance(bar, list):
            return False
        code = self.build_condition(action, methods_res, bar)
        parsed_code = ast.parse(code)
        # 创建一个字典来存储动态生成的变量
        exec_locals = {}

        # 执行代码，并将变量存储到 exec_locals 中
        exec(compile(parsed_code, filename="<string>", mode="exec"), {}, exec_locals)

        # 获取 td 的值
        td = exec_locals.get("td")
        return td

    def build_condition(self, actions, methods_res, bar):
        code_lines = []  # 存储代码行
        indent = 0  # 缩进级别
        sign_ls = [m.value for m in Sign]
        is_first_line = True  # 标记是否是第一行
        is_back = False
        for i in actions:
            if i in sign_ls:
                if i == Sign.END.value:
                    # 在当前行末尾添加冒号
                    if code_lines:  # 确保 code_lines 不为空
                        code_lines[-1] += i
                    else:
                        code_lines.append(i)  # 如果 code_lines 为空，直接添加冒号
                    # 增加缩进级别
                    indent += 1
                    # 冒号之后换行
                    code_lines.append(" " * (indent * 3))  # 添加一个空行并缩进
                    is_first_line = False  # 第一行已处理
                elif i == Sign.ENTER.value:
                    # 添加换行符
                    code_lines.append(" " * (indent * 3))  # 换行并保持缩进
                    is_first_line = False  # 第一行已处理
                elif i == Sign.METHOD.value:
                    # 确保 code_lines 不为空
                    if not code_lines:
                        code_lines.append("")
                    # 添加方法结果
                    code_lines[-1] += " " + str(methods_res.pop(0))
                    is_first_line = False  # 第一行已处理
                elif i == Sign.BAR.value:
                    # 确保 code_lines 不为空
                    if not code_lines:
                        code_lines.append("")
                    # 添加 bar 数据
                    code_lines[-1] += " " + str(bar.pop(0))
                    is_first_line = False  # 第一行已处理
                elif i == Sign.BACK.value:
                    # 回退缩进
                    indent -= 1
                    # 确保缩进级别不小于 0
                    indent = max(indent, 0)
                    # 添加一个空行并应用新的缩进
                    code_lines.append(" " * (indent * 4))
                    is_back = True
                    is_first_line = False  # 第一行已处理
                else:
                    # 添加非符号内容
                    if is_first_line:
                        # 第一行不加缩进
                        code_lines.append(i)
                        is_first_line = False
                        continue
                    # 确保 code_lines 不为空
                    elif not code_lines:
                        code_lines.append("")
                    # 添加其他符号
                    if is_back:
                        code_lines[-1] += i
                        is_back = False
                    else:
                        code_lines[-1] += " " + i
                    is_first_line = False  # 第一行已处理
            else:
                # 非第一行，应用当前缩进
                code_lines.append(" " + i)

        # 拼接为完整的代码字符串
        code = "\n".join(line for line in code_lines if line.strip())
        print(code)
        return code
    @staticmethod
    def build_args(am: ArrayManager, args: List[dict]):
        for i in args:
            if "open" in i:
                i["open"] = am.open_array[-1]
            elif "high" in i:
                i["high"] = am.high_array[-1]
            elif "low" in i:
                i["low"] = am.low_array[-1]
            elif "close" in i:
                i["close"] = am.close_array[-1]
            elif "volume" in i:
                i["volume"] = am.volume_array[-1]
        return args

    @staticmethod
    def build_bars(am: ArrayManager, bars: List[dict]):
        res = []
        for i in bars:
            if "open" == i:
                res.append(am.open_array[-1])
            elif "high" == i:
                res.append(am.high_array[-1])
            elif "low" == i:
                res.append(am.low_array[-1])
            elif "close" == i:
                res.append(am.close_array[-1])
            elif "volume" == i:
                res.append(am.volume_array[-1])
        return res







