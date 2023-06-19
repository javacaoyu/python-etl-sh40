# coding:utf8
"""
1. 创建库`test_sh40`
2. 创建表`test`列信息：`in int, name varchar(255)`
3. 执行插入操作，插入100条数据，通过手动提交的方式
4. 执行SQL查询，查询出全部的name信息，封装到list内
"""
import uuid

import pymysql

# 1. conn对象
conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    charset='UTF8'          # 注意是UTF8不是UTF-8
)

# 2. 获取cursor
cursor = conn.cursor()

# 3. create database 和 table
cursor.execute("CREATE DATABASE test_sh40 CHARSET UTF8")
conn.select_db("test_sh40")
cursor.execute("USE test_sh40")

cursor.execute("CREATE TABLE test(id int, name varchar(255))")

# 4. insert
for i in range(1, 100):
    sql = f"INSERT INTO test VALUES({i}, '{uuid.uuid4()}')"
    cursor.execute(sql)

conn.commit()

# 5. query
cursor.execute("SELECT name FROM test")
result = cursor.fetchall()
# ( (name, ), (), ...)
names = []
for r in result:
    names.append(r[0])

print(names)

conn.close()
