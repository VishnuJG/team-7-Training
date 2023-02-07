from flask import Blueprint, request, Response
import json
import models
from models.data_ingestion import DataIngestor

ingestionCtrlr = (Blueprint("ingestion", __name__))

@ingestionCtrlr.route("/",methods=['POST'])
def ingest_data():
    data = request.get_json(force=True, cache=True)
    # print(data)
    ingestor = DataIngestor()

    for product in data:
        status = ingestor.insert_product_in_db(product)
        if "duplicate" in status:
            continue
        elif "Error" in status:
            return Response(json.dumps({
                    'status': 'server_error',
                    'error': status.split(":")[1].strip()
                }), status=500, mimetype='application/json')


    return Response(json.dumps({
                    'status': 'Success'
                }), status=200, mimetype='application/json')
    