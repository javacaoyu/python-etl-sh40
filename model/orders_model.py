# coding:utf8
"""
订单业务模型
"""
import json
from util import str_util
from util import time_util
from config import project_config, db_config


class OrdersModel:

    def __init__(self, data_str: str):
        """
        构造方法，仅需要传入Json字符串即可，能够完成从字符串中抽取列，封装数据到成员属性
        :param data: Json 字符串
        """
        data = json.loads(data_str)

        self.discount_rate = data['discountRate']                   # 折扣率
        self.store_shop_no = data['storeShopNo']                    # 店铺店号（无用列）
        self.day_order_seq = data['dayOrderSeq']                    # 本单为当日第几单
        self.store_district = data['storeDistrict']                 # 店铺所在行政区
        self.is_signed = data['isSigned']                           # 是否签约店铺（签约第三方支付体系）
        self.store_province = data['storeProvince']                 # 店铺所在省份
        self.origin = data['origin']                                # 原始信息（无用）
        self.store_gps_longitude = data['storeGPSLongitude']        # 店铺GPS经度
        self.discount = data['discount']                            # 折扣金额
        self.store_id = data['storeID']                             # 店铺ID
        self.product_count = data['productCount']                   # 本单售卖商品数量
        self.operator_name = data['operatorName']                   # 操作员姓名
        self.operator = data['operator']                            # 操作员ID
        self.store_status = data['storeStatus']                     # 店铺状态
        self.store_own_user_tel = data['storeOwnUserTel']           # 店铺店主电话
        self.pay_type = data['payType']                             # 支付类型
        self.discount_type = data['discountType']                   # 折扣类型
        self.store_name = data['storeName']                         # 店铺名称
        self.store_own_user_name = data['storeOwnUserName']         # 店铺店主名称
        self.date_ts = data['dateTS']                               # 订单时间
        self.small_change = data['smallChange']                     # 找零金额
        self.store_gps_name = data['storeGPSName']                  # 店铺GPS名称
        self.erase = data['erase']                                  # 是否抹零
        self.store_gps_address = data['storeGPSAddress']            # 店铺GPS地址
        self.order_id = data['orderID']                             # 订单ID
        self.money_before_whole_discount = data['moneyBeforeWholeDiscount']  # 折扣前金额
        self.store_category = data['storeCategory']                 # 店铺类别
        self.receivable = data['receivable']                        # 应收金额
        self.face_id = data['faceID']                               # 面部识别ID
        self.store_own_user_id = data['storeOwnUserId']             # 店铺店主ID
        self.payment_channel = data['paymentChannel']               # 付款通道
        self.payment_scenarios = data['paymentScenarios']           # 付款情况（无用）
        self.store_address = data['storeAddress']                   # 店铺地址
        self.total_no_discount = data['totalNoDiscount']            # 整体价格（无折扣）
        self.payed_total = data['payedTotal']                       # 已付款金额
        self.store_gps_latitude = data['storeGPSLatitude']          # 店铺GPS纬度
        self.store_create_date_ts = data['storeCreateDateTS']       # 店铺创建时间
        self.store_city = data['storeCity']                         # 店铺所在城市
        self.member_id = data['memberID']                           # 会员ID

        self.orders_detail_model_list = []                          # 订单详情模型list
        for product_dict in data['product']:
            model = OrdersDetailModel(self.order_id, product_dict)
            self.orders_detail_model_list.append(model)
    
    def generate_insert_sql(self, table_name=db_config.target_orders_table_name):
        """生成INSERT SQL语句"""
        sql = f"INSERT IGNORE INTO {table_name}(" \
              f"order_id,store_id,store_name,store_status,store_own_user_id," \
              f"store_own_user_name,store_own_user_tel,store_category," \
              f"store_address,store_shop_no,store_province,store_city," \
              f"store_district,store_gps_name,store_gps_address," \
              f"store_gps_longitude,store_gps_latitude,is_signed," \
              f"operator,operator_name,face_id,member_id,store_create_date_ts," \
              f"origin,day_order_seq,discount_rate,discount_type,discount," \
              f"money_before_whole_discount,receivable,erase,small_change," \
              f"total_no_discount,pay_total,pay_type,payment_channel," \
              f"payment_scenarios,product_count,date_ts" \
              f") VALUES(" \
              f"'{self.order_id}', " \
              f"{self.store_id}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_name)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_status)}, " \
              f"{self.store_own_user_id}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_own_user_name)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_own_user_tel)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_category)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_address)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_shop_no)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_province)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_city)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_district)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_gps_name)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_gps_address)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_gps_longitude)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.store_gps_latitude)}, " \
              f"{self.is_signed}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.operator)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.operator_name)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.face_id)}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.member_id)}, " \
              f"'{time_util.millisecond_ts_to_date_str(self.store_create_date_ts)}', " \
              f"{str_util.check_null_and_transform_to_sql_null(self.origin)}, " \
              f"{self.day_order_seq}, " \
              f"{self.discount_rate}, " \
              f"{self.discount_type}, " \
              f"{self.discount}, " \
              f"{self.money_before_whole_discount}, " \
              f"{self.receivable}, " \
              f"{self.erase}, " \
              f"{self.small_change}, " \
              f"{self.total_no_discount}, " \
              f"{self.payed_total}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.pay_type)}, " \
              f"{self.payment_channel}, " \
              f"{str_util.check_null_and_transform_to_sql_null(self.payment_scenarios)}, " \
              f"{self.product_count}, " \
              f"'{time_util.millisecond_ts_to_date_str(self.date_ts)}')"
        return sql

    def to_csv(self):
        csv_line = \
            f"{self.discount_rate}{project_config.csv_output_sep}" \
            f"{self.store_shop_no}{project_config.csv_output_sep}" \
            f"{self.day_order_seq}{project_config.csv_output_sep}" \
            f"{self.store_district}{project_config.csv_output_sep}" \
            f"{self.is_signed}{project_config.csv_output_sep}" \
            f"{self.store_province}{project_config.csv_output_sep}" \
            f"{self.origin}{project_config.csv_output_sep}" \
            f"{self.store_gps_longitude}{project_config.csv_output_sep}" \
            f"{self.discount}{project_config.csv_output_sep}" \
            f"{self.store_id}{project_config.csv_output_sep}" \
            f"{self.product_count}{project_config.csv_output_sep}" \
            f"{self.operator_name}{project_config.csv_output_sep}" \
            f"{self.operator}{project_config.csv_output_sep}" \
            f"{self.store_status}{project_config.csv_output_sep}" \
            f"{self.store_own_user_tel}{project_config.csv_output_sep}" \
            f"{self.pay_type}{project_config.csv_output_sep}" \
            f"{self.discount_type}{project_config.csv_output_sep}" \
            f"{self.store_name}{project_config.csv_output_sep}" \
            f"{self.store_own_user_name}{project_config.csv_output_sep}" \
            f"{self.date_ts}{project_config.csv_output_sep}" \
            f"{self.small_change}{project_config.csv_output_sep}" \
            f"{self.store_gps_name}{project_config.csv_output_sep}" \
            f"{self.erase}{project_config.csv_output_sep}" \
            f"{self.store_gps_address}{project_config.csv_output_sep}" \
            f"{self.order_id}{project_config.csv_output_sep}" \
            f"{self.money_before_whole_discount}{project_config.csv_output_sep}" \
            f"{self.store_category}{project_config.csv_output_sep}" \
            f"{self.receivable}{project_config.csv_output_sep}" \
            f"{self.face_id}{project_config.csv_output_sep}" \
            f"{self.store_own_user_id}{project_config.csv_output_sep}" \
            f"{self.payment_channel}{project_config.csv_output_sep}" \
            f"{self.payment_scenarios}{project_config.csv_output_sep}" \
            f"{self.store_address}{project_config.csv_output_sep}" \
            f"{self.total_no_discount}{project_config.csv_output_sep}" \
            f"{self.payed_total}{project_config.csv_output_sep}" \
            f"{self.store_gps_latitude}{project_config.csv_output_sep}" \
            f"{self.store_create_date_ts}{project_config.csv_output_sep}" \
            f"{self.store_city}{project_config.csv_output_sep}" \
            f"{self.member_id}"
        return csv_line

    @staticmethod
    def get_csv_header():
        orders_header_str = \
            f"discountRate{project_config.csv_output_sep}" \
            f"storeShopNo{project_config.csv_output_sep}" \
            f"dayOrderSeq{project_config.csv_output_sep}" \
            f"storeDistrict{project_config.csv_output_sep}" \
            f"isSigned{project_config.csv_output_sep}" \
            f"storeProvince{project_config.csv_output_sep}" \
            f"origin{project_config.csv_output_sep}" \
            f"storeGPSLongitude{project_config.csv_output_sep}" \
            f"discount{project_config.csv_output_sep}" \
            f"storeID{project_config.csv_output_sep}" \
            f"productCount{project_config.csv_output_sep}" \
            f"operatorName{project_config.csv_output_sep}" \
            f"operator{project_config.csv_output_sep}" \
            f"storeStatus{project_config.csv_output_sep}" \
            f"storeOwnUserTel{project_config.csv_output_sep}" \
            f"payType{project_config.csv_output_sep}" \
            f"discountType{project_config.csv_output_sep}" \
            f"storeName{project_config.csv_output_sep}" \
            f"storeOwnUserName{project_config.csv_output_sep}" \
            f"dateTS{project_config.csv_output_sep}" \
            f"smallChange{project_config.csv_output_sep}" \
            f"storeGPSName{project_config.csv_output_sep}" \
            f"erase{project_config.csv_output_sep}" \
            f"storeGPSAddress{project_config.csv_output_sep}" \
            f"orderID{project_config.csv_output_sep}" \
            f"moneyBeforeWholeDiscount{project_config.csv_output_sep}" \
            f"storeCategory{project_config.csv_output_sep}" \
            f"receivable{project_config.csv_output_sep}" \
            f"faceID{project_config.csv_output_sep}" \
            f"storeOwnUserId{project_config.csv_output_sep}" \
            f"paymentChannel{project_config.csv_output_sep}" \
            f"paymentScenarios{project_config.csv_output_sep}" \
            f"storeAddress{project_config.csv_output_sep}" \
            f"totalNoDiscount{project_config.csv_output_sep}" \
            f"payedTotal{project_config.csv_output_sep}" \
            f"storeGPSLatitude{project_config.csv_output_sep}" \
            f"storeCreateDateTS{project_config.csv_output_sep}" \
            f"storeCity{project_config.csv_output_sep}" \
            f"memberID"
        return orders_header_str


