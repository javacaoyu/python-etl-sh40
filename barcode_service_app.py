# coding:utf8
"""
条码库服务主启动程序
"""
from service.barcode_service import BarcodeService


if __name__ == '__main__':
    BarcodeService().start()
