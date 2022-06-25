
import unittest
from src.EntryPayload import EntryPayload
from src.utils.uploader import post_time


class test_uploader(unittest.TestCase):
    payload = EntryPayload('testPlayer', 'luigiraceway', 2000, 'flap')

    def test_post_time(self):
        response = post_time(self.payload.to_json())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['userId'], self.payload.userId)
