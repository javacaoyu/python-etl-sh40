# coding:utf8
"""
MySQL工具类的单元测试
切记！切记！切记：
- 单元测试连接数据库一般单独找一个数据库实例或者单独创建一个库用
- 单元测试千万不要连接生产（正式应用的）数据库实例
"""
from unittest import TestCase
from util.mysql_util import MySQLUtil
from config import db_config


class TestMySQLUtil(TestCase):

    def setUp(self) -> None:
        """执行任何测试方法前，先跑它"""
        self.mysql_util = MySQLUtil(
            host=db_config.unittest_host,
            port=db_config.unittest_port,
            user=db_config.unittest_user,
            password=db_config.unittest_password,
            charset=db_config.unittest_charset
        )
        self.mysql_util.conn.select_db(db_config.unittest_db_name)

    def test_query(self):
        # 准备环境一致，假设查询的表是：test_query
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_query')

        # 创建新表
        self.mysql_util.execute(db_config.unittest_db_name, 'create table test_query(id int, name varchar(10))')
        # 插入测试数据
        self.mysql_util.execute_force_commit(db_config.unittest_db_name, "insert into test_query values(1, '周杰轮')")
        r = self.mysql_util.query(db_config.unittest_db_name, "select * from test_query")
        excepted = ((1, '周杰轮'), )
        self.assertEqual(excepted, r)

    def test_check_table_exists(self):
        # 准备环境一致，假设判断的表是：test_exists
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_exists')

        # 当前表不存在
        r = self.mysql_util.check_table_exists(db_config.unittest_db_name, 'test_exists')
        self.assertFalse(r)

        # 创建新表
        self.mysql_util.execute(db_config.unittest_db_name, 'create table test_exists(id int)')

        r = self.mysql_util.check_table_exists(db_config.unittest_db_name, 'test_exists')
        self.assertTrue(r)

    def test_check_and_create_table(self):
        # 准备环境一致，假设判断的表是：test_exists_and_create
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_exists_and_create')

        # 表不存在，要走创建，返回值应该是True
        r = self.mysql_util.check_and_create_table(db_config.unittest_db_name, 'test_exists_and_create', 'id int')
        self.assertTrue(r)
        r = self.mysql_util.check_table_exists(db_config.unittest_db_name, 'test_exists_and_create')  # 再次检查是否存在
        self.assertTrue(r)

        # 表存在，结果应当是False
        r = self.mysql_util.check_and_create_table(db_config.unittest_db_name, 'test_exists_and_create', 'id int')
        self.assertFalse(r)

    def test_execute(self):
        # 准备测试环境, 表：test_execute
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_execute')    # 先删除
        # 再创建
        self.mysql_util.check_and_create_table(db_config.unittest_db_name, 'test_execute', 'id int, name varchar(10)')
        # 执行insert，自动提交为False
        self.mysql_util.conn.autocommit(False)
        self.mysql_util.execute(db_config.unittest_db_name, "insert into test_execute values(1, '周杰轮')")
        # 为了验证结果正确，应当断开链接重连，避免从链接对象的缓存（缓冲区）查到缓存的未提交的数据
        self.mysql_util.conn.close()        # 断开，清空缓存如果缓存内有数据自动提交是True就提交，是False就丢弃
        self.mysql_util.conn.connect()      # 连接

        r = self.mysql_util.query(db_config.unittest_db_name, 'select * from test_execute')
        self.assertEqual(len(r), 0)

        # 执行insert，自动提交为True
        self.mysql_util.conn.autocommit(True)
        self.mysql_util.execute(db_config.unittest_db_name, "insert into test_execute values(1, '周杰轮')")
        # 为了验证结果正确，应当断开链接重连
        self.mysql_util.conn.close()  # 断开
        self.mysql_util.conn.connect()  # 连接

        r = self.mysql_util.query(db_config.unittest_db_name, 'select * from test_execute')
        self.assertEqual(((1, '周杰轮'),), r)

    def test_execute_force_commit(self):
        # 准备测试环境, 表：test_execute_force_commit
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_execute_force_commit')  # 先删除
        # 再创建
        self.mysql_util.check_and_create_table(db_config.unittest_db_name, 'test_execute_force_commit', 'id int, name varchar(10)')
        # 执行insert，自动提交为False
        self.mysql_util.conn.autocommit(False)      # 主动设置为False，验证是否能100%提交
        self.mysql_util.execute_force_commit(db_config.unittest_db_name, "insert into test_execute_force_commit values(1, '周杰轮')")

        # 为了验证结果正确，应当断开链接重连
        self.mysql_util.conn.close()  # 断开
        self.mysql_util.conn.connect()  # 连接

        r = self.mysql_util.query(db_config.unittest_db_name, 'select * from test_execute_force_commit')
        self.assertEqual(((1, '周杰轮'),), r)

    def tearDown(self) -> None:
        """任何测试方法结束后，会跑它"""
        # 清理表
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_query')
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_exists')
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_exists_and_create')
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_execute')
        self.mysql_util.execute(db_config.unittest_db_name, 'drop table if exists test_execute_force_commit')

        self.mysql_util.close()
