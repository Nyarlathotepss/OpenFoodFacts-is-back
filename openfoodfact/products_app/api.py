import requests
import constant


class API:
    """Communicate with API"""
    def __init__(self):
        self.json = None

    def communication_api(self, url, dict_parameters):
        """got .json from api"""
        r = requests.get(url, dict_parameters)
        self.json = r.json()

    def generate_parameters(self, category):
        param_url = {'action': 'process',
                     'tagtype_0': 'categories',
                     'tag_contains_0': 'contains',
                     'tag_0': category,
                     'sort_by': 'unique_scans_n',
                     'page_size': constant.LIMIT_PRODUCT,
                     'axis_x': 'energy',
                     'axis_y': 'products_n',
                     'json': '1'}
        return param_url