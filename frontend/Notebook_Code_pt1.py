import pandas as pd
import requests

URL = 'http://127.0.0.1:9090/asx/daily'  # TODO INSERT URL.
res = requests.get(URL)
rjson = res.json()
print(len(rjson['result']['hits']))

# Scan and store daily ASX data.
asx_daily = []
for hit in rjson['result']['hits']:
    date = pd.to_datetime(hit["_source"]["Date"], format="%Y-%m-%d").normalize()
    price = float(hit["_source"]["Price"])
    change = float(hit["_source"]["Change %"][:-1])
    asx_daily.append((date, price, change))
asx_daily.sort()
df_asx_daily = pd.DataFrame(asx_daily, columns=("Date", "ASX Price", "ASX Change (%)"))
df_asx_daily.head(10)

# --------------------------- NEW CELL -----------------------------------------------------------------------
URL = 'http://127.0.0.1:9090/tweets/daily'  # TODO INSERT URL.
res = requests.get(URL)

rjson = res.json()

# Exclude dates that ElasticSearch falsely initialized
EXCLUDE_DATES = {pd.to_datetime('2021-06-25'), pd.to_datetime('2022-03-29'), pd.to_datetime('2021-09-08'),
                 pd.to_datetime('2021-07-02'), pd.to_datetime('2021-09-09'), pd.to_datetime('2021-09-10'),
                 pd.to_datetime('2021-06-27'), pd.to_datetime('2021-09-07'), pd.to_datetime('2021-06-26'),
                 pd.to_datetime('2021-10-10'), pd.to_datetime('2021-07-03')} 
                 
# Scan and store daily Twitter data.
twitter = {}
for bucket in rjson["result"]["Date"]["buckets"]:
    date = pd.to_datetime(bucket["key_as_string"]).normalize()
    if date not in EXCLUDE_DATES:
        sentiment = float(bucket["Sentiment"]["value"])
        if date not in twitter:
            twitter[date] = 0
        twitter[date] += sentiment
df_twitter_daily = pd.DataFrame(sorted(twitter.items()), columns=("Date", "Sentiment"))
df_twitter_daily.head(10)

# --------------------------- NEW CELL -----------------------------------------------------------------------

# Merge Datasets
df = pd.merge(df_twitter_daily, df_asx_daily, on='Date')
df = df.dropna()
earliest_date = df['Date'].min()
df['Date Index'] = (df['Date'] - earliest_date).dt.days
df.head(10)

# --------------------------- NEW CELL -----------------------------------------------------------------------

# Analyse change over time.
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

x = np.array(df["Date Index"])
x_label = "Days Since 21/6/21"
field_names = ["Sentiment",  "ASX Price", "ASX Change (%)"]
colors = ["darkblue", "darkgreen", "indigo"]
for field_name, color in zip(field_names, colors):

    # Create regression.
    y = np.array(df[field_name])
    x0 = sm.add_constant(x)
    model = sm.OLS(y, x0).fit()
    y_pred = model.predict(x0)

    # Regression Description String.
    regression_string = ''
    regression_string += f'y = {model.params[1]:.2f}x + {model.params[0]:.2f}\n'
    regression_string += f'R-Squared (Adj) = {model.rsquared_adj:.2f}'

    # Plot Datapoints and Regression.
    plt.scatter(x, y, color=color)
    plt.plot(x, y_pred, color='red', label=regression_string)
    plt.title("Visualization of how " + field_name + " changes over time (from 21/6/21).")
    plt.xlabel(x_label)
    plt.ylabel(field_name)
    plt.legend()
    plt.grid(True)
    plt.show()

# --------------------------- NEW CELL -----------------------------------------------------------------------

# Directly Sentiment vs ASX.
y = np.array(df["Sentiment"])
y_label = "Twitter Sentiments"

field_names = ["ASX Price", "ASX Change (%)"]
colors = ["darkgoldenrod", "steelblue"]
for field_name, color in zip(field_names, colors):

    # Create regression.
    x = np.array(df[field_name])
    x0 = sm.add_constant(x)
    model = sm.OLS(y, x0).fit()
    y_pred = model.predict(x0)

    # Regression Description String.
    regression_string = ''
    regression_string += f'y = {model.params[1]:.2f}x + {model.params[0]:.2f}\n'
    regression_string += f'R-Squared (Adj) = {model.rsquared_adj:.2f}'

    # Plot Datapoints and Regression.
    plt.scatter(x, y, color=color)
    plt.plot(x, y_pred, color='red', label=regression_string)
    plt.title("Visualization of the relationship between " + field_name + " and\n Australian Twitter Sentiment.")
    plt.xlabel(field_name)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)
    plt.show()
