from datetime import datetime
import pandas as pd
import requests
import statsmodels.api as sm
URL = 'http://127.0.0.1:9090/tweets'

# get all the hits from fission
res = requests.get(URL)
rjson = res.json()

# process and analyse data
sents = []
days_from_start = []

for hit in rjson['result']['hits']:
    
    d = pd.to_datetime(hit["_source"]["Datetime"])
    dfs = (d - pd.to_datetime("2021-1-1")).days
    days_from_start.append(dfs)

    sent = hit["_source"]["Sentiment"]
    sents.append(sent)

model = sm.OLS(sents, days_from_start).fit()
print("Sentiment Gradient", model.params[0])