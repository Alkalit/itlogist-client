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
        response = requests.post(url, data=data)

        try:
            response_data = response.json()
        except JSONDecodeError:
            raise ITLogistException(response.text)

        # if condition:
        #     $

        return response_data

    def send(self, data):

        url = 'https://{}.itlogist.ru/api/v1/{}/orders_add/'.format(self.domain, self.api_key)

        data = {"orders": dumps(data["orders"])}
        response = requests.post(url, data=data)

        try:
            response_data = response.json()
        except JSONDecodeError:
            raise ITLogistException(response.text)


        # TODO - как отработает запрос, если какие-то заказы с ошибкой?
        # if condition:
        #     $

        return response_data
