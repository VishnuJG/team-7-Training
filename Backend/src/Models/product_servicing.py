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


    
    def get_catalog_product_details(self):

        db = Database()

        # Validate presence of UniqueID in database
        product_exists_query = "SELECT EXISTS({});".format(GET_PRODUCT)
        product_exists = db.read_from_db(product_exists_query)
        # if "Error" in product_exists:
        #     return product_exists
        
        # cur.execute(product_exists_query, (self.uniqueId,))
        if (product_exists[0]) == False:
            return "Error: Requested product not present in catalog"

        # Find corresponding product details from product table

        query_response = db.read_from_db(GET_PRODUCT+";", (str(self.uniqueId),))
        
        if "Error" in query_response:
            return query_response
        
        # Create JSON object as response
        # print("TITLE", query_response)
        # print(self.uniqueId)

        self.title = query_response[0][1]
        self.productDescription = query_response[0][2]
        self.price = str(query_response[0][3])
        self.productImage= query_response[0][4]
        print("Product request processed")
        return self.product_to_json()
        # convert to json in controller


    def get_searched_product_details(self):
        unbxdAPI_obj=UnbxdAPI()
        final_url=unbxdAPI_obj.url+'q=uniqueId '+self.uniqueId
        
        return unbxdAPI_obj.fetch_data_from_API(final_url)
        


    

        
 

