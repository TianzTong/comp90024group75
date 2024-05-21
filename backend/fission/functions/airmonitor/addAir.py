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
    
    # get the content
    jsonSend = request.get_json(force=True)
    current_app.logger.info(f'{jsonSend}')
    
    # send the http request to the elastic search to index the document
    res = client.index(
        
        index='air',
        id=f'{jsonSend["siteID"]}-{jsonSend["since"]}-{jsonSend["until"]}',
        document=jsonSend
    )

    return { "Result":res['result']}