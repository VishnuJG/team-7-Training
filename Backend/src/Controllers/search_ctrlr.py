from flask import Blueprint
from flask import Flask, request
import Models
from Models.search_servicing import Search


searchCtrlr = (Blueprint("product-search", __name__))

@searchCtrlr.route("/", methods=['GET'])
def UNBXDAPISearch():
    
    res = Search( )
    print(request.args)
    return res.return_search_query(request)
    