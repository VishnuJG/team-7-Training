from flask import Blueprint
from flask import Flask, request
import Models
from Models.search_servicing import Search


searchCtrlr = (Blueprint("product-search", __name__))

@searchCtrlr.route("/<string:search_term>", methods=['GET'])
def UNBXDAPISearch(search_term):
    
    res = Search( )
    print(request.args)
    return res.return_search_query(search_term, request)
    