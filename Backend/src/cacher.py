import sys
from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
sys.path.append('../')
import config

app = Flask(__name__)
CORS(app)
app.config.from_object('config.BaseConfig')  
cache = Cache(app)