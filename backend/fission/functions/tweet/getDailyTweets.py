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
    res = client.search(
      index="tweets",
      size=0,
      _source=["Datetime", "Sentiment"],
      aggs={
        "Date": {
          "date_histogram": {
            "field": "Datetime",
            "calendar_interval": "day"
          },
          "aggs": {
            "Sentiment": {
              "sum": {
                "field": "Sentiment"
              }
            }
          }
        }})

    current_app.logger.info(res["aggregations"])
    return {"result": res["aggregations"]}