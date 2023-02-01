from flask import Blueprint, request
import Models
from Models.category_servicing import Category, render_subcategory_names
categoryCtrlr = (Blueprint("category", __name__))


@categoryCtrlr.route("/",methods=['GET'])
def get_category_names():
    
    cat_names = render_subcategory_names()
    return cat_names

@categoryCtrlr.route("/category2-details/<string:catlevel1Name>/<string:catlevel2Name>", methods=['GET'])
def fetch_category1_products(catlevel1Name, catlevel2Name=None):

   
    cat_obj = Category(parent_name = catlevel1Name, subcategory_name = catlevel2Name) #need to send the params

    res = cat_obj.get_category_products(request)
    # print(res)

    return res


@categoryCtrlr.route("/category1-details/<string:catlevel1Name>", methods=['GET'])
def fetch_category2_products(catlevel1Name):

   
    cat_obj = Category(parent_name = catlevel1Name) #need to send the params

    res = cat_obj.get_category_products(request)
    # print(res)

    return res

