import operations
from operations.database import Database
from queries import *

class DataIngestor:

    def validate_parameters(self, request, params_list):
        
        for param in params_list:
            if param in request.keys():
                continue
            else:
                request[param]=""
        return self

    def insert_product_in_db(self, product_json):

        db = Database()
        status = db.create_table(CREATE_PRODUCT_TABLE)
        if "Error" in status:
            return status
        status = db.create_table(CREATE_CATEGORY_TABLE)
        if "Error" in status: 
            return status

        params_list = ['uniqueId', 'title', 'price', 'productDescription', 'productImage', 'catlevel1Name', 'catlevel2Name']
        self = self.validate_parameters(product_json, params_list)
        if product_json['uniqueId']=="":
            return "Error: Unique identifier is a required field "
            
        # product = Product(uniqueId=product_json['uniqueId'], title=product_json['title'], price=product_json)
        try:
            product_json['catlevel2Name'] = product_json['catlevel2Name'].strip()
        except:
            product_json['catlevel2Name'] = " "

        # Check if category ID for a hierarchy of cetegories already exists in category table
        cat_exists_res = db.read_from_db(CATEGORY_ID_EXISTS, (product_json['catlevel2Name'], product_json['catlevel1Name'],))
        if "Error" in cat_exists_res:
            return cat_exists_res
        # cur.execute(CATEGORY_ID_EXISTS, (product.catlevel2Name, product.catlevel1Name,))
        category_flag = cat_exists_res[0][0]
        # print(category_flag)
        # Create a new category ID in category table if not already exists
        if category_flag == False:
            status = db.write_to_db(INSERT_CATEGORY_ID, (product_json['catlevel2Name'], product_json['catlevel1Name'],))
            if "Error" in status:
                return status

        # Look up category ID for current hierarchy

        category_id_res = db.read_from_db(GET_CATEGORY_ID, (product_json['catlevel2Name'], product_json['catlevel1Name'],))
        if "Error" in category_id_res:
            return category_id_res
        # cur.execute(GET_CATEGORY_ID, (product_json['catlevel2Name'], product_json['catlevel1Name'],))

        category_id = category_id_res[0]

        # Insert details of current product into product table
        return db.write_to_db(INSERT_PRODUCT, (product_json['uniqueId'], product_json['title'], product_json['productDescription'], product_json['price'], product_json['productImage'], category_id))
     
        
    

    def update_product_in_db(self, cur, request):
        pass
    
    
    def delete_product_in_db(self, cur, request):
        pass