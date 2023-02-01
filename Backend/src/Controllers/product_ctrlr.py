from flask import Blueprint
import Models
from Models.product_servicing import Product

productsCtrlr = (Blueprint("products", __name__))

@productsCtrlr.route('/catalog/<string:uniqueId>', methods=['GET'])
def call_catalog_product_details(uniqueId):

    product = Product(uniqueId=uniqueId)

    details = product.get_catalog_product_details()

    return details

@productsCtrlr.route('/search/<string:uniqueId>', methods=['GET'])
def call_searched_product_details(uniqueId):

    product = Product(uniqueId=uniqueId)

    details = product.get_searched_product_details()

    return details




    





