from decimal import Decimal


async def spot_monitor(data, spot_price_dict, symbol):  # data最新数据, spot_price_dict历史数据, symbol
    total_val = Decimal(0)
    new_data = data[-1]
    for i in range(1, len(spot_price_dict[symbol])):
        data = spot_price_dict[symbol]
        high = Decimal(data[i][2])
        low = Decimal(data[i][3])
        val = (high - low) / ((high + low) / Decimal(2))
        total_val += val
    average_val = total_val / Decimal(len(data))
    new_val = (Decimal(new_data[2]) - Decimal(new_data[3])) / ((Decimal(new_data[2]) + Decimal(new_data[3])) / Decimal(2))
    if new_val - average_val > average_val * 2:
        open_price = Decimal(new_data[1])
        if Decimal(new_data[2]) - open_price > open_price - Decimal(new_data[3]):  # 多
            return 1, new_data[2]
        else:
            return -1, new_data[3]
    else:
        return 0, 0