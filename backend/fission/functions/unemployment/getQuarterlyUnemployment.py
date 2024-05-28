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
        index="unemployment",
        _source={"excludes": ["fid", "lga_name_2021_asgs"]},
        size=0,
        aggs={
              "Q1-2011": {
                "sum": {"field": "mar_11"}
              },
              "Q1-2012": {
                "sum": {"field": "mar_12"}
              },
              "Q1-2013": {
                "sum": {"field": "mar_13"}
              },
              "Q1-2014": {
                "sum": {"field": "mar_14"}
              },
              "Q1-2015": {
                "sum": {"field": "mar_15"}
              },
              "Q1-2016": {
                "sum": {"field": "mar_16"}
              },
              "Q1-2017": {
                "sum": {"field": "mar_17"}
              },
              "Q1-2018": {
                "sum": {"field": "mar_18"}
              },
              "Q1-2019": {
                "sum": {"field": "mar_19"}
              },
              "Q1-2020": {
                "sum": {"field": "mar_20"}
              },
              "Q1-2021": {
                "sum": {"field": "mar_21"}
              },
              "Q2-2011": {
                "sum": {"field": "jun_11"}
              },
              "Q2-2012": {
                "sum": {"field": "jun_12"}
              },
              "Q2-2013": {
                "sum": {"field": "jun_13"}
              },
              "Q2-2014": {
                "sum": {"field": "jun_14"}
              },
              "Q2-2015": {
                "sum": {"field": "jun_15"}
              },
              "Q2-2016": {
                "sum": {"field": "jun_16"}
              },
              "Q2-2017": {
                "sum": {"field": "jun_17"}
              },
              "Q2-2018": {
                "sum": {"field": "jun_18"}
              },
              "Q2-2019": {
                "sum": {"field": "jun_19"}
              },
              "Q2-2020": {
                "sum": {"field": "jun_20"}
              },
              "Q2-2021": {
                "sum": {"field": "jun_21"}
              },
              "Q3-2011": {
                "sum": {"field": "sep_11"}
              },
              "Q3-2012": {
                "sum": {"field": "sep_12"}
              },
              "Q3-2013": {
                "sum": {"field": "sep_13"}
              },
              "Q3-2014": {
                "sum": {"field": "sep_14"}
              },
              "Q3-2015": {
                "sum": {"field": "sep_15"}
              },
              "Q3-2016": {
                "sum": {"field": "sep_16"}
              },
              "Q3-2017": {
                "sum": {"field": "sep_17"}
              },
              "Q3-2018": {
                "sum": {"field": "sep_18"}
              },
              "Q3-2019": {
                "sum": {"field": "sep_19"}
              },
              "Q3-2020": {
                "sum": {"field": "sep_20"}
              },
              "Q3-2021": {
                "sum": {"field": "sep_21"}
              },
              "Q4-2010": {
                "sum": {"field": "dec_10"}
              },
              "Q4-2011": {
                "sum": {"field": "dec_11"}
              },
              "Q4-2012": {
                "sum": {"field": "dec_12"}
              },
              "Q4-2013": {
                "sum": {"field": "dec_13"}
              },
              "Q4-2014": {
                "sum": {"field": "dec_14"}
              },
              "Q4-2015": {
                "sum": {"field": "dec_15"}
              },
              "Q4-2016": {
                "sum": {"field": "dec_16"}
              },
              "Q4-2017": {
                "sum": {"field": "dec_17"}
              },
              "Q4-2018": {
                "sum": {"field": "dec_18"}
              },
              "Q4-2019": {
                "sum": {"field": "dec_19"}
              },
              "Q4-2020": {
                "sum": {"field": "dec_20"}
              }
              
            })

    current_app.logger.info(res["aggregations"])
    return {"result": res["aggregations"]}
