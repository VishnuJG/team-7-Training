from flask import Blueprint, request, Response
import json
# import models
import sys

sys.path.append('../')

from cacher import cache
from Models.category_servicing import Category, render_subcategory_names
categoryCtrlr = (Blueprint("category", __name__))


# Retrieve names of all subcategories pressent under all parents categories
@categoryCtrlr.route("/",methods=['GET'])
def get_category_names():
    
    cat_names = render_subcategory_names()
    
    if "Error" in cat_names:
        return Response(json.dumps({
                    'status': 'server_error',
                    'error': 'Cannot render subcategory names'
                }), status=500, mimetype='application/json')
    return cat_names


# Retrieves all products present in a a hierarchy of level 1 and level 2 categories
@categoryCtrlr.route("/<string:catlevel1Name>/<string:catlevel2Name>", methods=['GET'])
@cache.cached(timeout=30, query_string=True)
def fetch_category2_products(catlevel1Name, catlevel2Name=None):

   
    cat_obj = Category(parent_name = catlevel1Name, subcategory_name = catlevel2Name) #need to send the params
    res = cat_obj.get_category_products(request)

    if "Error" in res:
        return Response(json.dumps({
                    'status': 'server_error',
                    'error': 'Invalid subcategory'
                }), status=500, mimetype='application/json')
    return res


# Retrieves all products present in a single level 1 category
@categoryCtrlr.route("/<string:catlevel1Name>", methods=['GET'])
@cache.cached(timeout=30, query_string=True)
def fetch_category1_products(catlevel1Name):

   
    cat_obj = Category(parent_name = catlevel1Name) 
    res = cat_obj.get_category_products(request)

    if "Error" in res:
        return Response(json.dumps({
                    'status': 'server_error',
                    'error': 'Invalid category'
                }), status=500, mimetype='application/json')
    return res

