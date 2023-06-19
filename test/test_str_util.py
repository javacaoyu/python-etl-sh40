from unittest import TestCase
from util import str_util


class Test(TestCase):
    def test_check_null(self):
        r = str_util.check_null(None)
        self.assertTrue(r)

        r = str_util.check_null("NonE")
        self.assertTrue(r)

        r = str_util.check_null("")
        self.assertTrue(r)

        r = str_util.check_null("NulL")
        self.assertTrue(r)

        r = str_util.check_null("UndeFined")
        self.assertTrue(r)

        r = str_util.check_null("哈哈哈")
        self.assertFalse(r)

    def test_check_null_and_transform_to_sql_null(self):
        r = str_util.check_null_and_transform_to_sql_null("")
        self.assertEqual("NULL", r.upper())

        r = str_util.check_null_and_transform_to_sql_null("None")
        self.assertEqual("NULL", r.upper())

        r = str_util.check_null_and_transform_to_sql_null("NulL")
        self.assertEqual("NULL", r.upper())

        r = str_util.check_null_and_transform_to_sql_null("UndeFined")
        self.assertEqual("NULL", r.upper())

        r = str_util.check_null_and_transform_to_sql_null(None)
        self.assertEqual("NULL", r.upper())

        r = str_util.check_null_and_transform_to_sql_null("哈哈哈")
        self.assertEqual("'哈哈哈'", r.upper())

    def test_unite_path_slash(self):
        # r""，表示将字符串的内容原样输出，也就是里面写什么样子就是什么样子（撇除转义）
        r = str_util.unite_path_slash(r"E:\\a\b\\c\d/e")
        self.assertEqual("E:/a/b/c/d/e", r)
