# coding:utf8
"""
记录日志相关的配置项
"""
import os
from util import time_util


# 日志输出的根目录在当前Python项目根目录内的logs文件夹中，全部都写入到这个文件夹
default_logger_file_root_path = f"{os.path.dirname(os.getcwd())}/logs/"
# 日志的文件名，按天来，一天一个日志文件
default_logger_file_basename = f"pyetl_{time_util.get_today()}.log"

default_logger_level = 20                                               # 默认日志级别
default_logger_file_full_path = \
    f"{default_logger_file_root_path}{default_logger_file_basename}"    # 默认日志输出位置
default_logger_formatter = \
    "%(asctime)s - [%(levelname)s] - %(filename)s[line:%(lineno)d]: %(message)s"
