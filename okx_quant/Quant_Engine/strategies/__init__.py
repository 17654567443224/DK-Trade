"""An unofficial Python wrapper for the OKEx exchange API v3

.. moduleauthor:: Sam McHardy

"""

from Quant_Engine.strategies.Base_Template import Base_Template
from Quant_Engine.strategies.ma_strategy import MAStrategy
from Quant_Engine.strategies.rsi_strategy import RSIStrategy
from Quant_Engine.strategies.bollinger_strategy import BollingerStrategy
from Quant_Engine.strategies.macd_strategy import MACDStrategy
from Quant_Engine.strategies.grid_strategy import GridStrategy

__all__ = [
    'Base_Template',
    'MAStrategy',
    'RSIStrategy',
    'BollingerStrategy',
    'MACDStrategy',
    'GridStrategy'
]
