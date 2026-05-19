from enum import Enum

bar_property = ["open", "high", "low", "close", "volume"]

math_bar_property = ["add", "subtract", "multiply", "divide"]
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

class Books_channel(Enum):
    # 首次推400档快照数据，以后增量推送，每100毫秒推送一次变化的数据
    BOOKS = "books"
    # 首次推5档快照数据，以后定量推送，每100毫秒当5档快照数据有变化推送一次5档数据
    BOOKS5 = "books5 "
    # 首次推1档快照数据，以后定量推送，每10毫秒当1档快照数据有变化推送一次1档数据
    BBO_TBT = "bbo-tbt"
    # 首次推400档快照数据，以后增量推送，每10毫秒推送一次变化的数据
    BOOKS_12_TBT = "books-l2-tbt"
    # 首次推50档快照数据，以后增量推送，每10毫秒推送一次变化的数据
    BOOKS50_12_TBT = "books50-l2-tbt"

class Exchange(Enum):
    OKX = "okx"
    BINANCE = "binance"

class Books_action(Enum):
    # 全量
    SNAPSHOT = "snapshot"
    # 增量
    UPDATE = "update"

class Open_Posotion_Element(Enum):
    LABEL = "label"
    ACTION = "action"
    ARGS = "args"
    BAR = "bar"

class Sign(Enum):
    FI = "if"
    EQUAL = "=="
    GREATER = ">"
    LESS = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    END = ":"
    AND = "and"
    OR = "or"
    ADD = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"
    METHOD = "m"
    BAR = "b"
    ENTER = "e"
    RETURN = "return"
    ELSE = "else"
    ELIF = "elif"
    LONG = "1"
    SHORT = "0"
    BACK = "k"
    IS = "="
    TD = "td"
