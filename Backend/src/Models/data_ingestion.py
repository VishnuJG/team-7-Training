import Operations
from Operations.database import Database
from queries import *

class DataIngestor:

    def insert_product_in_db(self, product_json):

        db = Database()
        db.create_table(CREATE_PRODUCT_TABLE)
        db.create_table(CREATE_CATEGORY_TABLE)

        # params_list = ['uniqueId', 'title', 'price', 'productDescription', 'productImage', 'catlevel1Name', 'catlevel2Name']
        # product = Product()
        # product = product.validate_parameters(request, params_list)
        # product = Product(uniqueId=product_json['uniqueId'], title=product_json['title'], price=product_json)
        
        product_json['catlevel2Name'] = product_json['catlevel2Name'].strip()

        # Check if category ID for a hierarchy of cetegories already exists in category table
        cat_exists_res = db.read_from_db(CATEGORY_ID_EXISTS, (product_json['catlevel2Name'], product_json['catlevel1Name'],))
        # cur.execute(CATEGORY_ID_EXISTS, (product.catlevel2Name, product.catlevel1Name,))
        category_flag = cat_exists_res[0]

        # Create a new category ID in category table if not already exists
        if category_flag == False:
            db.write_to_db(INSERT_CATEGORY_ID, (product_json['catlevel2Name'], product_json['catlevel1Name'],))

        # Look up category ID for current hierarchy
        category_id_res = db.read_from_db(GET_CATEGORY_ID, (product_json['catlevel2Name'], product_json['catlevel1Name'],))
        # cur.execute(GET_CATEGORY_ID, (product_json['catlevel2Name'], product_json['catlevel1Name'],))
        category_id = category_id_res[0]

        # Insert details of current product into product table
        db.write_to_db(INSERT_PRODUCT, (product_json['uniqueId'], product_json['title'], product_json['productDescription'], product_json['price'], product_json['productImage'], category_id))

        print("Product inserted")
    

    def update_product_in_db(self, cur, request):
        pass
    
    
    def delete_product_in_db(self, cur, request):
        pass