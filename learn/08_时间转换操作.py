# coding:utf8
"""
演示时间转换操作
"""
import time


# 获取当前时间strftime -> str(字符串) format(格式) time，得到指定格式的时间字符串
# 20230101   2023-01-01  2023_01_01
# time.localtime()取当前时间，格式是标准的时间元组(time.struct_time(tm_year=2023, tm_mon=6, tm_mday=17, tm_hour=11, tm_min=18, tm_sec=39, tm_wday=5, tm_yday=168, tm_isdst=0))
format_str = "%Y-%m-%d"
"""
- %Y 4位格式年份
- %m 2位格式月份
- %d 2位格式日期
- %H 24小时制小时
- %M 2位格式分钟
- %S 2位格式秒
"""
current_date = time.strftime(format_str, time.localtime())
print(current_date)


# 时间戳转换
format_str = "%Y-%m-%d %H:%M:%S"
current_date = time.strftime(format_str, time.localtime(1686972236))
print(current_date)
