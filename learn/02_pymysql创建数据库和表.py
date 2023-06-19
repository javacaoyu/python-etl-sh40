# coding:utf8
"""
简单演示pymysql库的基本使用 - 创建数据库和表
"""
import pymysql


# 1. 需要先链接到MySQL上，获取pymysql.Connection类对象
conn: pymysql.Connection = pymysql.Connect(
    host='localhost',           # MySQL主机（IP）
    port=3306,                  # MySQL端口
    user='root',                # 账户名
    password='123456',          # 密码
    charset='UTF8'              # 编码集
)

# 2. 如果要执行SQL，需要拿到一个cursor（游标）对象
# 具体的SQL执行 ，是基于游标对象执行的。
# cursor对象就是具体干活的（小弟）
# 关系： conn链接对象，只是确保网络连接的，不干重活
# 具体干活的是cursor对象，可以通过链接对象调用cursor()方法获取
# 也就是conn是老大，不干活，干活需要小弟，通过cursor()方法可以创建小弟
cursor = conn.cursor()

# 3. 执行SQL
# 执行数据库创建
cursor.execute("CREATE DATABASE test_sh40 CHARSET UTF8")
# 凡是SQL，都是通过cursor.execute()执行的。

# 执行表创建
# 选择要操作的数据库
conn.select_db("test_sh40")             # 选择数据库功能由conn对象提供
cursor.execute("CREATE TABLE test(id int, name varchar(255))")
# 4. 关闭链接
conn.close()
