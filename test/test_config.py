
import unittest
from src.utils import config


class test_mk64(unittest.TestCase):

    def test_get_configt(self):
        filname = config.get_config()['eep-file']

        self.assertEqual(filname, 'MARIOKART64.eep')
