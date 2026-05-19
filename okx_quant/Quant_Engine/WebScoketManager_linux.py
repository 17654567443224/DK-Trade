import os
from multiprocessing import Process, Queue, Manager
import json
import asyncio
import websockets
import logging
import logging.handlers
class WebSocketProducer:
    def __init__(self, name, url: str, sub_param, timeout=25):
        self.connectName = name
        self.url = url
        self.sub_param = sub_param
        self.timeout = timeout
        self.manager = Manager()
        self.queues = self.manager.list()  # 共享队列列表
        self.log_queue = Queue()  # 日志专用队列
        self.running = False
        self._init_logger()

    def _init_logger(self):
        # 配置日志进程
        self.logger = logging.getLogger(self.connectName)
        self.logger.setLevel(logging.INFO)
        handler = logging.handlers.QueueHandler(self.log_queue)
        self.logger.addHandler(handler)

        # 启动日志写入进程
        self.log_process = Process(target=self._log_writer)
        self.log_process.start()

    def _log_writer(self):
        # 确保日志目录存在
        log_dir = os.path.dirname(f'{self.connectName}_ws.log')
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        file_handler = logging.FileHandler(f'{self.connectName}_ws.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        while True:
            try:
                record = self.log_queue.get()
                if record is None:
                    break
                logger = logging.getLogger(record.name)
                logger.handle(record)
            except Exception as e:
                print(f"Log writer error: {e}")

    def start(self):
        self.running = True
        process = Process(target=self.run_websocket)
        process.start()

    def run_websocket(self):
        asyncio.run(self.start_websocket())

    async def start_websocket(self):
        reconnect_delay = 1
        while self.running:
            try:
                async with websockets.connect(
                        self.url,
                        ping_interval=20,
                        close_timeout=self.timeout
                ) as ws:
                    reconnect_delay = 1
                    await ws.send(json.dumps(self.sub_param))
                    while self.running:
                        try:
                            message = await asyncio.wait_for(ws.recv(), timeout=self.timeout)
                            await self.broadcast_message(json.loads(message))
                        except (asyncio.TimeoutError, websockets.ConnectionClosed) as e:
                            self.logger.error(f"Connection error: {e}, reconnecting...")
                            break
            except Exception as e:
                self.logger.error(f"Connect failed: {e}, retry in {reconnect_delay}s")
                await asyncio.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, 30)

    async def broadcast_message(self, message):
        loop = asyncio.get_event_loop()
        for queue in self.queues:
            await loop.run_in_executor(None, queue.put, message)

    def regiest_consumer(self):
        queue = Queue()
        self.queues.append(queue)
        return queue

    def remove_consumer(self, queue: Queue):
        if queue in self.queues:
            self.queues.remove(queue)

    def stop(self):
        self.running = False
        self.log_queue.put(None)
        self.log_process.join()