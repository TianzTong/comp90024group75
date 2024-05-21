import requests
URL='https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites?environmentalSegment=air'
SUB_KEY = '1dc2f160a2a441af82171e3e01ca4f2f'

res = requests.get(URL,headers={"X-API-Key": SUB_KEY, 'User-Agent': 'group75A2'})
#curl -vvv "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites?environmentalSegment=air"
    #-H "X-API-Key:1dc2f160a2a441af82171e3e01ca4f2f"

resJson = res.json()
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
    except KeyError:
        continue
    else:
        print(newRecord)