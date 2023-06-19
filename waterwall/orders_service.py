# coding:utf8
"""
针对Json数据采集（订单数据）的业务逻辑代码（瀑布流）
"""
import json
import os
import sys

import pymysql
from utils import *

# ------ 配置信息段 -----
metadata_processed_table_name = \
    'orders_processed_files'                        # 记录了元数据表的表名
orders_json_file_data_path = "E:/pyetl-data"        # 记录了Json数据文件都在哪个文件夹内出现
target_orders_table_name = 'orders'                 # 目标库订单表，表名
target_orders_detail_table_name = 'orders_detail'   # 目标库订单表，表名
batch_commit_counter = 1000                         # 批量提交的计数器
csv_output_root_path = "E:/pyetl-data-output"       # csv数据输出的root根目录
csv_output_sep = ','                                # csv数据输出的分隔符定义
# ------ 配置信息段 -----


# TODO 1：元数据的读取
# 1.1 构建数据库链接，需要构建和元数据记录库以及和目标库记录的链接
# ps：这里尽管主机是同一个 ，我们还是分开来链接，因为在真实环境下，可能是2个不同的MySQL主机。
metadata_conn = pymysql.Connect(
    host='localhost',  # 主机
    port=3306,  # 端口
    user='root',  # 用户
    password='123456',  # 密码
    charset='UTF8',  # 编码
    autocommit=False,  # 自动提交
    db='metadata'
)

target_conn = pymysql.Connect(
    host='localhost',  # 主机
    port=3306,  # 端口
    user='root',  # 用户
    password='123456',  # 密码
    charset='UTF8',  # 编码
    autocommit=False,  # 自动提交
    db='target'
)

metadata_cursor = metadata_conn.cursor()  # 操作元数据库的游标对象
target_cursor = target_conn.cursor()  # 操作目的地数据库的游标对象

# 1.2 判断元数据表是否存在
metadata_cursor.execute("SHOW TABLES")
if (metadata_processed_table_name,) not in metadata_cursor.fetchall():
    create_table_sql = f"CREATE TABLE {metadata_processed_table_name}(" \
                       f"id int auto_increment primary key, " \
                       f"path varchar(255), " \
                       f"processed_date varchar(255))"
    print(f"元数据表：{metadata_processed_table_name}，不存在，现在创建它，SQL语句是：{create_table_sql}")
    metadata_cursor.execute(create_table_sql)

# 1.3 走到这里，这个表100%存在了，所以执行查询
metadata_cursor.execute(f"SELECT path FROM {metadata_processed_table_name}")
processed_file_list = []  # 记录已经处理过的文件列表
for line_tuple in metadata_cursor.fetchall():
    # (  ('a.txt', ),  ('b.txt', ) )
    processed_file_list.append(line_tuple[0])

# TODO 2：读取数据文件夹内的数据文件列表
all_files_list = []  # 记录全部的文件list
for name in os.listdir(orders_json_file_data_path):
    file_absolute_path = orders_json_file_data_path + "/" + name
    # 对路径符号，进行统一处理，都设置为单左斜杠
    all_files_list.append(unite_path_slash(file_absolute_path))

# TODO 3：和元数据中的记录做对比，找出本次需要处理的
need_to_process_files_list = []  # 需要被处理的文件路径list
for path in all_files_list:
    if path not in processed_file_list:  # 不在已经处理过的list记录中，就是想要的
        need_to_process_files_list.append(path)
print(f"本次即将处理的文件有：{need_to_process_files_list}")
if len(need_to_process_files_list) == 0:
    print(f"本次没有需要处理的文件，程序停止。")
    sys.exit(0)

# TODO 4：读取数据文件（Json字符串数据），转换成字典，封装到list内
origin_data_list = []  # 原始（未清洗转换）数据字典
for path in need_to_process_files_list:
    for line in open(path, 'r', encoding="UTF-8").readlines():
        line = line.strip()  # 通过strip去除前后空格以及换行符
        line_dict: dict = json.loads(line)
        origin_data_list.append(line_dict)

# TODO 5：数据清洗、转换
optimized_data_list = []  # 清洗转换后的数据字典list对象
for d in origin_data_list:
    # 省市区的转换处理
    if check_null(d['storeProvince']):  # 如果是True是无意义的内容
        d['storeProvince'] = '未知省份'  # 无意义就提供标记值
    if check_null(d['storeCity']):
        d['storeCity'] = '未知城市'
    if check_null(d['storeDistrict']):
        d['storeDistrict'] = '未知行政区'

    optimized_data_list.append(d)

