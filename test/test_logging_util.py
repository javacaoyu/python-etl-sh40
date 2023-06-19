import logging
import os.path
from unittest import TestCase
from util import logging_util


class Test(TestCase):

    def test_get_logger(self):
        logger = logging_util.get_logger(
            log_path=r"E:\上海40期-PythonETL\代码\python-etl-sh40\logs\unittest.log"
        )
        self.assertIsInstance(logger, logging.Logger)
        handles = logger.handlers
        self.assertEqual(len(handles), 1)

        logger.info("hahaha")
        self.assertTrue(True, os.path.exists(r"E:\上海40期-PythonETL\代码\python-etl-sh40\logs\unittest.log"))
