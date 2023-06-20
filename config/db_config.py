# coding:utf8
"""
和数据库相关的配置项
项目中会用到：
- metadata：元数据记录（库）
- target：目标记录（库）
"""

# 元数据相关数据库配置记录
metadata_orders_processed_table_name = \
    'orders_processed_files'                        # 记录了元数据表的表名
metadata_db_name = 'metadata'
metadata_host = "localhost"
metadata_port = 3306
metadata_user = "root"
metadata_password = "123456"
metadata_charset = "UTF8"

# 目标库相关数据配置记录
target_orders_table_name = 'orders'                 # 目标库订单表，表名
target_orders_detail_table_name = 'orders_detail'   # 目标库订单表，表名
target_db_name = 'target'
target_host = "localhost"
target_port = 3306
target_user = "root"
target_password = "123456"
target_charset = "UTF8"

# 单元测试相关
unittest_db_name = 'unittest'
unittest_host = "localhost"
unittest_port = 3306
unittest_user = "root"
unittest_password = "123456"
unittest_charset = "UTF8"
