import requests

URL = 'http://127.0.0.1:9090/unemployment'

# get all the hits from fission
res = requests.get(URL)
#print(res.content)

# process and analyse data
start_unemp = 0
end_unemp = 0
rjson = res.json()
for hit in rjson['result']['hits']:
    start_unemp += int(hit["_source"]["mar_21"])
    end_unemp += int(hit["_source"]["sep_21"])
print("Change in unemployment (pos=more, neg=less)", end_unemp - start_unemp)