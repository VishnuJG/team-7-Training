from flask import Blueprint, request, Response
import json
# import models
import sys

sys.path.append('../')
from recommendation.contentBased import ContentBasedRecommender
from cacher import cache
from Models.category_servicing import Category, render_subcategory_names
recommendationCtrlr = (Blueprint("recommendation", __name__))


# Retrieve names of all subcategories pressent under all parents categories
@recommendationCtrlr.route("/<string:uniqueID>",methods=['GET'])
def get_category_names(uniqueID):

    
    temp = ContentBasedRecommender()
    # print(temp.recommender(uniqueID))
    return temp.recommender(uniqueID)

