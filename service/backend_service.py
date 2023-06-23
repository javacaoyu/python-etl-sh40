# coding:utf8
"""
后台日志采集核心逻辑代码
"""
from util.mysql_util import MySQLUtil
from util import file_util, logging_util
from config import db_config, project_config


class BackendService:

    def __init__(self):
        # 构建到元数据库的MySQLUtil对象，用来做数据库操作
        self.metadata_mysql_util = MySQLUtil(
            host=db_config.metadata_host,
            port=db_config.metadata_port,
            user=db_config.metadata_user,
            password=db_config.metadata_password,
            charset=db_config.metadata_charset
        )

        # 构建到目标数据库的MySQLUtil对象，用来做数据库操作
        self.target_mysql_util = MySQLUtil(
            host=db_config.target_host,
            port=db_config.target_port,
            user=db_config.target_user,
            password=db_config.target_password,
            charset=db_config.target_charset
        )

        # 构建一个日志logger对象
        self.logger = logging_util.get_logger()


    def start(self):
        # 1. 获取本次需要处理的文件列表（其中要对比元数据）
        files: list = self.get_need_to_process_file_list()
        if len(files) > 0:
            self.logger.info(f"【后台日志采集实战】本次需要处理的文件列表是：{files}")
        else:
            self.logger.info(f"【后台日志采集实战】本次无文件处理，程序退出")
            return None
        # 2. 将数据文件内容读取，转换为model的list对象

        # 3. 数据写出（写出到MySQL和CSV）

        # 4. 记录元数据
        pass


    def get_need_to_process_file_list(self):
        """
        获取本次需要处理的文件列表（其中要对比元数据）
        :return:
        """
        # 1. 检查元数据，先检查表是否存在，不存在创建
        self.metadata_mysql_util.check_and_create_table(
            db=db_config.metadata_db_name,          # 数据库名
            table_name=db_config.metadata_backend_logs_processed_table_name,
            cols_define=db_config.metadata_backend_logs_processed_table_create_cols_define,
        )

        # 2. 查询元数据的内容，找出以往的历史记录
        # processed_files = ['e:/1.txt', 'e:/2.txt', ......]
        processed_files = self.metadata_mysql_util.query_result_single_column(
            db=db_config.metadata_db_name,
            sql=f"SELECT path FROM {db_config.metadata_backend_logs_processed_table_name}"
        )

        # 3. 读取数据文件夹，找出数据文件列表
        all_files = file_util.get_files_list(project_config.backend_file_data_path, recursion=True)

        # 4. 两者对比，找出新的未处理的文件列表
        return file_util.get_new_by_two_list_compare(big_list=all_files, small_list=processed_files)






