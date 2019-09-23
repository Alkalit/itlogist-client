from unittest import TestCase
from itlogist.client import ITLogistClient as Client


class TestClient(TestCase):

    def test_init(self):

        client = Client('spamhameggs', 'mydomain')

        self.assertEqual(client.api_key, 'spamhameggs')
        self.assertEqual(client.domain, 'mydomain')
