import json
import asyncio
import websockets
import logging
import threading
from queue import Queue

class WebSocketProducer:
    def __init__(self, name, url: str, url_ticker: str, sub_param, timeout=25):
        self.connectName = name
        self.url = url                 # K线数据的WebSocket URL
        self.url_ticker = url_ticker   # Ticker数据的WebSocket URL
        self.sub_param = sub_param     # [k线订阅参数, ticker订阅参数]
        self.timeout = timeout
        self.queues = []               # 直接用列表存储消费者队列
        self.running = False
        self.thread = None             # 线程对象

    def start(self):
        """启动 WebSocket 生产者（多线程模式）"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run_websocket, daemon=True)
            self.thread.start()

    def run_websocket(self):
        """在当前线程运行 WebSocket 任务"""
        asyncio.run(self.start_all_websockets())

    async def start_all_websockets(self):
        """同时启动多个WebSocket连接"""
        # 创建两个任务并行运行
        tasks = [
            self.start_kline_websocket(),
            self.start_ticker_websocket()
        ]
        await asyncio.gather(*tasks)

    async def start_kline_websocket(self):
        """K线数据WebSocket连接管理"""
        reconnect_delay = 1
        while self.running:
            try:
                async with websockets.connect(self.url) as ws:
                    reconnect_delay = 1
                    # 订阅K线数据
                    kline_param = {"op": "subscribe", "args": self.sub_param[0]}
                    await ws.send(json.dumps(kline_param))
                    logging.info(f"[{self.connectName}] 已连接K线WebSocket并订阅数据")
                    
                    while self.running:
                        try:
                            message = await asyncio.wait_for(ws.recv(), timeout=self.timeout)
                            await self.broadcast_message(json.loads(message))
                        except (asyncio.TimeoutError, websockets.ConnectionClosed) as e:
                            logging.warning(f"[{self.connectName}] K线WebSocket连接超时或断开: {e}")
                            break  # 重新连接
            except Exception as e:
                logging.error(f"[{self.connectName}] K线WebSocket连接异常: {e}")
                await asyncio.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, 30)

    async def start_ticker_websocket(self):
        """Ticker数据WebSocket连接管理"""
        reconnect_delay = 1
        while self.running:
            try:
                async with websockets.connect(self.url_ticker) as ws:
                    reconnect_delay = 1
                    # 订阅Ticker数据
                    ticker_param = {"op": "subscribe", "args": self.sub_param[1]}
                    await ws.send(json.dumps(ticker_param))
                    logging.info(f"[{self.connectName}] 已连接Ticker WebSocket并订阅数据")
                    
                    while self.running:
                        try:
                            message = await asyncio.wait_for(ws.recv(), timeout=self.timeout)
                            await self.broadcast_message(json.loads(message))
                        except (asyncio.TimeoutError, websockets.ConnectionClosed) as e:
                            logging.warning(f"[{self.connectName}] Ticker WebSocket连接超时或断开: {e}")
                            break  # 重新连接
            except Exception as e:
                logging.error(f"[{self.connectName}] Ticker WebSocket连接异常: {e}")
                await asyncio.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, 30)

    async def broadcast_message(self, message):
        """将消息广播给所有消费者"""
        for queue in self.queues:
            queue.put(message)  # 直接放入队列

    def register_consumer(self):
        """注册一个消费者（返回队列用于接收数据）"""
        queue = Queue()
        self.queues.append(queue)
        return queue

    def remove_consumer(self, queue: Queue):
        """移除消费者"""
        if queue in self.queues:
            self.queues.remove(queue)

    def stop(self):
        """停止 WebSocket 线程"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=3)  # 等待线程结束
