# coding:utf8
"""
后台日志采集实战模型类
"""
from config import db_config, project_config


class BackendLogsModel:

    def __init__(self, data_str: str):
        """
        构造方法，需要传入字符串数据
        一行数据对应一个模型类的实例对象
        :param data_str: 传入的字符串数据
        """
        arr = data_str.split("\t")

        self.log_time = arr[0]
        self.log_level = arr[1]
        self.log_module = arr[2]
        self.respond_time = arr[3]
        self.province = arr[4]
        self.city = arr[5]
        self.message = arr[6]

    def generate_insert_sql(self, table_name=db_config.target_backend_logs_table_name):
        sql = f"INSERT INTO {table_name}(id, log_time, log_level, log_module, respond_time, " \
              f"province, city, message) VALUES(" \
              f"NULL, " \
              f"'{self.log_time}', " \
              f"'{self.log_level}', " \
              f"'{self.log_module}', " \
              f"'{self.respond_time}', " \
              f"'{self.province}', " \
              f"'{self.city}', " \
              f"'{self.message}'" \
              f")"

        return sql

    @staticmethod
    def get_csv_header(sep=project_config.csv_output_sep):
        return f"log_time{sep}log_level{sep}log_module{sep}respond_time{sep}province{sep}city{sep}message"

    def to_csv(self, sep=project_config.csv_output_sep):
        csv_line = \
            f"{self.log_time}{sep}" \
            f"{self.log_level}{sep}" \
            f"{self.log_module}{sep}" \
            f"{self.respond_time}{sep}" \
            f"{self.province}{sep}" \
            f"{self.city}{sep}" \
            f"{self.message}{sep}"
        return csv_line
