from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import psycopg2
import json
from queries import *
from flask_cors import CORS
import requests
from flask_caching import Cache

app = Flask(__name__)
CORS(app)
app.config.from_object('config.BaseConfig')  
cache = Cache(app)


"""
    Connect to the database
    Args: None
    Returns: connection
"""

def get_db_connection():
    conn = psycopg2.connect(database='unbxddatabase',user='unbxd',password='unbxd', host="backend-database-1")
    return conn



"""
    Popoulate the databse with json objects. If tables do not exist, first create them according to a schema
    Args: List of JSON objects
          keys: ['uniqueId', 'title', 'price', 'productDescription', 'productImage', 'catlevel1Name, 'catlevel2Name']
    Returns: None
"""

@app.route('/product-details', methods=['POST'])
def populate_db():

    data = request.get_json(force=True, cache=True)
    conn = get_db_connection()
    cur = conn.cursor()

    # Create tables in the database
    cur.execute(CREATE_PRODUCT_TABLE)
    cur.execute(CREATE_CATEGORY_TABLE)
    product_no = 0

    # For each JSON object, retrieve values for all keys
    for product in data:

        # Validate whether each key is present in the JSON request
        try:
            uniqueId = product['uniqueId']
        except:
            pass
        try:
            title = product['title']
        except:
            title = ""
        try:
            price = product['price']
        except:
            price = ""
        try:
            description = product['productDescription']
        except:
            description = ""
        try:
            img_url = product['productImage']
        except:
            img_url = ""
        try:
            catlevel1Name = product['catlevel1Name']
        except:
            catlevel1Name = ""
        try:
            catlevel2Name = product['catlevel2Name']
            # catlevel2Name = catlevel2Name.replace("&", "and")
        except:
            catlevel2Name = ""

        #Remove spaces in the category names
        # catlevel1Name = catlevel1Name.replace(" ", "")
        # catlevel2Name = catlevel2Name.replace(" ", "")

        catlevel2Name=catlevel2Name.strip()

        # Check if category ID for a hierarchy of cetegories already exists in category table
        cur.execute(CATEGORY_ID_EXISTS, (catlevel2Name, catlevel1Name,))
        category_flag = cur.fetchone()[0]
        
        # Create a new category ID in category table if not already exists
        if not category_flag:
            print(category_flag)
            cur.execute(INSERT_CATEGORY_ID, (catlevel2Name, catlevel1Name,))

        # Look up category ID for current hierarchy
        cur.execute(GET_CATEGORY_ID, (catlevel2Name, catlevel1Name,))
        category_id = cur.fetchone()[0]

        # Insert details of current product into product table
        cur.execute(INSERT_PRODUCT, (uniqueId, title, description, price, img_url, category_id))
        product_no += 1

        # print("Product " + str(product_no) + " inserted")

    # cur.execute(SELECT_ALL_PRODUCTS)
    # prods = cur.fetchall()
    # for product in prods:
    #     print (product)

    conn.commit()
    cur.close()
    conn.close()
    return "Product(s) inserted into database"


"""
    Retrieve product details from database for a single product identified by a unique ID
    Args: str uniqueId
    Returns: dict product_details
"""

@app.route('/product-details', methods=['GET'])
@cache.cached(timeout=30, query_string=True)
def get_product_details():

    # Parse arguments from request
    uniqueId = str(request.args.get("uniqueId"))
    conn = get_db_connection()
    cur = conn.cursor()

    # Validate presence of UniqueID in database
    product_exists_query = "SELECT EXISTS({});".format(GET_PRODUCT)
    cur.execute(product_exists_query, (uniqueId,))
    if (cur.fetchone()[0]) == False:
        return "Requested product not present in catalog"

    # Find corresponding product details from product table
    cur.execute(GET_PRODUCT+";", (str(uniqueId),))
    query_response = cur.fetchall()

    # Create JSON object as response
    product_details = {}
    product_details['title'] = query_response[0][1]
    product_details['description'] = query_response[0][2]
    product_details['price'] = str(query_response[0][3])
    product_details['imageurl'] = query_response[0][4]
    print("Product request processed")
    return json.dumps(product_details)


"""
    Filters and retrieves all products as a list of JSOn objects belonging to a hierarchy of categories from the database
    Args: str catlevel1Name
          str catlevel2Name
    Returns: list product_details
"""

