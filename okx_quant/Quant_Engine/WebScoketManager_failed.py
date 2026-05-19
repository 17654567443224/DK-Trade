import json
import asyncio
import websockets
import multiprocessing

class WebSocketProducer:
    def __init__(self, name, url: str, sub_param=None, timeout=25):
        self.connectName = name
        self.url = url
        self.manager = multiprocessing.Manager()
        self.sub_param = self.manager.dict()  # 用共享字典存储 sub_param
        self.timeout = timeout
        self.queues = []  # 存储 Queue，不使用 Manager.list()
        self.running = multiprocessing.Value('b', True)  # 共享运行标志
        self.process = multiprocessing.Process(target=self._run_websocket, daemon=True)

    def start(self):
        self.process.start()

    def update_sub_param(self, sub_param):
        """更新订阅参数"""
        self.sub_param.clear()
        self.sub_param.update(sub_param)

    def _run_websocket(self):
        asyncio.run(self.start_websocket())

    async def start_websocket(self):
        reconnect_delay = 1
        while self.running.value:  # 使用共享变量判断是否继续运行
            try:
                async with websockets.connect(
                        self.url
                ) as ws:
                    reconnect_delay = 1
                    await ws.send(json.dumps(self.sub_param))
                    while self.running.value:
                        try:
                            message = await asyncio.wait_for(ws.recv(), timeout=self.timeout)
                            await self.broadcast_message(json.loads(message))
                        except (asyncio.TimeoutError, websockets.ConnectionClosed) as e:
                            print(f"[WebSocketProducer] 连接异常: {e}")
                            break
            except Exception as e:
                print(f"[WebSocketProducer] 重连异常: {e}")
                await asyncio.sleep(reconnect_delay)
                reconnect_delay = min(reconnect_delay * 2, 30)

    async def broadcast_message(self, message):
        """将数据推送到所有注册的消费者"""
        for queue in self.queues:
            try:
                queue.put_nowait(message)  # 直接放入队列，避免阻塞
            except Exception as e:
                print(f"[WebSocketProducer] 消息推送失败: {e}")

    def register_consumer(self):
        """动态注册消费者"""
        queue = multiprocessing.Queue()
        self.queues.append(queue)
        return queue

    def remove_consumer(self, queue):
        """动态移除消费者"""
        for q in self.queues:
            if q._id == queue._id:  # 确保是同一个队列
                self.queues.remove(q)
                print(f"[WebSocketProducer] 移除消费者: {queue}")
                return
        print(f"[WebSocketProducer] 未找到要移除的消费者: {queue}")

    def stop(self):
        """停止生产者"""
        self.running.value = False  # 关闭共享变量
        self.process.terminate()
        self.process.join()  # 等待子进程退出
        print("[WebSocketProducer] 已停止")


# ========== 测试代码 ==========
if __name__ == "__main__":
    producer = WebSocketProducer("test", "wss://example.com/socket", sub_param={"action": "subscribe"})
    producer.start()

    # 动态注册消费者
    queue1 = producer.register_consumer()
    queue2 = producer.register_consumer()

    def consumer(queue, name):
        while True:
            data = queue.get()
            print(f"[{name}] 消费者收到数据: {data}")

    # 启动消费者
    consumer_process1 = multiprocessing.Process(target=consumer, args=(queue1, "Consumer 1"), daemon=True)
    consumer_process2 = multiprocessing.Process(target=consumer, args=(queue2, "Consumer 2"), daemon=True)
    consumer_process1.start()
    consumer_process2.start()

    # 模拟运行一段时间后，停止一个消费者
    import time
    time.sleep(5)
    producer.remove_consumer(queue1)  # 移除消费者 1

    # 让程序继续运行一段时间
    time.sleep(10)
    producer.stop()
