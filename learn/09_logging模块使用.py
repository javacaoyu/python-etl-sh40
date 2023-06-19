# coding:utf8
"""
logging模块的演示
"""
import logging


logger: logging.Logger = logging.getLogger("sh40_logger")
logger.setLevel(20)

file_handler = logging.FileHandler("E:\\sh40.log", 'a', 'UTF-8')

fmt = logging.Formatter("%(asctime)s - [%(levelname)s] - %(filename)s[line:%(lineno)d]: %(message)s")

file_handler.setFormatter(fmt)

logger.addHandler(file_handler)

logger.warning("测试警告")
logger.info("测试info")
logger.error("测试错误")

"""

critical 灾难级别
error 错误级别
warning 警告级别
info 普通信息
debug 啰嗦信息

logger对象默认的级别是warning，调用的方法级别低于warning的不输出。

附录:Formatter参数列表
%(name)s            Name of the logger (logging channel)
%(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                    WARNING, ERROR, CRITICAL)
%(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                    "WARNING", "ERROR", "CRITICAL")
%(pathname)s        Full pathname of the source file where the logging
                    call was issued (if available)
%(filename)s        Filename portion of pathname
%(module)s          Module (name portion of filename)
%(lineno)d          Source line number where the logging call was issued
                    (if available)
%(funcName)s        Function name
%(created)f         Time when the LogRecord was created (time.time()
                    return value)
%(asctime)s         Textual time when the LogRecord was created
%(msecs)d           Millisecond portion of the creation time
%(relativeCreated)d Time in milliseconds when the LogRecord was created,
                    relative to the time the logging module was loaded
                    (typically at application startup time)
%(thread)d          Thread ID (if available)
%(threadName)s      Thread name (if available)
%(process)d         Process ID (if available)
%(message)s         The result of record.getMessage(), computed just as
                    the record is emitted
"""