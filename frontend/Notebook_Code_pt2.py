import requests
import pandas as pd

URL = 'http://127.0.0.1:9090/tweets/state'  # TODO INSERT URL.
res = requests.get(URL)
#print(res.content)
rjson = res.json()

# Scan and store daily Twitter data.
twitter = {}

for hit in rjson['result']['State']["buckets"]:
    state = hit["key"]
    sentiment = hit["Sentiment"]["value"]
    if state not in twitter:
        twitter[state] = 0
    twitter[state] += sentiment
df_twitter = pd.DataFrame(sorted(twitter.items()), columns=("State", "Sentiment"))
df_twitter.head(10)


# --------------------------- NEW CELL -----------------------------------------------------------------------

URL = 'http://127.0.0.1:9090/unemployment/mid'  # TODO INSERT URL.
res = requests.get(URL)
rjson = res.json()
print(rjson)

# Scan Unemployment file.
unemployment_sep21 = {}
unemployment_jun21 = {}
for hit in rjson['result']['State']['buckets']:
    state = hit["key"]
    sep21 = hit["sep_21"]['value']
    jun21 = hit["jun_21"]['value']

    if state not in unemployment_jun21:
        unemployment_jun21[state] = 0
    if state not in unemployment_sep21:
        unemployment_sep21[state] = 0
    unemployment_jun21[state] += jun21
    unemployment_sep21[state] += sep21

df_sep21 = pd.DataFrame(sorted(unemployment_sep21.items()), columns=("State", "sep_21"))
df_jun21 = pd.DataFrame(sorted(unemployment_jun21.items()), columns=("State", "jun_21"))
df_unemployment = pd.merge(df_sep21, df_jun21, on='State')
df_unemployment.head(10)

# --------------------------- NEW CELL -----------------------------------------------------------------------


# Merge two datasets
df = pd.merge(df_twitter, df_unemployment, on='State')
df = df.dropna()
df.head(10)
df["Unemp Avg"] = (df['sep_21'] + df['jun_21']) / 2


STATE_NAMES_TO_CODES = {"New South Wales": "NSW", "Victoria": "VIC", "Queensland": "QLD", "South Australia": "SA",
                        "Northern Territory": "NT", "Western Australia": "WA", "Tasmania": "TAS",
                        "Australian Capital Territory": "ACT"}
df["State"] = df["State"].apply(STATE_NAMES_TO_CODES.get)
df = df.sort_values(by="Unemp Avg", ascending=False)
df["June 2021"] = df['jun_21']
df["September 2021"] = df['sep_21']
df["Twitter Sentiment"] = df["Sentiment"]

# --------------------------- NEW CELL -----------------------------------------------------------------------

# Analyse General Unemployment levels.
import matplotlib.pyplot as plt

# State vs Unemployment
df[['State', "September 2021", "June 2021"]].plot(x='State', kind='bar', stacked=False, width=0.8, edgecolor='black',
                                                  title='Unemployment Levels across Australian States.')
plt.show()

# State vs Sentiment
df[['State', 'Twitter Sentiment']].plot(x='State', kind='bar', stacked=False, width=0.8, edgecolor='black',
                                        color='mediumorchid', title='Sentiment levels across Australian States.')
plt.show()

# --------------------------- NEW CELL -----------------------------------------------------------------------

# Scale data by state populations and redo analysis.
POPULATIONS = {'NSW': 8189266, 'VIC': 6649159, 'QLD': 5221170, 'SA': 1773243, 'WA': 2681633, 'TAS': 541479943,
               'NT': 246338103, 'ACT': 432266}
df["Population"] = df["State"].apply(POPULATIONS.get)
df["June 2021 (%)"] = df["June 2021"] / df["Population"]
df["September 2021 (%)"] = df["September 2021"] / df["Population"]
df["Twitter Sentiment (Scaled by Population)"] = df["Sentiment"] / df["Population"]

# State vs Unemployment
df[['State', "September 2021 (%)", "June 2021 (%)"]].plot(x='State', kind='bar', stacked=False, width=0.8, edgecolor='black',
                                                          title='Unemployment Levels across Australian States.')
plt.show()

# State vs Sentiment
df[['State', 'Twitter Sentiment (Scaled by Population)']].plot(x='State', kind='bar', stacked=False, width=0.8, edgecolor='black',
                                                                color='mediumorchid', title='Sentiment levels across Australian States.')
plt.show()

