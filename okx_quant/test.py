import multiprocessing
import time
import random

class Producer:
    """生产者类"""
    def __init__(self):
        self.queue = multiprocessing.Queue()  # 用于存储数据的队列
        self.process = multiprocessing.Process(target=self._run, daemon=True)

    def start(self):
        """启动生产者进程"""
        self.process.start()

    def _run(self):
        """生产者进程主循环"""
        while True:
            new_data = random.randint(1, 100)
            self.queue.put(new_data)
            print(f"[生产者] 生产数据: {new_data}")
            time.sleep(0.5)

    def get_queue(self):
        """获取队列"""
        return self.queue


class ConsumerManager:
    """消费者管理器，支持动态增删消费者"""
    def __init__(self, queue):
        self.queue = queue  # 共享队列
        self.consumers = []  # 存储消费者进程
        self.lock = multiprocessing.Lock()  # 进程安全锁

    def add_consumer(self):
        """添加消费者"""
        with self.lock:
            process = multiprocessing.Process(target=self._consumer_task, args=(self.queue,), daemon=True)
            process.start()
            self.consumers.append(process)
            print(f"[管理器] 添加消费者，当前消费者数量: {len(self.consumers)}")

    def remove_consumer(self):
        """移除一个消费者"""
        with self.lock:
            if self.consumers:
                process = self.consumers.pop()
                process.terminate()  # 强制终止消费者进程
                print(f"[管理器] 移除消费者，当前消费者数量: {len(self.consumers)}")

    @staticmethod
    def _consumer_task(queue):
        """消费者任务，循环消费数据"""
        while True:
            try:
                data = queue.get(timeout=2)  # 超时避免进程卡死
                print(f"[消费者] 消费数据: {data}")
            except:
                pass  # 允许队列为空时不报错

class Test:
    def run(self, count):
        for i in range(0, count):
            manager = ConsumerManager(producer.get_queue())

            # 模拟动态增减消费者
            time.sleep(2)
            manager.add_consumer()


if __name__ == "__main__":
    producer = Producer()
    producer.start()
    test = Test()
    test.run(5)


