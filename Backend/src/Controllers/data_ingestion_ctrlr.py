from flask import Blueprint, request, Response
import json
import os
import Models
from Models.data_ingestion import DataIngestor

ingestionCtrlr = (Blueprint("ingestion", __name__))

# Insert a single product in the database
@ingestionCtrlr.route("/",methods=['POST'])
def ingest_data():

    data = request.get_json(force=True, cache=True)
    ingestor = DataIngestor()

    for product in data:
        status = ingestor.insert_product_in_db(product)

        # If a uniqueId is already present in the database, do not insert that product
        if "duplicate" in status:
            continue

        elif "Error" in status:
            return Response(json.dumps({
                    'status': 'server_error',
                    'error': status.split(":")[1].strip()
                }), status=500, mimetype='application/json')

    try:
        os.remove('./processedDF.pkl')
    except:
        print("PKL file does not exist")
    return Response(json.dumps({
                    'status': 'Success'
                }), status=200, mimetype='application/json')
    