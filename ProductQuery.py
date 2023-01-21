from flask import Flask, url_for, request, jsonify
from datetime import datetime
import requests
import json
from flask_cors import CORS

app=Flask(__name__)
CORS(app)


@app.route('/product-query')
def productQuery():
    final_url="https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?"

    for param in request.args:
        final_url+="{}={}&".format(param, request.args[param])

    print(final_url)    
    

    # unbxd_val = requests.get('https://search.unbxd.io/fb853e3332f2645fac9d71dc63e09ec1/demo-unbxd700181503576558/search?q={}&page={}&sort={}'.format(query_val, page_val, sort_operation)).content
    unbxd_val = requests.get(final_url).content
    unbxd_val = json.loads(unbxd_val)
    # print(unbxd_val)
    return [unbxd_val['response']['numberOfProducts'], unbxd_val['response']['products']]



if __name__ == "__main__":
    app.run(debug=True)