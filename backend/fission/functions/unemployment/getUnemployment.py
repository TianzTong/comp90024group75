from elasticsearch8 import Elasticsearch
from flask import current_app, request

def main():
    
    # fetch the client
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs= False,
        ssl_show_warn= False,
        basic_auth=('elastic', 'elastic')
    )
    res = client.search(index="unemployment", query={
        "match_all": {}
    })
    
    current_app.logger.info(res["hits"])
    return {"result": res["hits"]}
    
    