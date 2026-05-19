from abc import ABC, abstractmethod
class BasePublicGateway(ABC):
    def __init__(self, exchange, url):
        self.exchange = exchange
        self.url = url

    @abstractmethod
    def get_instruments(self):
        pass

    @abstractmethod
    def query_Kline(self):
        pass

    @abstractmethod
    def subscribe(self):
        pass

class BasePrivateGateway(ABC):
    def __init__(self, ecchange, url, userId, login_data):
        self.exchange = ecchange
        self.url = url
        self.userId = userId
        self.Login_data = login_data

    @abstractmethod
    def get_account_balance(self):
        pass

    @abstractmethod
    def cancel_order(self):
        pass

    @abstractmethod
    def place_order(self):
        pass

    @abstractmethod
    def subscribe(self):
        pass

    def set_lever(self):
        pass

    def get_position_mode(self):
        pass

    def get_history_orders(self, count: int):
        pass

