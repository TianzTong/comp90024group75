import requests
URL='https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites?environmentalSegment=air'
SUB_KEY = '1dc2f160a2a441af82171e3e01ca4f2f'

res = requests.get(URL,headers={"X-API-Key": SUB_KEY, 'User-Agent': 'group75A2'})
#curl -vvv "https://gateway.api.epa.vic.gov.au/environmentMonitoring/v1/sites?environmentalSegment=air"
    #-H "X-API-Key:1dc2f160a2a441af82171e3e01ca4f2f"

data = res.json()
print(data['records'])
