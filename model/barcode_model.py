# coding:utf8
"""
商品（条码库）信息模型
"""
from config import db_config, project_config
from util import str_util


class BarcodeModel:

    def __init__(self, data_tuple=None):
        """
        Note：date_tuple是传入的数据元组，请确保元组内的列顺序遵循如下顺序：
        - code
        - name
        - spec
        - trademark
        - addr
        - units
        - factory_name
        - trade_price
        - retail_price
        - update_at
        - wholeunit
        - wholenum
        - img
        - src
        :param data_tuple: 传入的数据元组
        """

        self.code = data_tuple[0]
        self.name = data_tuple[1]
        self.spec = data_tuple[2]
        self.trademark = data_tuple[3]
        self.addr = data_tuple[4]
        self.units = data_tuple[5]
        self.factory_name = data_tuple[6]
        self.trade_price = data_tuple[7]
        self.retail_price = data_tuple[8]
        self.update_at = data_tuple[9]
        self.wholeunit = data_tuple[10]
        self.wholenum = data_tuple[11]
        self.img = data_tuple[12]
        self.src = data_tuple[13]

    def generate_insert_sql(self, table_name=db_config.target_barcode_table_name):
        sql = f"INSERT IGNORE INTO {table_name}(code, name, spec, trademark, addr, units, " \
              f"factory_name, trade_price, retail_price, update_at, wholeunit, wholenum, " \
              f"img, src) VALUES(" \
              f"'{self.code}', " \
              f"'{str_util.clean_str(self.name)}', " \
              f"'{str_util.clean_str(self.spec)}', " \
              f"'{str_util.clean_str(self.trademark)}', " \
              f"'{str_util.clean_str(self.addr)}', " \
              f"'{str_util.clean_str(self.units)}', " \
              f"'{str_util.clean_str(self.factory_name)}', " \
              f"'{str_util.clean_str(self.trade_price)}', " \
              f"'{str_util.clean_str(self.retail_price)}', " \
              f"'{str_util.clean_str(self.update_at)}', " \
              f"'{str_util.clean_str(self.wholeunit)}', " \
              f"{str_util.check_number_null_and_transform_to_sql_null(self.wholenum)}, " \
              f"'{str_util.clean_str(self.img)}', " \
              f"'{str_util.clean_str(self.src)}'" \
              f")"
        return sql

    @staticmethod
    def get_csv_header(sep=project_config.csv_output_sep):
        header = f"code{sep}," \
                 f"name{sep}," \
                 f"spec{sep}," \
                 f"trademark{sep}," \
                 f"addr{sep}," \
                 f"units{sep}," \
                 f"factory_name{sep}," \
                 f"trade_price{sep}," \
                 f"retail_price{sep}," \
                 f"update_at{sep}," \
                 f"wholeunit{sep}," \
                 f"wholenum{sep}," \
                 f"img{sep}," \
                 "src"
        return header

    def to_csv(self, sep=project_config.csv_output_sep):
        csv_line = f"{self.code}{sep}," \
                   f"{self.name}{sep}," \
                   f"{self.spec}{sep}," \
                   f"{self.trademark}{sep}," \
                   f"{self.addr}{sep}," \
                   f"{self.units}{sep}," \
                   f"{self.factory_name}{sep}," \
                   f"{self.trade_price}{sep}," \
                   f"{self.retail_price}{sep}," \
                   f"{self.update_at}{sep}," \
                   f"{self.wholeunit}{sep}," \
                   f"{self.wholenum}{sep}," \
                   f"{self.img}{sep}," \
                   f"{self.src}"
        return csv_line
