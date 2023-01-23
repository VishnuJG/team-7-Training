from flask import Flask, render_template, url_for, request, redirect
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2
import json 
from queries import *


"""
    Connect to the database
    Args: None
    Returns: connection
"""

def get_db_connection():
    conn = psycopg2.connect(host='localhost',database='unbxddatabase',user='unbxd',password='unbxd')
    return conn


app = Flask(__name__)


"""
    Popoulate the databse with json objects. If tables do not exist, first create them according to a schema
    Args: List of JSON objects 
          keys: ['uniqueId', 'title', 'price', 'productDescription', 'productImage', 'catlevel1Name, 'catlevel2Name']
    Returns: None
"""

@app.route('/product-details', methods=['POST'])
def populate_db():
    data = request.get_json(force=True, cache=True)
    #   print("DATA", data)
    # print(data)
    conn = get_db_connection()
    cur = conn.cursor()

    # Create tables in the database
    cur.execute(CREATE_PRODUCT_TABLE)
    cur.execute(CREATE_CATEGORY_TABLE)
    product_no = 0

    # For each JSOn object, retrieve values for all keys
    for i in data: 
        # print("IIIIIII", i)
        uniqueId=i['uniqueId']
        # print("UNIQUE ID", uniqueId)
        title=i['title']
        price=i['price']
        try:
            description=i['productDescription']
        except:
            description=" "
        img_url=i['productImage']

        #Assign category ID
        catlevel1Name = i['catlevel1Name']
        try:
            catlevel2Name = i['catlevel2Name']
        except:
            catlevel2Name = " "

        #Remove spaces in the category names
        catlevel1Name = catlevel1Name.replace(" ", "")
        catlevel2Name = catlevel2Name.replace(" ", "")

        # Check if category ID for a hierarchy of cetegories already exists in category table
        cur.execute(CATEGORY_ID_EXISTS, (catlevel2Name, catlevel1Name,))
        category_flag = cur.fetchone()[0]

        # Create a new category ID in category table if not already exists
        if category_flag == False:
            cur.execute(INSERT_CATEGORY_ID, (catlevel2Name, catlevel1Name,))

        # Look up category ID for current hierarchy 
        cur.execute(GET_CATEGORY_ID, (catlevel2Name, catlevel1Name,))
        category_id = cur.fetchone()[0]

        # Insert details of current product into product table
        cur.execute(INSERT_PRODUCT, (uniqueId, title, description, price, img_url, category_id))
        print("Product {} inserted", product_no+1)

    # cur.execute(SELECT_ALL_PRODUCTS)
    # prods = cur.fetchall()
    # for i in prods:
    #     print (i)
    conn.commit()
    cur.close()
    conn.close()
    return "completed"


""" 
    Retrieve product details from database for a single product identified by a unique ID
    Args: str uniqueId
    Returns: dict product_details
"""

@app.route('/product-details', methods=['GET'])
def get_product_details():
    # Parse arguments from request 
    uniqueId = str(request.args.get("uniqueId"))
    conn = get_db_connection()
    cur = conn.cursor()

    # Find corresponding product details from product table
    cur.execute(GET_PRODUCT, (str(uniqueId),))
    query_response = cur.fetchall()

    product_details = {}
    
    try:
        title = query_response[0][1]
        # print(title)
        description = query_response[0][2]
        # print(description)
        price = str(query_response[0][3])
        imageurl = query_response[0][4]
    except:
        title = " "
        description = " "
        price = " "
        imageurl = " "
    
    # Create JSON object as response
    product_details['title'] = title
    product_details['description'] = description
    product_details['price'] = price
    product_details['imageurl'] = imageurl
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
    catlevel1Name = request.args.get('catlevel1Name')
    catlevel2Name = request.args.get('catlevel2Name')

    #Remove spaces in the category names
    catlevel1Name = catlevel1Name.replace(" ", "")
    catlevel2Name = catlevel2Name.replace(" ", "")

    category_products = []
    conn = get_db_connection()
    cur = conn.cursor()

    # Lookup category ID of corresponding hierarchy from category table
    cur.execute(GET_CATEGORY_ID, (catlevel2Name, catlevel1Name))
    # print(catlevel2Name, catlevel1Name)
    category_id = cur.fetchone()[0]

    # Check if the given hierarchy exists in database
    if type(category_id) == "NoneType":
        print("Invalid category")
    
    # Retrieve all rows having respective category ID from product table
    cur.execute(GET_CATEGORY_PRODUCTS, (category_id,))
    for product in cur.fetchall():
        # print(product)
        product_details = {}
        product_details['title'] = product[1]
        # product_details['description'] = product[2]
        product_details['price'] = product[3]
        product_details['imageurl'] = product[4]
        print(product_details)
        category_products.append(product_details)

    # print(category_products)
    return json.dumps(product_details)


@app.route('/delete/<string:id>')
def delete(id):
    pass


@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update(id):
    pass


if __name__ == "__main__":
    app.run(debug=True)