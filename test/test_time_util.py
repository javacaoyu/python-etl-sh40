# coding:utf8
"""
测试time_util.py的内容
"""
from unittest import TestCase
from util import time_util
import time


class TestTimeUtil(TestCase):

    def test_get_time(self):
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        r = time_util.get_time()
        self.assertEqual(dt, r)

    def test_get_today(self):
        r = time_util.get_today()
        dt = time.strftime("%Y-%m-%d", time.localtime())
        self.assertEqual(dt, r)

    def test_second_ts_to_date_str(self):
        r = time_util.second_ts_to_date_str(1688659200)
        self.assertEqual("2023-07-07 00:00:00", r)

        r = time_util.second_ts_to_date_str(1688659200, "%Y_%m_%d-%H-%M-%S")
        self.assertEqual("2023_07_07-00-00-00", r)

    def test_millisecond_ts_to_date_str(self):
        r = time_util.millisecond_ts_to_date_str(1688659200000)
        self.assertEqual("2023-07-07 00:00:00", r)

        r = time_util.millisecond_ts_to_date_str(1688659200000, "%Y_%m_%d-%H-%M-%S")
        self.assertEqual("2023_07_07-00-00-00", r)

        r = time_util.millisecond_ts_to_date_str(1688659200003)
        self.assertEqual("2023-07-07 00:00:00", r)

        r = time_util.millisecond_ts_to_date_str(1688659200003, "%Y_%m_%d-%H-%M-%S")
        self.assertEqual("2023_07_07-00-00-00", r)
