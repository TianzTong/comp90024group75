import requests
import pandas as pd
import numpy as np

URL = 'http://127.0.0.1:9090/asx/quarterly' #Add URL here
res = requests.get(URL)
rjson = res.json()
#print(rjson)

asx_quarterly = []
for bucket in rjson['result']['quarters']["buckets"]:
    quarter_start_date = pd.to_datetime(bucket["key_as_string"].split('T')[0])
    quarter = "Q" + str(int(np.ceil(quarter_start_date.month / 3))) + "-" + str(quarter_start_date.year)
    price = float(str(bucket["Price_Average"]["value"]).replace(",", " "))
    asx_quarterly.append((quarter, price))

asx_quarterly.sort()
df_asx_quarterly = pd.DataFrame(asx_quarterly, columns=["Quarter", "ASX Price"])
df_asx_quarterly.head(10)

# ----------------------------
URL = 'http://127.0.0.1:9090/unemployment/quarterly' #Add URL here
res = requests.get(URL)
rjson = res.json()
#print(rjson)

QUARTERS = (["Q4-2010"] + ["Q" + str(i) + "-" + str(y) for y in range(2011, 2020+1) for i in range(1, 4+1)] +
            ["Q1-2021", "Q2-2021", "Q3-2021"])


unemployment = []
for Q in QUARTERS:
    unemployment.append((Q, rjson['result'][Q]['value']))
unemployment.sort()
df_unemployment_quarterly = pd.DataFrame(unemployment, columns=["Quarter", "Unemployment"])
df_unemployment_quarterly.head(10)
# --------------------------------------------------
REFERENCE_QUARTER = "Q4-2010"
def quarter_index(qaurter, reference_quarter="Q4-2010"):
    q_s, year_s = qaurter.split('-')
    q_s = q_s[1:]

    ref_q_s, ref_year_s = reference_quarter.split('-')
    ref_q_s = ref_q_s[1:]

    return (int(year_s) - int(ref_year_s)) * 4 + (int(q_s) - int(ref_q_s))


df = pd.merge(df_asx_quarterly, df_unemployment_quarterly, on='Quarter')
df = df.dropna()
df["Quarter Index"] = df["Quarter"].apply(quarter_index)
df = df.sort_values(by="Quarter Index")

df.head(10)

# --------------------------------------------------
# Analyse change over quarters.
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

x = np.array(df["Quarter Index"])
x_label = "Quarter Since " + REFERENCE_QUARTER
field_names = ["Unemployment",  "ASX Price"]
colors = ["red", "darkgreen", "orange"]
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
    plt.plot(x, y, color=color)
    plt.plot(x, y_pred, color='darkblue', label=regression_string)
    plt.title("Visualization of how " + field_name + " changes over quarters starting from " + REFERENCE_QUARTER + '.')
    plt.xlabel(x_label)
    plt.ylabel(field_name)
    plt.legend()
    plt.grid(True)
    plt.show()

# ----------------------------------------------------------------------------------------------------------------------
# Directly Unemployment vs ASX.
y = np.array(df["Unemployment"])
y_label = "Unemployment Amount"

# Create regression.
x = np.array(df["ASX Price"])
x0 = sm.add_constant(x)
model = sm.OLS(y, x0).fit()
y_pred = model.predict(x0)

# Regression Description String.
regression_string = ''
regression_string += f'y = {model.params[1]:.2f}x + {model.params[0]:.2f}\n'
regression_string += f'R-Squared (Adj) = {model.rsquared_adj:.2f}'


# Plot Datapoints and Regression.
plt.scatter(x, y, color="darkslategrey")
plt.plot(x, y_pred, color='red', label=regression_string)
plt.title("Visualization of the relationship between ASX Price and\n" + y_label)
plt.xlabel("ASX Price ($)")
plt.ylabel(y_label)
plt.legend()
plt.grid(True)
plt.show()