@app.route('/category', methods=['GET'])
def get_category_products():

    # Parse arguments from request
    # Validate that category level 1 name is present in request
    try:
        catlevel1Name = request.args.get('cat1')
    except:
        return "Invalid category. Request does not contain top level category"
    try:
        catlevel2Name = request.args.get('cat2')
    except:
        catlevel2Name = ""
    try:
        sort = request.args.get('sort')
    except:
        sort = ""
    try:
        page = int(request.args.get('page'))
    except:
        page = ""

    category_products = []
    conn = get_db_connection()
    cur = conn.cursor()

    # Lookup category ID of corresponding hierarchy from category table
    cur.execute(GET_CATEGORY_ID, (catlevel2Name, catlevel1Name))
    print(catlevel2Name, catlevel1Name)
    category_id = cur.fetchone()[0]

    # Check if the given hierarchy exists in database
    if len(str(category_id)) < 1:
        return "Invalid category"

    # Retrieve all rows having respective category ID from product table
    cur.execute(GET_CATEGORY_PRODUCTS, (category_id,))

    for product in cur.fetchall():
        # print(product)
        product_details = {}
        product_details['uniqueId'] = product[0]
        product_details['title'] = product[1]
        # product_details['description'] = product[2]
        product_details['price'] = product[3]
        product_details['productImage'] = product[4]
        # print(product_details)
        # product_details = json.dumps(product_details)
        category_products.append(product_details)
    # print(category_products)
    # num_products = 100
    num_products = len(category_products)
    print(num_products)

    # sort product list if sort parameter is present 
    if(sort is not None and len(sort) > 0):
        # sort based on price in ascending order
        if "asc" in sort:
            category_products = sorted(category_products, key=lambda product: float(product['price']))
        # sort based on price in descending order
        elif "desc" in sort:
            category_products = sorted(category_products, key=lambda product: float(product['price']), reverse=True)

    # display 10 product at a time on a page
    if num_products >= (page*10):
        return [num_products, category_products[page*10-10: page*10]]
    # if a non-existent page number is requested 
    elif (page-1)*10 > num_products:
        return [0, []]
    # last page of products which does displays less than 10 products
    else:
        return [num_products, category_products[page*10-10:]]



# @app.route('/product-details', methods=['DELETE'])
# def delete_product():

#     # Parse arguments from request
#     uniqueId = str(request.args.get("uniqueId"))
#     conn = get_db_connection()
#     cur = conn.cursor()

#     # Validate presence of UniqueID in database
#     product_exists_query = "SELECT EXISTS({});".format(GET_PRODUCT)
#     cur.execute(product_exists_query, (uniqueId,))
#     if (cur.fetchone()[0]) == False:
#         return "Product already deleted from catalog"

#     cur.execute(GET_CATEGORY_ID, (uniqueId,))
#     category_id = cur.fetchone()[0]
#     cur.execute(DELETE_PRODUCT, (uniqueId,))
#     cur.execute(OTHER_CATEGORY_PRODUCT_EXISTS, (category_id,))
#     category_exists = cur.fetchone()[0]
#     if  category_exists == False:
#         cur.execute(DELETE_CATEGORY, (category_id,))

#     return "Product deleted from table"

    
# @app.route('/update/<string:id>', methods=['PUT'])
# def update_product():
#     pass


@app.route('/subcategory-names', methods=['GET'])
def render_subcategory_names():

    conn = get_db_connection()
    cur = conn.cursor()
    men_categories = []
    women_categories = []

    # get the subcategories under men
    cur.execute(GET_SUBCATEGORY_NAMES, ("men",))
    for subcategory in cur.fetchall():
        if subcategory[0] != "":
            men_categories.append(subcategory[0])
    
    # get the subcategories under women
    cur.execute(GET_SUBCATEGORY_NAMES, ("women",))
    for subcategory in cur.fetchall():
        if subcategory[0] != "":
            women_categories.append(subcategory[0])
    return {"men": men_categories, "women": women_categories}


@app.route('/product-search')
@cache.cached(timeout=30, query_string=True)
def productQuery():

    final_url="https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?"
    for param in request.args:
        final_url+="{}={}&".format(param, request.args[param])
        
    # unbxd_val = requests.get('https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?q={}&page={}&sort={}'.format(query_val, page_val, sort_operation)).content
    unbxd_val = requests.get(final_url).content
    unbxd_val = json.loads(unbxd_val)
    return [unbxd_val['response']['numberOfProducts'], unbxd_val['response']['products']]


@app.route('/')
def hello():
    return 'Hello World! I have been seen'


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
