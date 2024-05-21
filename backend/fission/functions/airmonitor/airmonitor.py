from flask import current_app
import requests
import json
URL = "http://router.fission/air"
def config(k):
    with open(f'/configs/default/air-const/{k}', 'r') as f:
        return f.read()

def main():
    current_app.logger.info(config("URL"))
    rows = []
    # get the response by calling to the EPA API
    res = requests.get(config('URL'), headers={"X-API-Key": config('SUB_KEY'), 'User-Agent': 'group75A2'})
    resJson = res.json()
    
    # iterate through the records
    for record in resJson["records"]:
        try:
            
            newRecord = {}
            newRecord["siteName"] = record["siteName"]
            newRecord["siteID"] = record["siteID"]
            newRecord["siteType"] = record["siteType"]
            newRecord["since"] = record["siteHealthAdvices"][0]["since"]
            newRecord["until"] = record["siteHealthAdvices"][0]["until"]
            newRecord["healthParameter"] = record["siteHealthAdvices"][0]["healthParameter"]
            newRecord["averageValue"] = record["siteHealthAdvices"][0]["averageValue"]
            
            ## skip the record if there is missing field
        except KeyError:
            continue
        else:
            current_app.logger.info(f'{newRecord}')
            res = requests.post(URL, json=newRecord)
            
            
            
        
    return 'ok'
    
