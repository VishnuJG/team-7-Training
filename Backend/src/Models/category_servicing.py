import Operations, Models
from Operations.database import Database
from Models.product_servicing import Product
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

    
    """
        Helper function for get_category_products()
        Retrieves all products present in a a hierarchy of level 1 and level 2 categories
        Returns: list of JSON objects 
    """
        
    def get_l2_category_products(self):

        db = Database()
        category_products = [] 

        # Lookup category ID of corresponding hierarchy from category table
        self.category_id  = db.read_from_db(GET_CATEGORY_ID, (self.subcategory_name, self.parent_name))
        if len(self.category_id) < 1:
            return "Error: Invalid category"
        else:
            self.category_id = self.category_id[0]
    
        # Retrieve all rows having respective category ID from product table
        products = db.read_from_db(GET_CATEGORY_PRODUCTS, (self.category_id,))

        for product in products:
            product_details = Product(uniqueId=product[0], productDescription=product[2], title=product[1], price=product[3], productImage=product[4])
            product_details = json.loads(product_details.product_to_json())
            category_products.append(product_details)
        
        return category_products


    """
        Helper function for get_category_products()
        Retrieves all products present in a single level 1 category
        Returns: list of JSON objects containing all products 
    """
    def get_l1_category_products(self):

        db = Database()
        category_products = [] 
        # Retrieve all category IDs which have a particular parent category
        ids = db.read_from_db(GET_CATEGORY_L1, (self.parent_name,))
        print(ids)
        print(type(ids))
        
        # Check if the given hierarchy exists in database
        if len(ids) < 1:
            return "Error: Invalid category"
        # print(ids)

        for category_id in ids:
            # Retrieve products in each subcategory which has a particular parent category
            products = db.read_from_db(GET_CATEGORY_PRODUCTS, (category_id,))

            for product in products:
                product_details = Product(uniqueId=product[0], productDescription=product[2], title=product[1], price=product[3], productImage=product[4])
                product_details = json.loads(product_details.product_to_json())
                category_products.append(product_details)

        return category_products


    """
        Retrieves products present in a category or a hierarchy of categories for a paricular page number
        Args: request object received by the View
        Returns: list 
                 First element is the total number of products
                 Second element is a list of JSON objects to be rendered on a particular page 
    """

    def get_category_products(self, request):

        params_list = ['sort', 'page']
        # Validate whether parameters in the request actually exist
        self = self.validate_parameters(request, params_list)

        # Check whether category hierarchy level is 1 or 2
        if self.subcategory_name == "":
            category_products = self.get_l1_category_products()
        else:
            category_products = self.get_l2_category_products()

        if "Error" in category_products:
            return category_products

        num_products = len(category_products)

        # sort product list if sort parameter is present 
        if(self.sort is not None and len(self.sort) > 0):

            # sort based on price in ascending order
            if "asc" in self.sort:
                category_products = sorted(category_products, key=lambda product: float(product['price']))
            # sort based on price in descending order
            elif "desc" in self.sort:
                print(type(category_products[0]))
                category_products = sorted(category_products, key=lambda product: float(product['price']), reverse=True)

        # display 10 product at a time on a page        
        if num_products >= (int(self.page)*10):
            return [num_products, category_products[(int(self.page)*10)-10: int(self.page)*10]]

        # if a non-existent page number is requested 
        elif (int(self.page)-1)*10 > num_products:
            return [0, []]

        # last page of products which does displays less than 10 products
        else:
            return [num_products, category_products[(int(self.page)*10)-10:]]


"""
    Retrieve names of all subcategories pressent under all parents categories
    Returns: Dictionary 
             keys are parent category names
             Values are a list of subcategory names
"""
def render_subcategory_names():

    db = Database()
    
    men_categories = []
    women_categories = []

    # get the subcategories under men
    data = db.read_from_db(GET_SUBCATEGORY_NAMES, ("men",))
    if len(data) < 1:
        return "Error: No subcategories available"

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