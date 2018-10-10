# coding: UTF-8
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import pandas as pd

# url = "https://storestrategy.jp/?category=1&area=4&pref=22&order="
# url = "https://storestrategy.jp/?category=1&area=4&pref=24&order="
url = "https://storestrategy.jp/?category=1&area=5&pref=25&order="
instance = urllib.request.urlopen(url)
soup = BeautifulSoup(instance, "html.parser")

rosen = []
n_station = []
# for i in range(12):
# for i in range(33):
for i in range(19):
# for i in range(2):
    tmp = soup.select_one(f"#contents_lv02_wrapper > ul:nth-of-type({2+i}) > li > ul").text
    tmp = tmp.splitlines()
    rosen.append(tmp)
    for j in range(len(tmp)):
        # n_station.append(f'g_{i}')
        # n_station.append(f'a_{i}')
        n_station.append(f'm_{i}')

rosen = [x for list in rosen for x in list]
stations = pd.DataFrame({'station': rosen, 'rosen': n_station})
# stations.to_csv('input/gifu_station_name.csv')
# stations.to_csv('input/aichi_station_name.csv')
stations.to_csv('input/mie_station_name.csv')
