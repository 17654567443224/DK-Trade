import datetime
from decimal import Decimal

class kline_data:
    def __init__(self, mode):
        self.mode = mode
        self.old_price = None
        self.old_time = None


    async def mark_data_percentage(self, data, interval, percentage=None):  # 市价百分比
        if data != None:
            mark_price = Decimal(data[0]['markPx'])
            ts = data[0]['ts']
            ts = int(int(ts)/1000)
            # 使用 timestamp 创建 datetime 对象
            # dt = datetime.datetime.fromtimestamp(int(ts) / 1000)
            # 格式化输出时间
            # formatted_time = dt.strftime('%S')
            # print(formatted_time, mark_price)  # 输出: 2023-05-18 16:41:07 1827.54
            if interval:
                if self.old_price == None or self.old_time==None:
                   self.old_price = mark_price
                   self.old_time = ts
                   # print(self.old_time)
                   return
                while (ts - self.old_time)==interval:
                    pt = (mark_price - self.old_price)/self.old_price
                    if percentage >0 and pt >= percentage:
                        return pt
                    elif percentage <0 and pt <= percentage:
                        return pt
                    # print(pt)
                    self.old_time = ts

    async def mark_data_diff(self,data, interval, diff=None):  # 市价差价
        if data != None:
            mark_price = Decimal(data[0]['markPx'])
            ts = data[0]['ts']
            ts = int(int(ts) / 1000)
            if interval:
                if self.old_price == None or self.old_time == None:
                    self.old_price = mark_price
                    self.old_time = ts
                    # print(self.old_time)
                    return
                while (ts - self.old_time) == interval:
                    df = mark_price - self.old_price
                    if diff >0 and df >= diff:
                        return df
                    elif diff <0 and df <= diff:
                        return df

                    # print(df)
                    # print(diff, datetime.datetime.fromtimestamp(ts))
                    self.old_time = ts

    async def bar_data_percentage(self, data, percentage):  # kline 百分比
        if data != None:
            open_price = Decimal(data[0][1])
            high_price = Decimal(data[0][2])
            low_price = Decimal(data[0][3])
            close_price = Decimal(data[0][4])
            final = data[0][8]
            if percentage > 0 and (high_price-low_price)/open_price >= percentage:
                return (high_price-low_price)/open_price
            elif percentage < 0 and (high_price-low_price)/open_price <= percentage:
                return (high_price-low_price)/open_price

    async def bar_data_diff(self, data, diff):  # kline 差价
        if data != None:
            open_price = Decimal(data[0][1])
            high_price = Decimal(data[0][2])
            low_price = Decimal(data[0][3])
            close_price = Decimal(data[0][4])
            final = data[0][8]
            if diff >0 and high_price-low_price >= diff:
                return high_price-low_price
            elif diff < 0 and high_price-low_price <= diff:
                return high_price - low_price