# coding:utf8
"""
条码数据采集核心业务逻辑代码
"""
from util.mysql_util import MySQLUtil
from config import db_config

class BarcodeService:

    def __init__(self):
        self.metadata_mysql_util = MySQLUtil(
            host=db_config.metadata_host,
            port=db_config.metadata_port,
            user=db_config.metadata_user,
            password=db_config.metadata_password,
            charset=db_config.metadata_charset
        )
        self.target_mysql_util = MySQLUtil(
            host=db_config.target_host,
            port=db_config.target_port,
            user=db_config.target_user,
            password=db_config.target_password,
            charset=db_config.target_charset
        )
        self.source_mysql_util = MySQLUtil(
            host=db_config.source_host,
            port=db_config.source_port,
            user=db_config.source_user,
            password=db_config.source_password,
            charset=db_config.source_charset
        )

    def start(self):
        # 1. 查询元数据库获得上一次的时间
        last_update = self.get_last_update()
        # 2. 组装SQL 语句 查询数据源表

        # 3. 封装查询结果到模型list

        # 4. 写出MySQL和CSV

        # 5. 记录元数据
        pass

    def get_last_update(self):
        """
        查询最新元数据记录的上一次采集的最大时间
        :return: 查询到返回时间，查不到返回None
        """
        # 1. 检查元数据表，不存在创建
        self.metadata_mysql_util.check_and_create_table(
            db=db_config.metadata_db_name,
            table_name=db_config.metadata_barcode_processed_table_name,
            cols_define=db_config.metadata_barcode_processed_table_create_cols_define
        )

        # 2. 查询
        result = self.metadata_mysql_util.query_result_single_column(
            db=db_config.metadata_db_name,
            sql=f"SELECT last_update FROM "
                f"{db_config.metadata_barcode_processed_table_name} "
                f"ORDER BY id DESC LIMIT 1"     # 按照主键ID降序排序取1条，找出最新的元数据记录
        )

        # 3. 准备返回
        last_update = None
        if len(result) > 0:
            # 如果有结果，结果必然是： ( ('last_update'),  )
            # 查询结果limit 1只有1条， 查询SELECT 只有1个列，所以[0][0]取出
            last_update = result[0][0]

        return last_update
