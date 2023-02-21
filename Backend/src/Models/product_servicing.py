from queries import *
import json
import Operations
from Operations.unbxdAPI import UnbxdAPI
from Operations.database import Database


class Product():

    uniqueId = ""
    title = ""
    price = ""
    productDescription = ""
    productImage = ""
    catlevel1Name = ""
    catlevel2Name = ""
    category_id = ""


    def __init__(self, uniqueId="", title="", price="", productDescription="", productImage="", catlevel1Name="", catlevel2Name="", category_id=""):
        self.uniqueId = uniqueId
        self.title = title
        self.price = price
        self.productDescription = productDescription
        self.productImage = productImage
        self.catlevel1Name = catlevel1Name
        self.catlevel2Name = catlevel2Name
        self.category_id = category_id
        

    """
        Converts product details from a product object to JSON format
    """
    def product_to_json(self):

        product_details = {}
        product_details['uniqueId'] = self.uniqueId
        product_details['title'] = self.title
        product_details['productDescription'] = self.productDescription
        product_details['price'] = self.price
        product_details['productImage'] = self.productImage

        return json.dumps(product_details)


    """
        Retrieves product detials from a single product belonging to a hierarchy of categories
        Returns: JSON object
    """
    def get_catalog_product_details(self):

        db = Database()

        # Validate presence of UniqueID in database
        product_exists_query = "SELECT EXISTS({});".format(GET_PRODUCT)
        product_exists = db.read_from_db(product_exists_query)
        
        # If read from database is empty, product does not exist
        if (product_exists[0]) == False:
            return "Error: Requested product not present in catalog"

        # Find corresponding product details from product table
        query_response = db.read_from_db(GET_PRODUCT+";", (str(self.uniqueId),))
        
        if "Error" in query_response or len(query_response)<=0:
            return query_response
        
        # Create a Product object
        self.title = query_response[0][1]
        self.productDescription = query_response[0][2]
        self.price = str(query_response[0][3])
        self.productImage= query_response[0][4]
        
        print("Product request processed")
        return self.product_to_json()


    """
        Retrieves product detials from a single product searched for 
        Returns: JSON object
    """
    def get_searched_product_details(self):
        unbxdAPI_obj=UnbxdAPI()
        product = Product(uniqueId=self.uniqueId)

        # Create URL using UniqueId of the requested product
        final_url=unbxdAPI_obj.url+'q=uniqueId '+self.uniqueId
        return unbxdAPI_obj.fetch_data_from_API(final_url)
        


    

        
 

