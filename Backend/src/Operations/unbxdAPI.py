import json
import requests

class UnbxdAPI:

    def __init__(self):
        
        self.url = "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?"
        

    """
        Connect to the unbxdAPI
        Args: URL to connect to
        Returns: list
                 first element is the total number of products 
                 Second element is a list of products
    """

    def fetch_data_from_API(self, final_url):
        unbxd_val = requests.get(final_url).content
        unbxd_val = json.loads(unbxd_val)
        print(unbxd_val)
        return [unbxd_val['response']['numberOfProducts'], unbxd_val['response']['products']]

    