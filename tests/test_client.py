from unittest import TestCase
from unittest.mock import MagicMock
import responses
from itlogist.client import ITLogistClient as Client, ITLogistException


API_KEY = '6de38f49c4473d8ea2d9e9158404e97c'
DOMAIN = "mydomain"

order = {
    'COD_amount': 2500,
    'appraised_value': 2000,
    'buildingfrom': '12К1',
    'buildingto': '120К2',
    'cityfrom': client.SPB,
    'cityto': client.SPB,
    'clientcontactfrom': 'Иван Егоров',
    'clientcontactto': 'Ефимова Ольга',
    'clientnamefrom': 'ООО Пирамида',
    'clientnameto': 'Ефимова Ольга',
    'clientphonefrom': '8812999228282',
    'clientphoneto': '8905888775',
    'comment': 'хрупкий предмет',
    'date_from': '2019-09-25',
    'date_to': '2019-09-25',
    'md_order': 'e4516e384ef9cd91df081d5fe68cbcf9',
    'order_barcode': '1000001427508',
    'ordernumber': '1338',
    'ordertype': Client.EXPRESS_DELIVERY,
    'pieces': 2,
    'roomfrom': '301',
    'roomto': '17',
    'streetfrom': 'Ленина пр.',
    'streetto': 'Большевиков пр.',
    'time1_from': '10:00',
    'time1_to': '10:00',
    'time2_from': '22:00',
    'time2_to': '22:00',
    'value': 19.5,
    'weight': 5.5
}

invalid_order = {
    'COD_amount': 2500,
    'appraised_value': 2000,
    'buildingfrom': '12К1',
    'buildingto': '120К2',
    'cityfrom': client.SPB,
    'cityto': client.SPB,
    'clientcontactfrom': 'Иван Егоров',
    'clientcontactto': 'Ефимова Ольга',
    'clientnamefrom': 'ООО Пирамида',
    'clientnameto': 'Ефимова Ольга',
    'clientphonefrom': '8812999228282',
    'clientphoneto': '8905888775',
    'comment': 'хрупкий предмет',
    'date_from': '2015-09-25',
    'date_to': '2015-09-25',
    'md_order': 'e4516e384ef9cd91df081d5fe68cbcf9',
    'order_barcode': '1000001427508',
    'ordernumber': '1339',
    'ordertype': Client.EXPRESS_DELIVERY,
    'pieces': 2,
    'roomfrom': '301',
    'roomto': '17',
    'streetfrom': 'Ленина пр.',
    'streetto': 'Большевиков пр.',
    'time1_from': '10:00',
    'time1_to': '10:00',
    'time2_from': '22:00',
    'time2_to': '22:00',
    'value': 19.5,
    'weight': 5.5
}


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
                "666": {
                    "ordertype": Client.DELIVERY,
                    "ordernumber": 666,
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
                "1337": order
            }
        }

        with self.assertRaises(ITLogistException, msg=fake_response):
            client.send(url, orders)

    @responses.activate
    def test_send_if_an_error(self):

        fake_response = {
            'result': 0,
            'error': 'Array orders is null',
            'get': [],
            'post': {'orders': '{}'}
        }

        url = 'https://{}.itlogist.ru/api/v1/{}/orders_add/'.format(DOMAIN, API_KEY)
        responses.add(responses.POST, url, json=fake_response, status=200)

        wrong_orders = { "orders": { } }

        client = Client(API_KEY, DOMAIN)

        with self.assertRaises(ITLogistException, msg='Array orders is null'):
            client.send(url, wrong_orders)

    @responses.activate
    def test_send(self):

        fake_response = {
            'result': 1, 'info': {'1337': {'order_add': 1, 'itlogist_order_id': 10_000}}
        }

        orders = {
            "orders": {
                "1337": order
            }
        }

        url = 'https://{}.itlogist.ru/api/v1/{}/orders_add/'.format(API_KEY, DOMAIN)
        responses.add(responses.POST, url, json=fake_response, status=200)

        client = Client(DOMAIN, API_KEY)

        response = client.send(url, orders)

        self.assertEqual(response, fake_response)

    @responses.activate
    def test_send_if_some_error(self):

        fake_response = {
                 'result': 0,
                 'info': {
                     '1338': {'order_add': 1, 'itlogist_order_id': 74724},
                     '1339': {'error': 'error date 2015-09-25 (2015-09-25), error date 2015-09-25 (2015-09-25)', 'order_add': 0}
                  }
             }

        url = 'https://{}.itlogist.ru/api/v1/{}/orders_add/'.format(DOMAIN, API_KEY)
        responses.add(responses.POST, url, json=fake_response, status=200)

        wrong_orders = {"orders": {
                '1338': order,
                '1339': invalid_order
            }
        }

        client = Client(API_KEY, DOMAIN)

        response = client.send(url, wrong_orders)

        # Don't rise anithing if some orders passed and some not
        self.assertEqual(response, fake_response)

    def test_add_an_order(self):

        client = Client(API_KEY, DOMAIN)
        client.add_orders = MagicMock()

        client.add_order(
            order_id="100500",
            ordertype=Client.DELIVERY,

            date_from="2019-09-25",
            time1_from="12:00",
            time2_from="13:00",

            date_to="2019-09-25",

            clientnamefrom="Вася",
            clientcontactfrom="Вася",
            clientphonefrom=89771016770,

            clientnameto="Лена",
            clientcontactto="Лена",
            clientphoneto=89771016767,
            cityfrom= client.SPB,
            cityto= client.SPB,

            streetfrom="Мира",
            streetto="Мира",
            buildingfrom="5",
            buildingto="55"
        )

        expected = {
            "orders": {
                "100500": dict(
                    ordertype=Client.DELIVERY,

                    date_from="2019-09-25",
                    time1_from="12:00",
                    time2_from="13:00",

                    date_to="2019-09-25",

                    clientnamefrom="Вася",
                    clientcontactfrom="Вася",
                    clientphonefrom=89771016770,

                    clientnameto="Лена",
                    clientcontactto="Лена",
                    clientphoneto=89771016767,
                    cityfrom= client.SPB,
                    cityto= client.SPB,

                    streetfrom="Мира",
                    streetto="Мира",
                    buildingfrom="5",
                    buildingto="55"
                )
            }
        }

        client.add_orders.assert_called_with(expected)