class OrdersDetailModel:

    def __init__(self, order_id, product_dict):

        self.order_id = order_id
        self.count = product_dict['count']
        self.name = product_dict['name']
        self.unit_id = product_dict['unitID']
        self.barcode = product_dict['barcode']
        self.price_per = product_dict['pricePer']
        self.retail_price = product_dict['retailPrice']
        self.trade_price = product_dict['tradePrice']
        self.category_id = product_dict['categoryID']

    def generate_insert_sql(self, table_name=db_config.target_orders_detail_table_name):
        sql = f"INSERT INTO {table_name}(" \
              f"order_id, barcode, name, count, price_per, retail_price, " \
              f"trade_price, category_id, unit_id) VALUES(" \
              f"\'{self.order_id}\', " \
              f"\'{self.barcode}\', " \
              f"\'{self.name}\', " \
              f"{self.count}, " \
              f"{self.price_per}, " \
              f"{self.retail_price}, " \
              f"{self.trade_price}, " \
              f"{self.category_id}, " \
              f"{self.unit_id}" \
              f")"
        return sql

    def to_csv(self, sep=project_config.csv_output_sep):
        csv_line = \
            f"{self.order_id}{sep}" \
            f"{self.barcode}{sep}" \
            f"{self.count}{sep}" \
            f"{self.name}{sep}" \
            f"{self.unit_id}{sep}" \
            f"{self.price_per}{sep}" \
            f"{self.retail_price}{sep}" \
            f"{self.trade_price}{sep}" \
            f"{self.category_id}"
        return csv_line

    @staticmethod
    def get_csv_header():
        orders_detail_header_str = \
            f"orderID{project_config.csv_output_sep}" \
            f"barcode{project_config.csv_output_sep}" \
            f"count{project_config.csv_output_sep}" \
            f"name{project_config.csv_output_sep}" \
            f"unitID{project_config.csv_output_sep}" \
            f"pricePer{project_config.csv_output_sep}" \
            f"retailPrice{project_config.csv_output_sep}" \
            f"tradePrice{project_config.csv_output_sep}" \
            f"categoryID"

        return orders_detail_header_str
