import json
import requests

with open('data/out.json') as f:
   data = json.load(f)

url = "http://127.0.0.1:5000/product-details"
headers = {'Content-type': 'application/json'}
r = requests.post(url, data=json.dumps(data), headers=headers)