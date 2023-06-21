# coding:utf8
"""
针对文件工具做单元测试
"""
import os
from unittest import TestCase
from util import file_util


class TestFileUtil(TestCase):

    def setUp(self) -> None:
        # 前置方法
        # 确认单元测试用的文件夹是否存在，不存在创建
        self.unittest_root_path = f"{os.path.dirname(os.getcwd())}/test/unittest"
        if not os.path.exists(self.unittest_root_path):
            os.mkdir(self.unittest_root_path)

    def test_change_file_suffix(self):
        # 创建测试文件
        test_file_path = self.unittest_root_path + "/" + "test.csv.tmp"
        # 如果测试文件不存在，则创建
        if not os.path.exists(test_file_path):
            open(test_file_path, 'w', encoding="UTF-8").close()
        # 确认目标文件不存在
        target_file_path = self.unittest_root_path + "/" + "test.csv"
        # 确认目标文件不存在，存在删除
        if os.path.exists(target_file_path):
            os.remove(target_file_path)

        file_util.change_file_suffix(test_file_path, "", ".tmp")
        self.assertTrue(os.path.exists(self.unittest_root_path + "/" + "test.csv"))
        os.remove(target_file_path)