# TODO 6：插入MySQL
# 6.1 组装SQL语句
orders_insert_sql_list = []                         # 订单表插入sql语句list
orders_detail_insert_sql_list = []                  # 订单详情表插入sql语句list

# 组装订单表的SQL list
for d in optimized_data_list:
    sql = f"INSERT INTO {target_orders_table_name}(" \
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
          f"\'{d['orderID']}\', " \
          f"{d['storeID']}, " \
          f"{check_null_and_transform_to_sql_null(d['storeName'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeStatus'])}, " \
          f"{d['storeOwnUserId']}, " \
          f"{check_null_and_transform_to_sql_null(d['storeOwnUserName'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeOwnUserTel'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeCategory'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeAddress'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeShopNo'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeProvince'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeCity'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeDistrict'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeGPSName'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeGPSAddress'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeGPSLongitude'])}, " \
          f"{check_null_and_transform_to_sql_null(d['storeGPSLatitude'])}, " \
          f"{d['isSigned']}, " \
          f"{check_null_and_transform_to_sql_null(d['operator'])}, " \
          f"{check_null_and_transform_to_sql_null(d['operatorName'])}, " \
          f"{check_null_and_transform_to_sql_null(d['faceID'])}, " \
          f"{check_null_and_transform_to_sql_null(d['memberID'])}, " \
          f"'{millisecond_ts_to_date_str(d['storeCreateDateTS'])}', " \
          f"{check_null_and_transform_to_sql_null(d['origin'])}, " \
          f"{d['dayOrderSeq']}, " \
          f"{d['discountRate']}, " \
          f"{d['discountType']}, " \
          f"{d['discount']}, " \
          f"{d['moneyBeforeWholeDiscount']}, " \
          f"{d['receivable']}, " \
          f"{d['erase']}, " \
          f"{d['smallChange']}, " \
          f"{d['totalNoDiscount']}, " \
          f"{d['payedTotal']}, " \
          f"{check_null_and_transform_to_sql_null(d['payType'])}, " \
          f"{d['paymentChannel']}, " \
          f"{check_null_and_transform_to_sql_null(d['paymentScenarios'])}, " \
          f"{d['productCount']}, " \
          f"'{millisecond_ts_to_date_str(d['dateTS'])}'" \
          f")"

    orders_insert_sql_list.append(sql)

# 组装订单详情表的SQL list
for d in optimized_data_list:
    for product_dict in d['product']:
        sql = f"INSERT INTO {target_orders_detail_table_name}(" \
              f"order_id, barcode, name, count, price_per, retail_price, " \
              f"trade_price, category_id, unit_id) VALUES(" \
              f"\'{d['orderID']}\', " \
              f"\'{product_dict['barcode']}\', " \
              f"\'{product_dict['name']}\', " \
              f"{product_dict['count']}, " \
              f"{product_dict['pricePer']}, " \
              f"{product_dict['retailPrice']}, " \
              f"{product_dict['tradePrice']}, " \
              f"{product_dict['categoryID']}, " \
              f"{product_dict['unitID']}" \
              f")"
        orders_detail_insert_sql_list.append(sql)

# 6.2 判断目标表是否存在，不存在创建它
target_cursor.execute("SHOW TABLES")
current_tables_list = []  # 查询出来有哪些表
for line_tuple in target_cursor.fetchall():
    # ( ('atable', ), ('btable', ) )
    current_tables_list.append(line_tuple[0])

