from unittest import TestCase
from tmp import t1


class Test(TestCase):
    def test_make_upper(self):
        r = t1.make_upper("abc")
        self.assertEqual("ABC", r)
