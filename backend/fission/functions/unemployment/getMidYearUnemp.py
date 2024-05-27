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
        _source=["lga_code_2021_asgs", "jun_21", "sep_21"],
        size=0,
        aggs={
            "State": {
            "terms": {
                "script": {
                "source": """
                    def state_code = doc['lga_code_2021_asgs'].value.toString().substring(0,1);
                    def state = 'Unknown';
                    if (state_code == "1") {
                        state = 'New South Wales';
                    } else if (state_code == "2") {
                        state = 'Victoria';
                    } else if (state_code == "3") {
                        state = 'Queensland';
                    } else if (state_code == "4") {
                        state = 'South Australia';
                    } else if (state_code == "5") {
                        state = 'Western Australia';
                    } else if (state_code == "6") {
                        state = 'Tasmania';
                    } else if (state_code == "7") {
                        state = 'Northern Territory';
                    } else if (state_code == "8") {
                        state = 'Australian Capital Territory';
                    }
                    return state;
                """
                }
            },
            "aggs": {
                "jun_21": {
                "sum": {"field": "jun_21"}
                },
                "sep_21": {
                "sum": {"field": "sep_21"}
                }
            }
            }
        }
    )
    current_app.logger.info(res["aggregations"])
    return {"result": res["aggregations"]}