# coding:utf8
"""
条码数据采集核心业务逻辑代码
"""
from util.mysql_util import MySQLUtil
from config import db_config, project_config
from model.barcode_model import BarcodeModel
from util import logging_util, time_util, file_util

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

        self.logger = logging_util.get_logger()

        self.barcode_csv_path = project_config.csv_output_root_path + \
                               "/barcode_" + time_util.get_time("%Y-%m-%d_%H_%M_%S") + ".csv.tmp"

    def start(self):
        # 1. 查询元数据库获得上一次的时间
        last_update = self.get_last_update()
        # 2. 组装SQL 语句 查询数据源表
        result = self.query_source_data(last_update)
        # 3. 封装查询结果到模型list
        model_list = self.get_model_list(result)
        # 4. 写出MySQL和CSV
        self.__write(model_list)
        # 5. 记录元数据

    def __write(self, model_list: list):

        self.target_mysql_util.disable_autocommit()         # 关闭自动提交
        self.target_mysql_util.conn.begin()                 # 开启事务
        try:
            self.__write_to_mysql(model_list)
            self.__write_to_csv(model_list)
        except Exception as e:
            self.target_mysql_util.conn.rollback()          # 出错误回滚
            self.logger.error(f"【MySQL数据采集】写出数据到MySQL或CSV出错，回滚，程序退出。")
            raise e

        self.target_mysql_util.conn.commit()                # 提交

        # csv改名
        file_util.change_file_suffix(self.barcode_csv_path, "", ".tmp")

    def __write_to_mysql(self, model_list):
        for model in model_list:
            sql = model.generate_insert_sql()
            self.target_mysql_util.execute(db_config.target_db_name, sql)

    def __write_to_csv(self, model_list):
        # 1. open
        csv_writer = open(self.barcode_csv_path, 'w', encoding="UTF-8")

        # 2. 写header
        csv_writer.write(BarcodeModel.get_csv_header())
        csv_writer.write("\n")

        # 3. for 写数据
        for model in model_list:
            csv_writer.write(model.to_csv())
            csv_writer.write("\n")

        # 4. close
        csv_writer.close()

    def get_model_list(self, query_result):
        model_list = []
        for line_tuple in query_result:
            model = BarcodeModel(line_tuple)
            model_list.append(model)

        return model_list

    def query_source_data(self, last_update):
        sql = None
        if not last_update:
            sql = f"SELECT * FROM {db_config.source_barcode_table_name} " \
                  f"WHERE updateAt >= '{last_update}' ORDER BY updateAt"
        else:
            sql = f"SELECT * FROM {db_config.source_barcode_table_name} " \
                  f"ORDER BY updateAt"

        result = self.source_mysql_util.query(
            db=db_config.source_db_name,
            sql=sql
        )

        return result

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