if target_orders_table_name not in current_tables_list:
    # 订单表不存在，创建
    create_table_sql = f"CREATE TABLE {target_orders_table_name}(" \
                          "order_id                    VARCHAR(255) PRIMARY KEY," \
                          "store_id                    INT COMMENT '店铺ID'," \
                          "store_name                  VARCHAR(30) COMMENT '店铺名称'," \
                          "store_status                VARCHAR(10) COMMENT '店铺状态(open,close)'," \
                          "store_own_user_id           INT COMMENT '店主id'," \
                          "store_own_user_name         VARCHAR(50) COMMENT '店主名称'," \
                          "store_own_user_tel          VARCHAR(15) COMMENT '店主手机号'," \
                          "store_category              VARCHAR(10) COMMENT '店铺类型(normal,test)'," \
                          "store_address               VARCHAR(255) COMMENT '店铺地址'," \
                          "store_shop_no               VARCHAR(255) COMMENT '店铺第三方支付id号'," \
                          "store_province              VARCHAR(10) COMMENT '店铺所在省'," \
                          "store_city                  VARCHAR(10) COMMENT '店铺所在市'," \
                          "store_district              VARCHAR(10) COMMENT '店铺所在行政区'," \
                          "store_gps_name              VARCHAR(255) COMMENT '店铺gps名称'," \
                          "store_gps_address           VARCHAR(255) COMMENT '店铺gps地址'," \
                          "store_gps_longitude         VARCHAR(255) COMMENT '店铺gps经度'," \
                          "store_gps_latitude          VARCHAR(255) COMMENT '店铺gps纬度'," \
                          "is_signed                   TINYINT COMMENT '是否第三方支付签约(0,1)'," \
                          "operator                    VARCHAR(10) COMMENT '操作员'," \
                          "operator_name               VARCHAR(50) COMMENT '操作员名称'," \
                          "face_id                     VARCHAR(255) COMMENT '顾客面部识别ID'," \
                          "member_id                   VARCHAR(255) COMMENT '顾客会员ID'," \
                          "store_create_date_ts        TIMESTAMP COMMENT '店铺创建时间'," \
                          "origin                      VARCHAR(255) COMMENT '原始信息(无用)'," \
                          "day_order_seq               INT COMMENT '本订单是当日第几单'," \
                          "discount_rate               DECIMAL(10, 5) COMMENT '折扣率'," \
                          "discount_type               TINYINT COMMENT '折扣类型'," \
                          "discount                    DECIMAL(10, 5) COMMENT '折扣金额'," \
                          "money_before_whole_discount DECIMAL(10, 5) COMMENT '折扣前总金额'," \
                          "receivable                  DECIMAL(10, 5) COMMENT '应收金额'," \
                          "erase                       DECIMAL(10, 5) COMMENT '抹零金额'," \
                          "small_change                DECIMAL(10, 5) COMMENT '找零金额'," \
                          "total_no_discount           DECIMAL(10, 5) COMMENT '总价格(无折扣)'," \
                          "pay_total                   DECIMAL(10, 5) COMMENT '付款金额'," \
                          "pay_type                    VARCHAR(10) COMMENT '付款类型'," \
                          "payment_channel             TINYINT COMMENT '付款通道'," \
                          "payment_scenarios           VARCHAR(15) COMMENT '付款描述(无用)'," \
                          "product_count               INT COMMENT '本单卖出多少商品'," \
                          "date_ts                     VARCHAR(255) COMMENT '订单时间'," \
                          "INDEX (receivable)," \
                          "INDEX (date_ts))"
    print(f"目标表：{target_orders_table_name}不存在，创建它，SQL是：{create_table_sql}")
    target_cursor.execute(create_table_sql)

if target_orders_detail_table_name not in current_tables_list:
    # 订单详情表不存在，创建
    create_table_sql = f"CREATE TABLE {target_orders_detail_table_name}(" \
                                "order_id     VARCHAR(255) COMMENT '订单ID', " \
                                "barcode      VARCHAR(255) COMMENT '商品条码', " \
                                "name         VARCHAR(255) COMMENT '商品名称', " \
                                "count        INT COMMENT '本单此商品卖出数量', " \
                                "price_per    DECIMAL(10, 5) COMMENT '实际售卖单价', " \
                                "retail_price DECIMAL(10, 5) COMMENT '零售建议价', " \
                                "trade_price  DECIMAL(10, 5) COMMENT '贸易价格(进货价)', " \
                                "category_id  INT COMMENT '商品类别ID', " \
                                "unit_id      INT COMMENT '商品单位ID(包、袋、箱、等)', " \
                                "PRIMARY KEY (order_id, barcode))"
    print(f"目标表：{target_orders_detail_table_name}不存在，创建它，SQL是：{create_table_sql}")
    target_cursor.execute(create_table_sql)

# 6.3 执行SQL插入操作，走批量操作
# 判断自动提交，如果是True，设置为False
if target_conn.get_autocommit():
    target_conn.autocommit(False)                   # 如果是True，改False
