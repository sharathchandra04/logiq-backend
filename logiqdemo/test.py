import pandas as pd

from pycaret.anomaly import *

data = pd.read_csv('https://raw.githubusercontent.com/numenta/NAB/master/data/realKnownCause/nyc_taxi.csv')
data['timestamp'] = pd.to_datetime(data['timestamp'])
# data.head()
# print(data.head())
data['MA48'] = data['value'].rolling(48).mean()
data['MA336'] = data['value'].rolling(336).mean()

import plotly.express as px
# fig = px.line(data, x="timestamp", y=['value', 'MA48', 'MA336'], title='NYC Taxi Trips', template = 'plotly_dark')
# fig.show()

# print(data.fillna(0))
data['MA48'] = data['MA48'].fillna(0)
data['MA336'] = data['MA336'].fillna(0)
a = data['MA48']
b = data['MA336']
print(a)
print(b)
print(len(a))
print(len(b))
# print(data)
# len(df.index)
data.drop(['MA48', 'MA336'], axis=1, inplace=True)

data.set_index('timestamp', drop=True, inplace=True)
# resample timeseries to hourly 
data = data.resample('H').sum()
# creature features from date
data['day'] = [i.day for i in data.index]
data['day_name'] = [i.day_name() for i in data.index]
data['day_of_year'] = [i.dayofyear for i in data.index]
data['week_of_year'] = [i.weekofyear for i in data.index]
data['hour'] = [i.hour for i in data.index]
data['is_weekday'] = [i.isoweekday() for i in data.index]

print('1. ', data.head())

print('2. ', len(data.index))

s = setup(data, silent = True, session_id = 123)
iforest = create_model('iforest', fraction = 0.1)
iforest_results = assign_model(iforest)

# iforest_results.head()

print('3. ',iforest_results.head())

print(iforest_results[iforest_results['Anomaly'] == 1].head())

outlier_dates = iforest_results[iforest_results['Anomaly'] == 1].index
# obtain y value of anomalies to plot
y_values = [iforest_results.loc[i]['value'] for i in outlier_dates]

import plotly.graph_objects as go
# plot value on y-axis and date on x-axis
fig = px.line(iforest_results, x=iforest_results.index, y="value", title='NYC TAXI TRIPS - UNSUPERVISED ANOMALY DETECTION', template = 'plotly_dark')
# create list of outlier_dates
outlier_dates = iforest_results[iforest_results['Anomaly'] == 1].index
# obtain y value of anomalies to plot
y_values = [iforest_results.loc[i]['value'] for i in outlier_dates]
fig.add_trace(go.Scatter(x=outlier_dates, y=y_values, mode = 'markers', 
                name = 'Anomaly', 
                marker=dict(color='red',size=10)))
        
fig.show()

print(outlier_dates)
print(y_values)








