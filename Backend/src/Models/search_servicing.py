import requests
import json

class Search():

    url = ""

    def __init__(self):
        self.url =  "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?"

    
    """
        Retrieves search results by accessing the UNBXD Search API
        Args: string searched 
              request object
        Returns: list
                 First element is total number of products being retrieved
                 Second element is list of products
    """

    def return_search_query(self, search_term, request):
        
        # Form URL using the search term and other parameters
        self.url += "q="+search_term+"&"
        for param in request.args:
            self.url += "{}={}&".format(param, request.args[param])

        # Send a GET request to the UNBXD Search API
        unbxd_val = requests.get(self.url).content
        unbxd_val = json.loads(unbxd_val)
        result = []
        for product in unbxd_val['response']['products']:
            result.append({'uniqueId': product['uniqueId'], 'title': product['title'], 'productdescription': product['productDescription'], 'price': product['price'], 'productimage': product['productImage'], 'catlevel1name': product['catlevel1Name'], 'catlevel2name': product['catlevel2Name']})
        return [unbxd_val['response']['numberOfProducts'], result]

