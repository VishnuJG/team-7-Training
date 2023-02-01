from flask import Blueprint, request
import Models
from Models.data_ingestion import DataIngestor

ingestionCtrlr = (Blueprint("ingestion", __name__))

@ingestionCtrlr.route("/",methods=['POST'])
def ingest_data():
    data = request.get_json(force=True, cache=True)
    # print(data)
    ingestor = DataIngestor()

    for product in data:
        ingestor.insert_product_in_db(product)
    return "Data ingested successfully"
    