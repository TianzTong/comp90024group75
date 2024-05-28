from elasticsearch8 import Elasticsearch
from flask import current_app, request


def main():
    # fetch the client
    client = Elasticsearch(
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs=False,
        ssl_show_warn=False,
        basic_auth=('elastic', 'elastic')
    )

    # get matches from the range of time in VIC
    res = client.search(index="asx", size=0, _source=["Date", "Price", "Change %"], aggs={
          
          "quarters": {
            "date_histogram": {
              "field": "Date",
              "calendar_interval": "quarter"
            },
            "aggs": {
              "Price_Average": {
                "avg": {
                  "field": "Price"
                }
              }
            }
          }
          
        })

    current_app.logger.info(res["aggregations"])
    return {"result": res["aggregations"]}
