from elasticsearch8 import Elasticsearch
from flask import current_app, request


def main():
    # fetch the client
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic'))
    
    # query the ES
    res = client.search(
        index="tweets",
        size=0,
        _source=["State", "Sentiment"],
        query={
            "bool": {
            "must": [
                {
                "range": {
                    "Datetime": {
                    "gte": "2021-06-01 00:00:00",
                    "lte": "2021-09-01 00:00:00"
                    }
                }
                }
            ]
            }
        },
        aggs={
            "State": {
            "terms": {
                "field": "State",
                "include": ["Australian Capital Territory", "New South Whales", "Northern Territory", "Queensland", "South Australia", "Tasmania", "Victoria", "Western Australia"]
            },
            "aggs": {
                "Sentiment": {
                "sum": {
                    "field": "Sentiment"
                }
                }
            }
            }
        }
    )
    
        
    current_app.logger.info(res["aggregations"])
    return {"result": res["aggregations"]}