from flask import Flask, render_template, url_for, request, redirect
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2
import json 
from queries import *


def get_db_connection():
    conn = psycopg2.connect(host='localhost',database='unbxddatabase',user='unbxd',password='unbxd')
    return conn

app = Flask(__name__)

@app.route('/product-details', methods=['POST'])
def populate_db():
    data = request.get_json(force=True, cache=True)
    #   print("DATA", data)
    # print(data)
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(CREATE_PRODUCT_TABLE)
    #   cur.execute(CREATE_CATEGORY_TABLE)
    product_no = 0
    for i in data: 
        # print("IIIIIII", i)
        uniqueId=i['uniqueId']
        # print("UNIQUE ID", uniqueId)
        title=i['title']
        price=i['price']
        try:
            description=i['productDescription']
        except:
            description=""
        img_url=i['productImage']
        cur.execute("INSERT INTO product_table (uniqueId, title, description, price, image_url) VALUES(%s, %s, %s, %s, %s);", (uniqueId, title, description, price, img_url))
        print("Product {} inserted", product_no+1)
    cur.execute(SELECT_ALL_PRODUCTS)
    prods = cur.fetchall()
    for i in prods:
        print (i)
    conn.commit()
    cur.close()
    conn.close()
    return "completed"

    #   return render_template('index.html')


# @app.get("/product-details/<string:uniqueID>")
@app.route('/product-details', methods=['GET'])
def find_product_details():
  uniqueId = request.args.get('uniqueId')
  product_details = {}
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute(GET_PRODUCT, (uniqueId))
  title = cur.fetchone()[1]
  description = cur.fetchone()[2]
  price = cur.fetchone()[3]
  imageurl = cur.fetchone()[4]
  product_details['title'] = title
  product_details['description'] = description
  product_details['price'] = price
  product_details['imageurl'] = imageurl
  return json.dumps(product_details)


# @app.route('/product-details', methods=['GET'])
# def get_cetegory_products():
#   catlevel1Name = request.args.get()






@app.route('/delete/<string:id>')
def delete(id):
    pass

@app.route('/update/<string:id>', methods=['GET', 'POST'])
def update(id):
    pass

if __name__ == "__main__":
    app.run(debug=True)