# coding:utf8
"""
订单的业务服务代码

完成数据采集 -> MYSQL
订单服务类映射的就是：采集数据采集 -> MYSQL
"""
import os

from config import project_config, db_config
from util.mysql_util import MySQLUtil
from util import str_util, file_util
from model.orders_model import OrdersModel, OrdersDetailModel


class OrdersService:

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

    def start(self):
        # 1. 获取需要处理的文件
        files: list = self.get_need_to_process_file_list()

        # 2. 转model对象，得到list内含的都是订单模型对象
        models_list = self.get_models_list(files)
        # # 3. 转insert sql插入
        # mysql_xxx(models_list)
        # # 4. 写出csv
        # csv_xxx(models_list)
        # # 5. 记录元数据
        # metadata_xxx(files)

    def get_models_list(self, files):
        """
        读取文件，转换成订单模型，封装到list内
        :param files: list记录文件路径
        :return: list（内函OrdersModel对象）
        """
        models_list = []
        for path in files:
            for line in open(path, 'r', encoding="UTF-8").readlines():
                # 去除尾部换行符
                line = line.strip()
                model = OrdersModel(line)
                models_list.append(model)

        return models_list

    def get_need_to_process_file_list(
            self,
            files_dir=project_config.orders_json_file_data_path,
            db=db_config.metadata_db_name,
            metadata_table_name=db_config.metadata_orders_processed_table_name
    ):
        # 1. 判断元数据表是否存在
        self.metadata_mysql_util.check_and_create_table(
            db,
            metadata_table_name,
            db_config.metadata_orders_processed_table_create_cols_define
        )

        # 2. 查询元数据
        processed_list = self.metadata_mysql_util.query_result_single_column(
            db,
            f"SELECT path FROM {metadata_table_name}"
        )

        # 3. 读取文件列表
        all_files_list = file_util.get_files_list(files_dir)

        # 4. 对比找出需要处理的
        need_to_processed_file_list = file_util.get_new_by_two_list_compare(
            all_files_list,
            processed_list
        )

        return need_to_processed_file_list
