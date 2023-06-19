# coding:utf8
"""
简单演示pymysql库的基本使用 - 链接到mysql数据库
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

# 2. 验证MySQL链接
mysql_info = conn.get_server_info()
print(mysql_info)

# 3. 关闭链接
conn.close()
