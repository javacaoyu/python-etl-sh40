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

# 目标库相关数据配置记录
target_orders_table_name = 'orders'                 # 目标库订单表，表名
target_orders_detail_table_name = 'orders_detail'   # 目标库订单表，表名

