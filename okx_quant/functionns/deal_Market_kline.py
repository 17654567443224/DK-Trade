from decimal import Decimal
class MarketData:
    def __init__(self, ts, open_price, high_price, low_price, close_price, confirm):
        self.ts = int(ts)
        self.open_price = Decimal(open_price)
        self.high_price = Decimal(high_price)
        self.low_price = Decimal(low_price)
        self.close_price = Decimal(close_price)
        self.confirm = bool(int(confirm))

def encapsulate_data(data):
    encapsulated_data = []
    for item in data:
        encapsulated_data.append(MarketData(*item))
    return encapsulated_data