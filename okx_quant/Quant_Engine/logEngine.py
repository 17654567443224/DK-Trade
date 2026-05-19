import logging
import os
from datetime import datetime

class DuplicateFilter(logging.Filter):
    """
    过滤重复的日志消息
    """
    def __init__(self):
        super().__init__()
        self.last_log = None
        
    def filter(self, record):
        # 获取当前日志记录的消息
        current_log = record.getMessage()
        
        # 如果消息与上一条相同，则不记录
        if current_log == self.last_log:
            return False
            
        # 更新上一条日志并允许记录当前消息
        self.last_log = current_log
        return True

class logEngine:
    """
    日志引擎，用于记录系统日志
    
    参数说明：
    - log_name: 日志文件名前缀
    """
    
    def __init__(self, log_name="quant_engine"):
        self.log_name = log_name
        self.log_dir = "logs"
        
        # 确保日志目录存在
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
            
        # 构建日志文件路径
        log_date = datetime.now().strftime("%Y%m%d")
        self.log_path = os.path.join(self.log_dir, f"{self.log_name}_{log_date}.log")
        
        # 创建重复过滤器
        self.duplicate_filter = DuplicateFilter()
        
    def create_logger(self):
        """
        创建并返回一个logger对象，带有重复消息过滤功能
        """
        # 创建logger对象
        logger = logging.getLogger(self.log_name)
        logger.setLevel(logging.DEBUG)
        
        # 检查是否已有handler，避免重复添加
        if logger.handlers:
            return logger
            
        # 创建文件处理器
        file_handler = logging.FileHandler(self.log_path)
        file_handler.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)
        
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加重复过滤器
        logger.addFilter(self.duplicate_filter)
        
        # 添加处理器到logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
