# coding:utf8
"""
订单的业务服务代码

完成数据采集 -> MYSQL
订单服务类映射的就是：采集数据采集 -> MYSQL
"""
import os

from config import project_config, db_config
from util.mysql_util import MySQLUtil
from util import str_util, file_util, time_util, logging_util
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

        self.orders_csv_path = project_config.csv_output_root_path + \
                          "/orders_" + time_util.get_time("%Y-%m-%d_%H_%M_%S") + ".csv.tmp"
        self.orders_detail_csv_path = project_config.csv_output_root_path + \
                                 "/orders_detail_" + time_util.get_time("%Y-%m-%d_%H_%M_%S") + ".csv.tmp"
        self.logger = logging_util.get_logger()

    def start(self):
        self.logger.info("【Json订单数据采集】开启本次执行")
        # 1. 获取需要处理的文件
        files: list = self.get_need_to_process_file_list()

        if not files:
            # 无文件需要处理
            self.logger.info(f"【Json订单数据采集】本次无文件需要处理，程序退出")
            return None

        self.logger.info(f"【Json订单数据采集】本次需要采集的文件是：{files}，文件条数：{len(files)}")

        # 2. 转model对象，得到list内含的都是订单模型对象
        models_list = self.get_models_list(files)

        # 3. 写出（包含MySQL写出和CSV写出）
        self.__write(models_list)
        # 4. 记录元数据
        self.record_metadata(files)
        # 5. close
        self.metadata_mysql_util.close()
        self.target_mysql_util.close()

        self.logger.info(f"【Json订单数据采集】程序运行结束。")

    def record_metadata(self, files):
        """
        记录元数据
        :param files: 本次处理的文件列表
        :return: None
        """
        # 确认元数据表存在
        self.metadata_mysql_util.check_and_create_table(
            db=db_config.metadata_db_name,
            table_name=db_config.metadata_orders_processed_table_name,
            cols_define=db_config.metadata_orders_processed_table_create_cols_define
        )

        # 执行插入
        self.metadata_mysql_util.disable_autocommit()       # 关闭自动提交
        self.metadata_mysql_util.conn.begin()               # 开启事务
        try:
            for path in files:
                sql = f"INSERT INTO {db_config.metadata_orders_processed_table_name} VALUES(" \
                      f"NULL, '{path}', '{time_util.get_time()}')"
                self.metadata_mysql_util.execute(db_config.metadata_db_name, sql)
        except Exception as e:
            # 如果在企业中，这种类型的错误，可能会直接调用工具代码直接发邮件、或发短信
            self.logger.critical("元数据记录失败，请立即检查")
            self.metadata_mysql_util.conn.rollback()        # 回滚事务
            raise e

        self.metadata_mysql_util.conn.commit()              # 提交事务
        self.logger.info(f"【Json订单数据采集】本次处理的文件：{files}已经处理完成，并完成元数据记录。")

    def __write(self, models_list):
        # 1. to mysql
        # 开启事务
        self.target_mysql_util.conn.begin()     # 开启事务
        try:
            self.__write_to_mysql(models_list)
            self.__write_to_csv(models_list)
        except Exception as e:
            # 如果有异常，mysql回退，csv不改名
            self.target_mysql_util.conn.rollback()  # 回滚
            raise e

        # 没有异常
        # mysql 提交
        self.target_mysql_util.conn.commit()        # 提交
        # csv改名
        file_util.change_file_suffix(self.orders_csv_path, target_suffix="", origin_suffix=".tmp")
        file_util.change_file_suffix(self.orders_detail_csv_path, target_suffix="", origin_suffix=".tmp")

    def __write_to_csv(self, models_list):

        # 获取写文件对象
        orders_csv_writer = open(self.orders_csv_path, 'w', encoding="UTF-8")
        orders_detail_csv_writer = open(self.orders_detail_csv_path, 'w', encoding="UTF-8")

        # 写出csv标头
        orders_csv_writer.write(OrdersModel.get_csv_header())
        orders_csv_writer.write("\n")
        orders_detail_csv_writer.write(OrdersDetailModel.get_csv_header())
        orders_detail_csv_writer.write("\n")

        orders_detail_counter = 0
        for model in models_list:
            csv_line = model.to_csv()           # 订单 to csv
            orders_csv_writer.write(csv_line)
            orders_csv_writer.write("\n")
            for detail_model in model.orders_detail_model_list:
                csv_line = detail_model.to_csv()  # 订单详情 to csv
                orders_detail_csv_writer.write(csv_line)
                orders_detail_csv_writer.write("\n")
                orders_detail_counter += 1

        orders_csv_writer.close()
        orders_detail_csv_writer.close()
        self.logger.info(f"【Json订单数据采集】写出订单数据到CSV文件：{self.orders_csv_path}, 条数：{len(models_list)}, "
                         f"写出订单详情数据到CSV文件：{self.orders_detail_csv_path}, 条数：{orders_detail_counter}")

    def __write_to_mysql(self, models_list):
        """
        将模型list的内容，写入MySQL数据库(订单表和订单详情表）
        :return: None
        """
        # 如果订单表不存在，提前创建
        self.target_mysql_util.check_and_create_table(
            db=db_config.target_db_name,
            table_name=db_config.target_orders_table_name,
            cols_define=db_config.target_orders_table_cols_define
        )
        # 如果订单详情表不存在，提前创建
        self.target_mysql_util.check_and_create_table(
            db=db_config.target_db_name,
            table_name=db_config.target_orders_detail_table_name,
            cols_define=db_config.target_orders_detail_table_cols_define
        )

        # 关闭自动提交，走批量执行
        self.target_mysql_util.disable_autocommit()

        orders_detail_counter = 0
        for model in models_list:
            sql = model.generate_insert_sql()       # 订单表的插入语句
            self.target_mysql_util.execute(db_config.target_db_name, sql)
            for detail_model in model.orders_detail_model_list:
                sql = detail_model.generate_insert_sql()    # 订单详情表的插入语句
                self.target_mysql_util.execute(db_config.target_db_name, sql)
                orders_detail_counter += 1

        self.logger.info(f"【Json订单数据采集】本次即将向数据库提交，"
                         f"orders表：{len(models_list)}条，orders_detail表：{orders_detail_counter}条。")

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
        all_files_list = file_util.get_files_list(files_dir, recursion=True)

        # 4. 对比找出需要处理的
        need_to_processed_file_list = file_util.get_new_by_two_list_compare(
            all_files_list,
            processed_list
        )

        return need_to_processed_file_list
