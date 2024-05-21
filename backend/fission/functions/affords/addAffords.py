import logging, json
from flask import current_app, request
from elasticsearch8 import Elasticsearch

def main():
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        ssl_show_warn= False,
        basic_auth=('elastic', 'elastic')
    )

    
    res = client.index(
        
        index='affords',
        id=request.headers['X-Fission-Params-Id'],
        body=request.get_json(force=True)
    )
        
    return 'ok'
