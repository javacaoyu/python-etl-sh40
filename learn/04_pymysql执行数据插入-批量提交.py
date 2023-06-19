# coding:utf8
"""
简单演示pymysql库的基本使用 - 创建数据库和表
"""
import uuid

import pymysql


# 1. 需要先链接到MySQL上，获取pymysql.Connection类对象
conn: pymysql.Connection = pymysql.Connect(
    host='localhost',           # MySQL主机（IP）
    port=3306,                  # MySQL端口
    user='root',                # 账户名
    password='123456',          # 密码
    charset='UTF8',             # 编码集
    autocommit=False            # 自动确认（自动提交）默认关闭
)

# 2. 获取游标对象来执行sql语句
cursor = conn.cursor()
conn.select_db("test_sh40")     # 切记，要先选择数据库
for i in range(0, 1000):
    sql = f"INSERT INTO test VALUES({i}, '{uuid.uuid1()}')"
    cursor.execute(sql)

conn.commit()

# 3. 关闭链接
conn.close()
