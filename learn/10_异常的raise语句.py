# coding:utf8
"""
演示异常的raise语句
"""

import pymysql
import pymysql.err
conn = pymysql.Connect(
    host='123',
    port=3306,
    user='root',
    password='123456',
    charset='UTF8'
)

print(conn.get_server_info())
