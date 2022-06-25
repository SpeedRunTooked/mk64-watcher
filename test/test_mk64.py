
import unittest
from src.utils import mk64


class test_mk64(unittest.TestCase):

    def test_get_tracklist(self):
        name_list = mk64.get_tracklist('names')
        slug_list = mk64.get_tracklist('slugs')

        self.assertEqual(name_list[0], 'Luigi Raceway')
        self.assertEqual(slug_list[0], 'luigiraceway')

# TODO - Write tests for mk64.compare_records so we can cover all edge cases, with deleted tracks, etc...
