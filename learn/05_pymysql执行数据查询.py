# coding:utf8
"""
简单演示pymysql库的基本使用 - 数据查询
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

cursor.execute("SELECT * FROM test")
result = cursor.fetchall()      # 取到全部查询结果
print(result)
# 查询结果的格式是：元组套元组，即( (), ()  )
# 外层元组是全部数据的封装
# 内层元组，每一个内层元组就是一条结果的封装。内部的元素就是一个个的列
print(result[0][1])

# 3. 关闭链接
conn.close()
