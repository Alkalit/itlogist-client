import requests
from json import JSONDecodeError, dumps


class ITLogistException(Exception):
    pass


class ITLogistClient:

    def __init__(self, api_key: str, domain: str):

        self.api_key = api_key
        self.domain = domain

    def add_orders(self, data):

        url = 'https://{}.itlogist.ru/api/v1/{}/orders_add/'.format(self.domain, self.api_key)

        return self.send(url, data)

    def send(self, url, data):

        data = {"orders": dumps(data["orders"])}
        response = requests.post(url, data=data)

        try:
            response_data = response.json()
        except JSONDecodeError:
            raise ITLogistException(response.text)

        if response_data['result'] == 0 and 'error' in response_data:
            raise ITLogistException(response_data['error'])

        return response_data
