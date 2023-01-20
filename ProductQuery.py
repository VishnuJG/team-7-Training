from flask import Flask, url_for, request, jsonify
from datetime import datetime
import requests
import json
from flask_cors import CORS

app=Flask(__name__)
CORS(app)


@app.route('/product-query')
def productQuery():
    query_val = request.args.get('q', default="", type=str)
    page_val = request.args.get('page', default="1", type = str)
    unbxd_val = requests.get('https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?q={}&page={}'.format(query_val, page_val)).content
    unbxd_val = json.loads(unbxd_val)
    
    return [unbxd_val['response']['numberOfProducts'], unbxd_val['response']['products']]



if __name__ == "__main__":
    app.run(debug=True)