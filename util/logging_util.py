# coding:utf8
"""
日志输出相关的工具代码文件
"""
import logging
from config import logging_config


def get_logger(
        log_path=logging_config.default_logger_file_full_path,
        level=logging_config.default_logger_level,
        formatter=logging_config.default_logger_formatter):
    """
    返回一个设置好的logger对象
    :param log_path: 日志输出的文件路径，提供默认值
    :param level: 日志输出的级别，默认是INFO 20
    :param formatter: 日志显示格式，提供默认显示格式
    :return: logging.Logger 对象
    """
    # 构建logger对象
    logger = logging.getLogger("python-etl")

    if len(logger.handlers) > 0:
        return logger

    # 设置级别
    logger.setLevel(level)

    # 创建FileHandler对象
    file_handler = logging.FileHandler(
        filename=log_path,              # 日志写出的文件路径
        mode='a',                       # 模式，追加
        encoding="UTF-8"
    )

    # 创建Formatter对象
    fmt = logging.Formatter(fmt=formatter)

    # 向Handler对象设置fmt显示格式
    file_handler.setFormatter(fmt)

    # 向logger对象设置Handler
    logger.addHandler(file_handler)

    # 返回logger对象
    return logger
