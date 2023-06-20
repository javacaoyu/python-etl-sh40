# coding:utf8
"""
MySQL工具类的单元测试
切记！切记！切记：
- 单元测试连接数据库一般单独找一个数据库实例或者单独创建一个库用
- 单元测试千万不要连接生产（正式应用的）数据库实例
"""
from unittest import TestCase
from util.mysql_util import MySQLUtil
import pymysql


class TestMySQLUtil(TestCase):

    def setUp(self) -> None:
        """执行任何测试方法前，先跑它"""
        self.mysql_util = MySQLUtil(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            charset='UTF8'
        )
        self.mysql_util.conn.select_db("unittest")

    def test_query(self):
        # 准备环境一致，假设查询的表是：test_query
        self.mysql_util.execute('unittest', 'drop table if exists test_query')

        # 创建新表
        self.mysql_util.execute('unittest', 'create table test_query(id int, name varchar(10))')
        # 插入测试数据
        self.mysql_util.execute_force_commit('unittest', "insert into test_query values(1, '周杰轮')")
        r = self.mysql_util.query("unittest", "select * from test_query")
        excepted = ((1, '周杰轮'), )
        self.assertEqual(excepted, r)

    def tearDown(self) -> None:
        """任何测试方法结束后，会跑它"""
        # 清理表
        self.mysql_util.execute('unittest', 'drop table if exists test_query')

        self.mysql_util.close()

