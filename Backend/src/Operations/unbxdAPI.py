import json
import requests

class UnbxdAPI:

    def __init__(self):
        
        self.url = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?"
        

    """
        Connect to the unbxdAPI
        Args: url to connect to
        Returns: [number of products , products list]
    """

    def fetch_data_from_API(self, final_url):
        unbxd_val = requests.get(final_url).content
        unbxd_val = json.loads(unbxd_val)
        return [unbxd_val['response']['numberOfProducts'], unbxd_val['response']['products']]

    