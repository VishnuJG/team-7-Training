import operations, models
from operations.database import Database
from models.product_servicing import Product
from queries import *
import json


class Category():
    category_id = ""
    parent_name = ""
    subcategory_name = ""
    sort = ""
    page = "1"

    def __init__(self, category_id="", parent_name="", subcategory_name="", sort="", page="1"):
        self.category_id = category_id
        self.parent_name = parent_name
        self.subcategory_name = subcategory_name
        self.sort = sort
        self.page = page
        
    """
        Validation for the presence of query parameters in the database
        Args: list of keys to validate
        Returns: dict params_dict containing parsed values of parameters
    """

    def validate_parameters(self, request, params_list):
        
        for param in params_list:
            if param not in request.args:
                setattr(self, param, "")
            else:
                setattr(self, param, request.args.get(param))
                # self.param = request.args.get(param)
        # print(self.param)
        return self

        
        
    def get_l2_category_products(self):

        db = Database()
        category_products = [] 

        # Lookup category ID of corresponding hierarchy from category table
        
        self.category_id  = db.read_from_db(GET_CATEGORY_ID, (self.subcategory_name, self.parent_name))
        if len(self.category_id) < 1:
            return "Error: Invalid category"
        else:
            self.category_id = self.category_id[0]
        # print(self.catlevel2Name, self.catlevel1Name)

    
        # Retrieve all rows having respective category ID from product table
        products = db.read_from_db(GET_CATEGORY_PRODUCTS, (self.category_id,))
        # cur.execute(GET_CATEGORY_PRODUCTS, (self.category_id,))
        # print(products)
        for product in products:
            
            
            product_details = Product(uniqueId=product[0], productDescription=product[2], title=product[1], price=product[3], productImage=product[4])
            
            product_details = json.loads(product_details.product_to_json())
            
            category_products.append(product_details)
        
        return category_products


    def get_l1_category_products(self):

        db = Database()
        category_products = [] 
        # caetgory_flag = db.read_from_db(CATEGORY_ID_EXISTS, (cat))
        ids = db.read_from_db(GET_CATEGORY_L1, (self.parent_name,))
        print(ids)
        print(type(ids))
        
        # Check if the given hierarchy exists in database
        if len(ids) < 1:
            return "Error: Invalid category"
        # print(ids)

        for category_id in ids:
            # print(category_id)
            products = db.read_from_db(GET_CATEGORY_PRODUCTS, (category_id,))

            for product in products:
                product_details = Product(uniqueId=product[0], productDescription=product[2], title=product[1], price=product[3], productImage=product[4])
                product_details = json.loads(product_details.product_to_json())
                category_products.append(product_details)

        return category_products


    def get_category_products(self, request):

        params_list = ['sort', 'page']
        # category = Category()
        self = self.validate_parameters(request, params_list)

        # print(self.subcategory_name)
        if self.subcategory_name == "":
            category_products = self.get_l1_category_products()
        else:
            category_products = self.get_l2_category_products()

        if "Error" in category_products:
            return category_products

        num_products = len(category_products)
        # print(num_products)


        # sort product list if sort parameter is present 
        if(self.sort is not None and len(self.sort) > 0):
            # sort based on price in ascending order
            if "asc" in self.sort:
                category_products = sorted(category_products, key=lambda product: float(product['price']))
            # sort based on price in descending order
            elif "desc" in self.sort:
                print(type(category_products[0]))
                category_products = sorted(category_products, key=lambda product: float(product['price']), reverse=True)
        # print(self.page)
        # display 10 product at a time on a page
        
        if num_products >= (int(self.page)*10):
            return [num_products, category_products[(int(self.page)*10)-10: int(self.page)*10]]
        # if a non-existent page number is requested 
        elif (int(self.page)-1)*10 > num_products:
            return [0, []]
        # last page of products which does displays less than 10 products
        else:
            return [num_products, category_products[(int(self.page)*10)-10:]]


def render_subcategory_names():
    db = Database()
    
    men_categories = []
    women_categories = []

    # get the subcategories under men
    data = db.read_from_db(GET_SUBCATEGORY_NAMES, ("men",))
    if len(data) < 1:
        return "Error: No subcategories available"
    # cur.execute(GET_SUBCATEGORY_NAMES, ("men",))
    for subcategory in data:
        if subcategory[0] != "":
            men_categories.append(subcategory[0])
    
    # get the subcategories under women
    data = db.read_from_db(GET_SUBCATEGORY_NAMES, ("women",))
    if len(data) < 1:
        return "Error: No subcategories available"
    for subcategory in data:
        if subcategory[0] != "":
            women_categories.append(subcategory[0])

    return {"men": men_categories, "women": women_categories}


# a = Category(parent_name="men", subcategory_name="New Arrivals")
# a.get_category_products()





