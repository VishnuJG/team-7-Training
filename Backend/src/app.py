from flask import Flask
from flask_cors import CORS
# from flask_caching import Cache

from flask import Blueprint
from Controllers.product_ctrlr import productsCtrlr
from Controllers.category_ctrlr import categoryCtrlr
from Controllers.search_ctrlr import searchCtrlr
from Controllers.data_ingestion_ctrlr import ingestionCtrlr

app = Flask(__name__)
CORS(app)
# app.config.from_object('config.BaseConfig')  
# cache = Cache(app)

app.register_blueprint(productsCtrlr, url_prefix = "/products")
app.register_blueprint(categoryCtrlr, url_prefix = "/category")
app.register_blueprint(searchCtrlr, url_prefix = "/product-search")
app.register_blueprint(ingestionCtrlr, url_prefix = "/ingestion")



if __name__ == "__main__":
    app.run(debug=True)