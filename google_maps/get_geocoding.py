# -*- coding: utf-8 -*-
import requests
import json
from time import sleep
import pandas as pd
import sys

wait_time = 0.3 # (sec)
base_url = 'https://maps.googleapis.com/maps/api/geocode/json?language=ja&address={}&key=AIzaSyD208hE6JZHAwgrmS9aQViSnY9mvNDZbCA'
headers = {'content-type': 'application/json'}

stations_df = pd.read_csv('input/gifu_station_name.csv', index_col=0)
for q in stations_df['station'].values:
    url = base_url.format(q)
    r = requests.get(url, headers=headers)
    data = r.json()
    if 'results' in data and len(data['results']) > 0 and 'formatted_address' in data['results'][0]:
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        print(q, lat, lng)
    sleep(wait_time)
