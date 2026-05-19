from decimal import Decimal

from Quant_Engine.utils import deal_message, retry_on_exception_sync
import okx.Public_api as Public
from functionns import setting


class BaseFundTemplate:
    def __init__(self, account, lever, invest_amount=None, martin_amount=None, max_amount=None, init_amount=None, positions: dict = None):
        self.positions = positions  # 仓位字典
        self.account = account  # 账户余额
        self.account["balance"] = Decimal(self.account["balance"])
        self.account["orderFee"] = float(self.account["orderFee"])
        self.publicAPI = Public.PublicAPI(False)
        self.order_fee = self.account["orderFee"]  # 手续费
        self.init_amount = init_amount  # 初始金额
        self.lever = lever
        self.invest_amount = invest_amount
        self.martin_amount = martin_amount
        self.max_amount = max_amount
        self.martin_mode = 'common'

    def fixed_investment(self, td, symbol, price):
        """
        :param symbol: 交易对
        :param invest_amount: 数额
        :return:
        """
        # 定投
        sz = self._check_size(td, symbol, price, self.invest_amount)
        if sz == -1 or sz == '0':
            return False
        return sz

    def martin_investment(self, td, symbol, price):
        """
        :param martin_amount: 倍数
        :param max_amount: 最大倍数
        :return:
        """
        multiple = 1
        if self.max_amount and self.martin_amount <= self.max_amount:
            if self.positions:
                for i in self.positions:
                    if self.martin_mode == 'common':
                        if float(i.get('upl')) < 0:
                            multiple *= self.martin_amount
                            continue
                    elif self.martin_mode == 'reverse':
                        if float(i.get('upl')) > 0:
                            multiple *= self.martin_amount
                            continue
                    break
        sz = multiple * self.init_amount
        sz = self._check_size(td, symbol, price, sz)
        return sz

    @retry_on_exception_sync
    def _check_size(self, td, symbol, price, usdt):
        symbol = self._remove_swap(symbol)
        lever = self.lever
        result = deal_message(self.publicAPI.get_instruments(instType='SWAP', instFamily=symbol))
        ctVal = result[0]['ctVal']
        minSz = result[0]['minSz']
        result = deal_message(self.publicAPI.get_tier(instType='SWAP', instFamily=symbol, tdMode='isolated'))
        for i in result:
            if i['maxSz'] is None or i['minSz'] is None:
                continue
            elif Decimal(i['maxLever']) == Decimal(lever):  # and Decimal(usdt) < Decimal(i['maxSz']) and Decimal(usdt) > Decimal(i['minSz'])
                val = Decimal(usdt) * Decimal(lever)
                size = self._convert_contract_coin(symbol, order_type='open', price=price, val=str(val))
                if Decimal(size) <= Decimal(i['maxSz']) and Decimal(size) >= Decimal(minSz):
                    imr = i['imr']
                    mmr = i['mmr']
                    liq_price = self.calculate_liquidation_price(imr, ctVal, size, price, mmr,
                                                                 self.order_fee, td)
                    if setting.sim:
                        return val, liq_price, lever
                    return Decimal(size), liq_price, lever
            elif Decimal(i['maxLever']) < Decimal(lever):
                lever = i['maxLever']
                continue
        return -1


    def _convert_contract_coin(self, symbol, val, price,
                              order_type):  # transform_sheet_coin price:limit val：usdt order_type:  open  close
        symbol = self._remove_swap(symbol)
        try:
            cv_co = deal_message(
            self.publicAPI.convert_contract_coin(instId=f'{symbol}-SWAP', sz=val, px=str(price), opType=order_type,
                                                 unit='usds'))
        except Exception as e:
            print(e)
        return cv_co[0].get('sz')

    def _remove_swap(self, symbol):
        if '-SWAP' in symbol:
            symbol = symbol.replace("-SWAP", "")
        return symbol

    def calculate_liquidation_price(self, initial_margin_rate, notional_value, num_contracts, entry_price,
                                    maintenance_margin_rate, fee_rate, position_type):
        """
        计算USDT保证金合约的多仓或空仓强平价格，使用高精度 Decimal。

        参数:
        - initial_margin_rate (Decimal): 最低初始保证金率（如 Decimal('0.05') 表示 5%）。
        - notional_value (Decimal): 面值（每张合约的名义价值）。
        - num_contracts (int): 合约张数（正数表示多仓，负数表示空仓）。
        - entry_price (Decimal): 开仓均价。
        - maintenance_margin_rate (Decimal): 维持保证金率（如 Decimal('0.005') 表示 0.5%）。
        - fee_rate (Decimal): 手续费率（如 Decimal('0.0004') 表示 0.04%）。
        - position_type (str): 持仓类型 ("long" 表示多仓, "short" 表示空仓)。

        返回:
        - Decimal: 强平价格。
        """
        # 转换参数为 Decimal 类型（确保输入为数字或字符串）
        initial_margin_rate = Decimal(initial_margin_rate)
        notional_value = Decimal(notional_value)
        entry_price = Decimal(entry_price)
        maintenance_margin_rate = Decimal(maintenance_margin_rate)
        fee_rate = Decimal(fee_rate)
        num_contracts = Decimal(num_contracts)
        # 计算保证金余额
        margin_balance = abs(num_contracts) * notional_value * entry_price * initial_margin_rate

        # 根据持仓类型计算强平价格
        if position_type == 1:  # 多仓
            denominator = abs(num_contracts) * notional_value * (maintenance_margin_rate + fee_rate - 1)
            if denominator == 0:
                raise ZeroDivisionError("Denominator is zero during long liquidation price calculation.")
            liquidation_price = (margin_balance - abs(num_contracts) * notional_value * entry_price) / denominator
        elif position_type == 0:  # 空仓
            denominator = abs(num_contracts) * notional_value * (maintenance_margin_rate + fee_rate + 1)
            if denominator == 0:
                raise ZeroDivisionError("Denominator is zero during short liquidation price calculation.")
            liquidation_price = (margin_balance + abs(num_contracts) * notional_value * entry_price) / denominator
        else:
            raise ValueError("Invalid position type. Use 'long' for多仓 or 'short' for空仓.")

        return liquidation_price