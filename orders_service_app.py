# coding:utf8
"""
订单（Json文件）数据采集，启动逻辑
"""
from service.orders_service import OrdersService
if __name__ == '__main__':
    OrdersService().start()


"""
从逻辑封装中，OrdersService类是对：
- 从Json读取文件
- 判断元数据找出需要处理的文件
- 转换成模型
- 转换为sql插入mysql
- 转换为csv字符串写入文件
这一系列操作，都可以被OrdersService类所包含，我们只需要获得
OrdersService类的一个实例对象，点击start启动即可。
"""
