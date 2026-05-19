from decimal import Decimal


class Base_Template:
    def __init__(self, lever, tp_points=None, sl_points=None, tp_percent=None, sl_percent=None):
        self.lever = lever
        self.tp_points = tp_points
        self.sl_points = sl_points
        self.tp_percent = tp_percent
        self.sl_percent = sl_percent

    # ------------------------- 核心逻辑 -----------------------------
    def _adjust_by_leverage(self, value, mode):
        """根据杠杆调整参数值（私有方法）"""
        if mode == 'points':
            return value / self.lever  # 点数需按杠杆缩小
        elif mode == 'percent':
            return value / self.lever  # 百分比也按杠杆缩小
        else:
            return value

    # ------------------------- 策略方法 -----------------------------
    def get_fixed_point_levels(self, symbol, td, avg_price):
        """
        固定点数止盈止损（考虑杠杆）
        :param tp_points: 原始止盈点数（基于无杠杆的预期风险）
        :param sl_points: 原始止损点数
        :return: (止盈价, 止损价)
        """
        # 调整点数：杠杆越高，实际允许的点数越小
        tp_adj = self._adjust_by_leverage(self.tp_points, mode='points')
        sl_adj = self._adjust_by_leverage(self.sl_points, mode='points')

        if td == 1:  # 多单
            return (
                Decimal(avg_price) + Decimal(tp_adj),
                Decimal(avg_price) - Decimal(sl_adj)
            )
        else:  # 空单
            return (
                Decimal(avg_price) - Decimal(tp_adj),
                Decimal(avg_price) + Decimal(sl_adj)
            )

    def get_percentage_levels(self, symbol, td, avg_price):
        """
        百分比止盈止损（考虑杠杆）
        :param tp_percent: 原始止盈百分比（基于无杠杆的预期风险）
        :param sl_percent: 原始止损百分比
        :return: (止盈价, 止损价)
        """
        # 调整百分比：杠杆越高，实际允许的波动越小
        tp_adj = self._adjust_by_leverage(self.tp_percent, mode='percent')
        sl_adj = self._adjust_by_leverage(self.sl_percent, mode='percent')

        if td == 1:  # 多单
            return (
                Decimal(avg_price) * (Decimal('1') + Decimal(tp_adj) / Decimal('100')),
                Decimal(avg_price) * (Decimal('1') - Decimal(sl_adj) / Decimal('100')),
            )
        else:  # 空单
            return (
                Decimal(avg_price) * (Decimal('1') - Decimal(tp_adj) / Decimal('100')),
                Decimal(avg_price) * (Decimal('1') + Decimal(sl_adj) / Decimal('100')),
            )
