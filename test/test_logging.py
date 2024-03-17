import logging

class SpecificStringFilter(logging.Filter):
    def __init__(self, specific_string):
        super().__init__()
        self.specific_string = specific_string

    def filter(self, record):
        return self.specific_string not in record.getMessage()

# 创建一个 logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# 创建一个 console handler，并设置级别为 debug
ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# 创建一个 filter 实例
specific_string = "httpx.RemoteProtocolError: Server disconnected without sending a response."
my_filter = SpecificStringFilter(specific_string)

# 将 filter 添加到 handler
ch.addFilter(my_filter)

# 将 handler 添加到 logger
logger.addHandler(ch)

# 测试日志消息
logger.debug("This is a debug message.")
logger.error("This message will be ignored: ignore me.httpx.RemoteProtocolError: Server disconnected without sending a response.")
logger.info("Another info message.")