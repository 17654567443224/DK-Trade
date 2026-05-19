from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum

from typing import Any, Optional

class Capital_mode(Enum):
    PERCENT = "percent"
    NUMBER = "number"
    CUSTOM = "custom"

class BaseTemplate(ABC):
    def __init__(self, symbols_fun, total_capital):
        self.total_capital = total_capital
        self.symbols_ls = self.get_symbols(symbols_fun)

    def get_symbols(self, symbols_fun: Any) -> Optional[list]:  # 选b策略
        if isinstance(symbols_fun, list):
            return symbols_fun
        elif callable(symbols_fun):
            return symbols_fun()
        else:
            return []

    @abstractmethod
    def open_position(self, size):
        pass

    def capital(self, capital_mode, achieve) -> str:
        if isinstance(achieve, str):
            if capital_mode == Capital_mode.NUMBER:
                return achieve

            elif capital_mode == Capital_mode.PERCENT:
                return self.total_capital * Decimal(achieve)

        elif capital_mode == Capital_mode.CUSTOM and callable(achieve):
            return achieve()

    @abstractmethod
    def capital_strategy(self):
        pass

    @abstractmethod
    def profit_loss(self):
        pass

    @abstractmethod
    def public_sub(self):
        pass

    @abstractmethod
    def private_sub(self):
        pass

