from flask import Flask, request, jsonify, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
# from flask_restful import Resource, Api
import os


app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))

# api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Product(db.Model):
    uniqueId = db.Column(db.String(32), primary_key=True)
    title = db.Column(db.String(32), unique=True)
    price = db.Column(db.Integer)
    image_url = db.Column(db.String(64))
    colour = db.Column(db.String(32))
    size = db.Column(db.String(32))
    category_type = db.Column(db.String(32))
    description = db.Column(db.String(128))


    def __init__(self, uniqueId, title, price, image_url, colour, size, category_type, description):
        self.uniqueId = uniqueId
        self.title = title
        self.price = price
        self.image_url = image_url
        self.colour = colour
        self.size = size
        self.category_type = category_type
        self.description = description


    def test_connection(self):
        with app.app_context():
            self.__init__()

class ProductSchema(ma.Schema):
    class Meta: 
        fields = ('uniqueId', 'title', 'price', 'image_url', 'colour', 'size', 'category_type', 'description')

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Create a Product
@app.route('/product', methods=['POST'])
def add_product():
  uniqueId = request.json['uniqueId']
  title = request.json['title']
  price = request.json['price']
  image_url = request.json['image_url']
  colour = request.json['colour']
  size = request.json['size']
  category_type = request.json['category_type']
  description = request.json['description']

  new_product = Product(uniqueId, title, price, image_url, colour, size, category_type, description)

  db.session.add(new_product)
  db.session.commit()

  return product_schema.jsonify(new_product)

# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result.data)

# Get Single Products
@app.route('/product/<uniqueId>', methods=['GET'])
def get_product(uniqueId):
  product = Product.query.get(uniqueId)
  return product_schema.jsonify(product)

# Update a Product
@app.route('/product/<uniqueId>', methods=['PUT'])
def update_product(uniqueId):
  product = Product.query.get(uniqueId)

  uniqueId = request.json['uniqueId']
  title = request.json['title']
  price = request.json['price']
  image_url = request.json['image_url']
  colour = request.json['colour']
  size = request.json['size']
  category_type = request.json['category_type']
  description = request.json['description']

  product.uniqueId = uniqueId
  product.title = title
  product.price = price
  product.image_url = image_url
  product.colour = colour
  product.size = size
  product.category_type = category_type
  product.description = description

  db.session.commit()

  return product_schema.jsonify(product)

# Delete Product
@app.route('/product/<uniqueId>', methods=['DELETE'])
def delete_product(uniqueId):
  product = Product.query.get(uniqueId)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)

# Run Server
if __name__ == '__main__':
  app.run(debug=True)

