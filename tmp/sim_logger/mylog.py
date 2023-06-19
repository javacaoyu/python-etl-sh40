"""
CRITICAL = 50
ERROR = 40
WARNING = 30
INFO = 20
DEBUG = 10
NOTSET = 0
"""
from handler import MyFileHandler
from formatter import Formatter
class mylog:

    def __init__(self):
        self.handler = None
        self.level = 30

    def setLevel(self, level):
        self.level = level

    def addHandler(self, handler):
        self.handler = handler

    def info(self, msg):
        if self.level <= 20:
            self.handler.output(msg, 'info')

    def error(self, msg):
        if self.level <= 40:
            self.handler.output(msg, 'error')

    def warning(self, msg):
        if self.level <= 30:
            self.handler.output(msg, 'warning')


logger = mylog()
logger.setLevel(20)

file_handler = MyFileHandler("E:\\test.log")
fmt = Formatter(3)
file_handler.setFormatter(fmt)

logger.addHandler(file_handler)

logger.info("我是info信息")
logger.error("集群炸了")



