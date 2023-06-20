

import pymysql

conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    db='test',
    charset='UTF8'
)

conn.autocommit(False)

cursor = conn.cursor()
cursor.execute("INSERT INTO t VALUES(1, '拉拉拉')")

conn.close()
conn.connect()

cursor.execute("SELECT * FROM t")
print(cursor.fetchall())

conn.close()


