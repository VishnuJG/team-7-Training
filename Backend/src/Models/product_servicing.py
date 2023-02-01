from queries import *
import json
import Operations
from Operations.unbxdAPI import UnbxdAPI
from Operations.database import Database


class Product():

    def __init__(self, uniqueId="", title="", price="", productDescription="", productImage="", catlevel1Name="", catlevel2Name="", category_id=""):
        self.uniqueId = uniqueId
        self.title = title
        self.price = price
        self.productDescription = productDescription
        self.productImage = productImage
        self.catlevel1Name = catlevel1Name
        self.catlevel2Name = catlevel2Name
        self.category_id = category_id
        


    def product_to_json(self):

        product_details = {}
        product_details['uniqueId'] = self.uniqueId
        product_details['title'] = self.title
        product_details['productDescription'] = self.productDescription
        product_details['price'] = self.price
        product_details['productImage'] = self.productImage

        return json.dumps(product_details)


    # """
    #     Validation for the presence of query parameters in the database
    #     Args: list of keys to validate
    #     Returns: dict params_dict containing parsed values of parameters
    # """

    # def validate_parameters(self, request, params_list):
        
    #     for param in params_list:
    #         if param not in request.args:
    #             self.param = ""
    #         else:
    #             self.param = request.args.get(param)
    #     return self

    
    def get_catalog_product_details(self):

        db = Database()

        # Validate presence of UniqueID in database
        product_exists_query = "SELECT EXISTS({});".format(GET_PRODUCT)
        product_exists = db.read_from_db(product_exists_query)
        
        # cur.execute(product_exists_query, (self.uniqueId,))
        if (product_exists[0]) == False:
            return "Requested product not present in catalog"

        # Find corresponding product details from product table

        query_response = db.read_from_db(GET_PRODUCT+";", (str(self.uniqueId),))

        # Create JSON object as response
        # print("TITLE", query_response)
        self.title = query_response[0][1]
        self.description = query_response[0][2]
        self.price = str(query_response[0][3])
        self.imageurl = query_response[0][4]
        print("Product request processed")

        return self.product_to_json()
        # convert to json in controller


    def get_searched_product_details(self):
        unbxdAPI_obj=UnbxdAPI()
        final_url=unbxdAPI_obj.url+'uniqueId='+self.uniqueId
        
        return unbxdAPI_obj.fetch_data_from_API(final_url)
        


    

        
 

