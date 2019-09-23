from unittest import TestCase
import responses
from itlogist.client import ITLogistClient as Client, ITLogistException


API_KEY = 'ae56f2b0b3728d564cacd97ffdff8a61'
DOMAIN = "mydomain"


class TestClient(TestCase):

    def test_init(self):

        client = Client('spamhameggs', 'mydomain')

        self.assertEqual(client.api_key, 'spamhameggs')
        self.assertEqual(client.domain, 'mydomain')

    @responses.activate
    def test_add_orders(self):

        fake_response = {
            "result": 1
        }

        url = 'https://{}.itlogist.ru/api/v1/{}/orders_add/'.format(DOMAIN, API_KEY)
        responses.add(responses.POST, url, json=fake_response, status=200)

        client = Client(API_KEY, DOMAIN)

        orders = {
            "orders": {
                "1488": {
                    "ordertype": 2,
                    "ordernumber": 1488,
                    "date_from": "2019-09-01",
                    "time1_from": "12:00",
                    "time2_from": "13:00",

                    "date_to": "2019-09-01",
                    "time1_to": "17:00",
                    "time2_to": "18:00",
                    "pieces": 1,

                    "clientnamefrom": "Вася",
                    "clientcontactfrom": "Вася",
                    "clientphonefrom": 78124071343,

                    "clientnameto": "Маша",
                    "clientcontactto": "Маша",
                    "clientphoneto": 78124071342,
                }
            }
        }

        response = client.add_orders(orders)

        self.assertEqual(response, fake_response)

    @responses.activate
    def test_if_passed_nonexisting_domain(self):

        fake_response = "Ваш домен не найден: kabinet (kabinet.itlogist.ru) <br> Обратитесь в службу поддержки ITLOGIST"

        url = 'https://{}.itlogist.ru/api/v1/{}/orders_add/'.format('nonexistence', API_KEY)
        responses.add(responses.POST, url, body=fake_response, status=200)

        client = Client(API_KEY, 'nonexistence')

        orders = {
            "orders": {
                "1488": {
                    "ordertype": 2,
                    "ordernumber": 1488,
                    "date_from": "2019-09-01",
                    "time1_from": "12:00",
                    "time2_from": "13:00",

                    "date_to": "2019-09-01",
                    "time1_to": "17:00",
                    "time2_to": "18:00",
                    "pieces": 1,

                    "clientnamefrom": "Вася",
                    "clientcontactfrom": "Вася",
                    "clientphonefrom": 78124071343,

                    "clientnameto": "Маша",
                    "clientcontactto": "Маша",
                    "clientphoneto": 78124071342,
                }
            }
        }

        with self.assertRaises(ITLogistException, msg=fake_response):
            client.add_orders(orders)
