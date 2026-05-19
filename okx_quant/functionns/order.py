import okx.Account_api as Account
from utils import deal_message
import time
class Order:
    def __init__(self):
        self.accountAPI = Account.AccountAPI()

    def get_order_count(self, order_count):  # {"msg":"APIKey does not match current environment.","code":"50101"}, 401
        res: list
        res = deal_message(self.accountAPI.get_positions_history())
        if order_count >= len(res):
            return res
        return res[:order_count]

    def get_order_time(self, order_time):  # 时间单位：min
        current_timestamp = time.time()
        res_time = current_timestamp + order_time * 60
        res: list
        res = deal_message(self.accountAPI.get_positions_history())
        start_time = int(res[0]['uTime'])
        print(start_time)
        count = 0
        for i in res:
            if start_time - int(i['uTime']) > res_time:
                count = count + 1
                break
        return res[:count]

    def default_order(self):
        return self.get_order_count(1)

if __name__ == '__main__':
    asd = Order()

    print(asd.default_order())