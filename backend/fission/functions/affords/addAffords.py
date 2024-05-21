from elasticsearch8 import Elasticsearch
from flask import current_app, request
import pandas as pd
import scipy as sc
import numpy as np

def main():
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        ssl_show_warn= False,
        basic_auth=('elastic', 'elastic')
    )
      
    jsonSend = request.get_json(force=True)
    res = client.index(
        
        index='affords',
        id=request.headers['X-Fission-Params-Id'],
        document=jsonSend
    )
    test = request.headers['X-Fission-Params-Id']
    return { "Result":res['result'], "id": test}