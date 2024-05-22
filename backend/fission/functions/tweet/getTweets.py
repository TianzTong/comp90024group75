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
    
    # get matches from the range of time in VIC
    res = client.search(index="tweets", query={
        "bool": {
            "must": [
            {
                "match": {
                    "State": "Victoria"
                }
            },
            {
                "range": {
                    "Datetime": {
                        "gte": "2021-01-01 00:00:00",
                        "lte": "2021-09-31 00:00:00"
                    }
                }
            }
            ]
        }
    })
    
    current_app.logger.info(res["hits"])
    return {"result": res["hits"]}
    
    