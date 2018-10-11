# -*- coding: utf-8 -*-
import requests
import json
from time import sleep
import pandas as pd
import sys

wait_time = 0.3 # (sec)
base_url = 'https://maps.googleapis.com/maps/api/geocode/json?language=ja&address={}&key=**********'
headers = {'content-type': 'application/json'}

# station_df = pd.read_csv('input/gifu_station_name.csv', index_col=0)
station_df = pd.read_csv('input/aichi_station_name.csv', index_col=0)
# station_df = pd.read_csv('input/mie_station_name.csv', index_col=0)

for i, q in enumerate(station_df['station'].values):
    url = base_url.format(q)
    r = requests.get(url, headers=headers)
    data = r.json()
    if 'results' in data and len(data['results']) > 0 and 'formatted_address' in data['results'][0]:
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        station_df.loc[i, 'lat'] = lat
        station_df.loc[i, 'lng'] = lng
        print(i, q, lat, lng)
    sleep(wait_time)

# station_df.to_csv('input/gifu_station_geo.csv')
station_df.to_csv('input/aichi_station_geo.csv')
# station_df.to_csv('input/mie_station_geo.csv')
