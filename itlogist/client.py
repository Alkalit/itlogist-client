import requests
from json import JSONDecodeError, dumps


class ITLogistException(Exception):
    pass


class ITLogistClient:

    def __init__(self, api_key: str, domain: str):

        self.api_key = api_key
        self.domain = domain

    def add_order(self, order_id:str, ordertype:int, date_from:str, time1_from:str, time2_from:str, date_to:str,
            clientnamefrom:str, clientcontactfrom:str, clientphonefrom:int, clientnameto:str, clientcontactto:str,
            clientphoneto:int, cityfrom:int, cityto:int, streetfrom:str, streetto:str, buildingfrom:str, buildingto:str,
            ordernumber:str=None, time1_to:str=None, time2_to:str=None, value:float=None, weight:float=None, pieces:int=None,
            comment:str=None, order_barcode:str=None, appraised_value:float=None, COD_amount:float=None,
            roomfrom:str=None, latfrom:float=None, lngfrom:float=None, pickuppointfrom:int=None,
            roomto:str=None, latto:float=None, lngto:float=None, pickuppointto:int=None
            ):

        args = locals()
        args.pop('self')
        args.pop('order_id')

        data = {}
        for k, v in args.items():
            if v is not None:
                data[k] = v

        return self.add_orders({"orders": {order_id: data}})

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
