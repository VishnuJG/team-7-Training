from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
import sys
sys.path.append('..')
from cacher import app
from flask import Blueprint
from controllers.product_ctrlr import productsCtrlr
from controllers.category_ctrlr import categoryCtrlr
from controllers.search_ctrlr import searchCtrlr
from controllers.data_ingestion_ctrlr import ingestionCtrlr

app.register_blueprint(productsCtrlr, url_prefix = "/products")
app.register_blueprint(categoryCtrlr, url_prefix = "/category")
app.register_blueprint(searchCtrlr, url_prefix = "/search")
app.register_blueprint(ingestionCtrlr, url_prefix = "/ingestion")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)