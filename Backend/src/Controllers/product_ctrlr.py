from flask import Blueprint, Response
import json
import Models
from Models.product_servicing import Product

productsCtrlr = (Blueprint("products", __name__))


# Retrieves product detials from a single product belonging to a hierarchy of categories
@productsCtrlr.route('/cat=<string:uniqueId>', methods=['GET'])
def call_catalog_product_details(uniqueId):

    product = Product(uniqueId=uniqueId)

    details = product.get_catalog_product_details()

    if "Error" in details:
        return Response(json.dumps({
                    'status': 'server_error',
                    'error': 'Product does not exist'+str(details)
                }), status=500, mimetype='application/json')

    return details


# Retrieves product detials from a single product searched for 
@productsCtrlr.route('/ser=<string:uniqueId>', methods=['GET'])
def call_searched_product_details(uniqueId):

    product = Product(uniqueId=uniqueId)

    details = product.get_searched_product_details()

    return details




    





