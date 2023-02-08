import requests
import json

class Search():

    url = ""

    def __init__(self):

        
        self.url =  "https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?"

    
    def return_search_query(self, search_term, request):

        self.url += "q="+search_term+"&"
        for param in request.args:
            # print(param)
            self.url += "{}={}&".format(param, request.args[param])
        # print(self.url)
        unbxd_val = requests.get(self.url).content
        unbxd_val = json.loads(unbxd_val)
        # print(unbxd_val)
        return [unbxd_val['response']['numberOfProducts'], unbxd_val['response']['products']]

