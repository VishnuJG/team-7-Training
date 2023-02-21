import Operations
from Operations.database import Database
from queries import *

class DataIngestor:


    """
        Validates whether given parameters are present in the request object. 
        If not present, the respective field is filled with an empty string
        Args: request object 
              List of parameters to be validated
        Returns: Dataingestor object with placeholders in empty required fields
    """

    def validate_parameters(self, request, params_list):
        
        for param in params_list:

            # Check if parameter is present in request
            if param in request.keys():
                continue
            else:
                request[param]=""
        return self


    """
        Business logic to insert a single product in the database
        Args:  JSON object of product details
        Returns: Status message 

    """
    def insert_product_in_db(self, product_json):

        db = Database()

        # Create product and category tables if they dp not already exist
        status = db.create_table(CREATE_PRODUCT_TABLE)
        if "Error" in status:
            return status
        status = db.create_table(CREATE_CATEGORY_TABLE)
        if "Error" in status: 
            return status

        # Validate whether required arguments are present in the product JSON
        params_list = ['uniqueId', 'title', 'price', 'productDescription', 'productImage', 'catlevel1Name', 'catlevel2Name']
        self = self.validate_parameters(product_json, params_list)

        # UniqueID is a mandatory field to identify a product
        if product_json['uniqueId']=="":
            return "Error: Unique identifier is a required field "

        # Remove railing spaces in category names    
        try:
            product_json['catlevel2Name'] = product_json['catlevel2Name'].strip()
        except:
            product_json['catlevel2Name'] = " "

        # Check if category ID for a hierarchy of cetegories already exists in category table
        cat_exists_res = db.read_from_db(CATEGORY_ID_EXISTS, (product_json['catlevel2Name'], product_json['catlevel1Name'],))
        if "Error" in cat_exists_res:
            return cat_exists_res
        category_flag = cat_exists_res[0][0]

        # Create a new category ID in category table if not already exists
        if category_flag == False:
            status = db.write_to_db(INSERT_CATEGORY_ID, (product_json['catlevel2Name'], product_json['catlevel1Name'],))
            if "Error" in status:
                return status

        # Look up category ID for current hierarchy
        category_id_res = db.read_from_db(GET_CATEGORY_ID, (product_json['catlevel2Name'], product_json['catlevel1Name'],))
        if "Error" in category_id_res:
            return category_id_res
        category_id = category_id_res[0]

        # Insert details of current product into product table
        return db.write_to_db(INSERT_PRODUCT, (product_json['uniqueId'], product_json['title'], product_json['productDescription'], product_json['price'], product_json['productImage'], category_id))


    def update_product_in_db(self, cur, request):
        pass
    
    
    def delete_product_in_db(self, cur, request):
        pass