# for循环sql list，执行insert插入
counter1 = 0                                        # 插入计数器
for sql in orders_insert_sql_list:
    target_cursor.execute(sql)
    counter1 += 1
    if counter1 % batch_commit_counter == 0:
        print(f"目标表：{target_orders_table_name}，插入了{counter1}条数据。")
        target_conn.commit()

counter2 = 0                                        # 重置计数器
for sql in orders_detail_insert_sql_list:
    target_cursor.execute(sql)
    counter2 += 1
    if counter2 % batch_commit_counter == 0:
        print(f"目标表：{target_orders_detail_table_name}，插入了{counter2}条数据。")
        target_conn.commit()
target_conn.commit()                                # 手动提交
print(f"目标表：{target_orders_table_name}插入数据完成，共插入了{counter1}条数据。")
print(f"目标表：{target_orders_detail_table_name}插入数据完成，共插入了{counter2}条数据。")

# TODO 7：写出CSV的逻辑
# 7.1 准备写出的文件对象
orders_csv_output_path = f"{csv_output_root_path}\orders_{get_time('%Y%m%d_%H%M%S')}.csv"
orders_detail_csv_output_path = f"{csv_output_root_path}\orders_detail_{get_time('%Y%m%d_%H%M%S')}.csv"
orders_csv_writer = open(orders_csv_output_path, 'a', encoding="UTF-8")                 # 订单csv写出的文件对象
orders_detail_csv_writer = open(orders_detail_csv_output_path, 'a', encoding="UTF-8")   # 订单详情csv写出的文件对象

# 7.2 先写第一行（csv的标头）
orders_header_str = \
            f"discountRate{csv_output_sep}" \
            f"storeShopNo{csv_output_sep}" \
            f"dayOrderSeq{csv_output_sep}" \
            f"storeDistrict{csv_output_sep}" \
            f"isSigned{csv_output_sep}" \
            f"storeProvince{csv_output_sep}" \
            f"origin{csv_output_sep}" \
            f"storeGPSLongitude{csv_output_sep}" \
            f"discount{csv_output_sep}" \
            f"storeID{csv_output_sep}" \
            f"productCount{csv_output_sep}" \
            f"operatorName{csv_output_sep}" \
            f"operator{csv_output_sep}" \
            f"storeStatus{csv_output_sep}" \
            f"storeOwnUserTel{csv_output_sep}" \
            f"payType{csv_output_sep}" \
            f"discountType{csv_output_sep}" \
            f"storeName{csv_output_sep}" \
            f"storeOwnUserName{csv_output_sep}" \
            f"dateTS{csv_output_sep}" \
            f"smallChange{csv_output_sep}" \
            f"storeGPSName{csv_output_sep}" \
            f"erase{csv_output_sep}" \
            f"storeGPSAddress{csv_output_sep}" \
            f"orderID{csv_output_sep}" \
            f"moneyBeforeWholeDiscount{csv_output_sep}" \
            f"storeCategory{csv_output_sep}" \
            f"receivable{csv_output_sep}" \
            f"faceID{csv_output_sep}" \
            f"storeOwnUserId{csv_output_sep}" \
            f"paymentChannel{csv_output_sep}" \
            f"paymentScenarios{csv_output_sep}" \
            f"storeAddress{csv_output_sep}" \
            f"totalNoDiscount{csv_output_sep}" \
            f"payedTotal{csv_output_sep}" \
            f"storeGPSLatitude{csv_output_sep}" \
            f"storeCreateDateTS{csv_output_sep}" \
            f"storeCity{csv_output_sep}" \
            f"memberID"
orders_csv_writer.write(orders_header_str)                      # 写出订单csv的标头字符串
orders_csv_writer.write("\n")                                   # 单独写一个换行符

orders_detail_header_str = \
            f"orderID{csv_output_sep}" \
            f"barcode{csv_output_sep}" \
            f"count{csv_output_sep}" \
            f"name{csv_output_sep}" \
            f"unitID{csv_output_sep}" \
            f"pricePer{csv_output_sep}" \
            f"retailPrice{csv_output_sep}" \
            f"tradePrice{csv_output_sep}" \
            f"categoryID"
orders_detail_csv_writer.write(orders_detail_header_str)
orders_detail_csv_writer.write("\n")

