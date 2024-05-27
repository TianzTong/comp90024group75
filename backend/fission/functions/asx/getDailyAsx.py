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
    res = client.search(index="asx",size=1000,_source=["Date", "Price", "Change %"],query={
      "bool": {
        "must": [
          {
            "range": {
              "Date": {
                "gte": "2021-06-21",
                "lte": "2022-06-04"
              }
            }
          }
        ]
      }
    })

    current_app.logger.info(res["hits"])
    return {"result": res["hits"]}
