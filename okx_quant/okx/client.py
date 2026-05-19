import requests
import json
from functionns import setting
from . import consts as c, utils, exceptions
import logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

class Client(object):

    def __init__(self, use_server_time=False, proxy = setting.proxies):
        self.API_KEY = setting.api_key
        self.API_SECRET_KEY = setting.secret_key
        self.PASSPHRASE = setting.passphrase
        self.use_server_time = use_server_time
        self.flag = setting.flag
        self.proxy = proxy

    def _request(self, method, request_path, params):
        if method == c.GET:
            request_path = request_path + utils.parse_params_to_str(params)
        # url
        url = c.API_URL + request_path

        timestamp = utils.get_timestamp()

        # sign & header
        if self.use_server_time:
            timestamp = self._get_timestamp()

        body = json.dumps(params) if method == c.POST else ""

        sign = utils.sign(utils.pre_hash(timestamp, method, request_path, str(body)), self.API_SECRET_KEY)
        header = utils.get_header(self.API_KEY, sign, timestamp, self.PASSPHRASE, self.flag)

        # send request
        response = None

        # print("url:", url)
        # # print("headers:", header)
        # print("body:", body)
        if method == c.GET:
            response = requests.get(url, headers=header, proxies=self.proxy)
        elif method == c.POST:
            response = requests.post(url, data=body, headers=header, proxies=self.proxy)

        # exception handle
        # print(response.headers)
        # 报错
        if not str(response.status_code).startswith('2'):
            response_text = response.text
            status_code = response.status_code
            if status_code != 429:
                # 输出到日志文件
                logging.error(f'{response_text}, {status_code}')
            # print(url,response,body)
            raise exceptions.OkxAPIException(response)

        return response.json()

    def _request_without_params(self, method, request_path):
        return self._request(method, request_path, {})

    def _request_with_params(self, method, request_path, params):
        return self._request(method, request_path, params)

    def _get_timestamp(self):
        url = c.API_URL + c.SERVER_TIMESTAMP_URL
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['data'][0]['ts']
        else:
            return ""