# 7.3 for循环处理数据，将每一个字典对象转换为对应的csv字符串，写出去
for d in optimized_data_list:                                   # 处理订单业务
    csv_line = \
        f"{d['discountRate']}{csv_output_sep}" \
        f"{d['storeShopNo']}{csv_output_sep}" \
        f"{d['dayOrderSeq']}{csv_output_sep}" \
        f"{d['storeDistrict']}{csv_output_sep}" \
        f"{d['isSigned']}{csv_output_sep}" \
        f"{d['storeProvince']}{csv_output_sep}" \
        f"{d['origin']}{csv_output_sep}" \
        f"{d['storeGPSLongitude']}{csv_output_sep}" \
        f"{d['discount']}{csv_output_sep}" \
        f"{d['storeID']}{csv_output_sep}" \
        f"{d['productCount']}{csv_output_sep}" \
        f"{d['operatorName']}{csv_output_sep}" \
        f"{d['operator']}{csv_output_sep}" \
        f"{d['storeStatus']}{csv_output_sep}" \
        f"{d['storeOwnUserTel']}{csv_output_sep}" \
        f"{d['payType']}{csv_output_sep}" \
        f"{d['discountType']}{csv_output_sep}" \
        f"{d['storeName']}{csv_output_sep}" \
        f"{d['storeOwnUserName']}{csv_output_sep}" \
        f"{d['dateTS']}{csv_output_sep}" \
        f"{d['smallChange']}{csv_output_sep}" \
        f"{d['storeGPSName']}{csv_output_sep}" \
        f"{d['erase']}{csv_output_sep}" \
        f"{d['storeGPSAddress']}{csv_output_sep}" \
        f"{d['orderID']}{csv_output_sep}" \
        f"{d['moneyBeforeWholeDiscount']}{csv_output_sep}" \
        f"{d['storeCategory']}{csv_output_sep}" \
        f"{d['receivable']}{csv_output_sep}" \
        f"{d['faceID']}{csv_output_sep}" \
        f"{d['storeOwnUserId']}{csv_output_sep}" \
        f"{d['paymentChannel']}{csv_output_sep}" \
        f"{d['paymentScenarios']}{csv_output_sep}" \
        f"{d['storeAddress']}{csv_output_sep}" \
        f"{d['totalNoDiscount']}{csv_output_sep}" \
        f"{d['payedTotal']}{csv_output_sep}" \
        f"{d['storeGPSLatitude']}{csv_output_sep}" \
        f"{d['storeCreateDateTS']}{csv_output_sep}" \
        f"{d['storeCity']}{csv_output_sep}" \
        f"{d['memberID']}"
    orders_csv_writer.write(csv_line)           # 写出订单csv字符串的一行
    orders_csv_writer.write("\n")               # 单独写一个换行符

counter = 0                                     # 计数器
for d in optimized_data_list:                   # 处理订单详情业务
    for product_dict in d['product']:
        csv_line = \
                f"{d['orderID']}{csv_output_sep}" \
                f"{product_dict['barcode']}{csv_output_sep}" \
                f"{product_dict['count']}{csv_output_sep}" \
                f"{product_dict['name']}{csv_output_sep}" \
                f"{product_dict['unitID']}{csv_output_sep}" \
                f"{product_dict['pricePer']}{csv_output_sep}" \
                f"{product_dict['retailPrice']}{csv_output_sep}" \
                f"{product_dict['tradePrice']}{csv_output_sep}" \
                f"{product_dict['categoryID']}"
        orders_detail_csv_writer.write(csv_line)
        orders_detail_csv_writer.write("\n")
        counter += 1

# 7.4 关闭文件对象
orders_csv_writer.close()
orders_detail_csv_writer.close()
print(f"写出CSV文件：{orders_csv_output_path}，写出条数：{len(optimized_data_list)}")
print(f"写出CSV文件：{orders_detail_csv_output_path}，写出条数：{counter}")


# TODO 8：记录元数据信息
for path in need_to_process_files_list:
    sql = f"INSERT INTO {metadata_processed_table_name} VALUES(" \
          f"NULL, '{path}', '{get_time()}')"
    print(f"向元数据记录本次处理的文件是：{path}，SQL语句：{sql}")
    metadata_cursor.execute(sql)
    metadata_conn.commit()

target_conn.close()
metadata_conn.close()
