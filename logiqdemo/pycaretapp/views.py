from django.shortcuts import render

# Create your views here.
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
import pandas as pd
from pycaret.anomaly import *
import json

class PycaretDataAnamoly(RetrieveAPIView):

    # permission_classes = (AllowAny,)
    # serializer_class = UserLoginSerializer

    def get(self, request):
        
        data = pd.read_csv('https://raw.githubusercontent.com/numenta/NAB/master/data/realKnownCause/nyc_taxi.csv')
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        data.set_index('timestamp', drop=True, inplace=True)
        data = data.resample('H').sum()
        data['day'] = [i.day for i in data.index]
        data['day_name'] = [i.day_name() for i in data.index]
        data['day_of_year'] = [i.dayofyear for i in data.index]
        data['week_of_year'] = [i.weekofyear for i in data.index]
        data['hour'] = [i.hour for i in data.index]
        data['is_weekday'] = [i.isoweekday() for i in data.index]
        s = setup(data, silent = True, session_id = 123)
        iforest = create_model('iforest', fraction = 0.1)
        iforest_results = assign_model(iforest)
        outlier_dates = iforest_results[iforest_results['Anomaly'] == 1].index
        # obtain y value of anomalies to plot
        y_values = [iforest_results.loc[i]['value'] for i in outlier_dates]
        print(data)
        print(data.head().reset_index().to_json(orient='records'))
        print(type(data.head().reset_index().to_json(orient='records')))
        
        # x =  '{ "name":"John", "age":30, "city":"New York"}'
        # y = json.loads(x)
        data['time'] = data.index
        responsedata = {
            # 'dataframe': json.loads(data.reset_index().to_json(orient='records')),
            'dataframe': data,
            'outlier_dates': outlier_dates,
            'anamoly_values': y_values
        }
        return Response(responsedata, status=200)

class PycaretDataMeans(RetrieveAPIView):

    # permission_classes = (AllowAny,)
    # serializer_class = UserLoginSerializer

    def get(self, request):
        
        data = pd.read_csv('https://raw.githubusercontent.com/numenta/NAB/master/data/realKnownCause/nyc_taxi.csv')
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data['MA48'] = data['value'].rolling(48).mean()
        data['MA336'] = data['value'].rolling(336).mean()
        data['MA48'] = data['MA48'].fillna(0)
        data['MA336'] = data['MA336'].fillna(0)

        return Response(data, status=200)
