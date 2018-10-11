# http://hiiragiy.hateblo.jp/entry/2017/08/24/145754
# https://developers.google.com/places/web-service/search?hl=ja

import urllib.request, json, time
import pandas as pd
import numpy as np
import api_key
import sys

Places_key = api_key.places
radius = '500'
prefecture = ['gifu', 'aichi', 'mie']

station = pd.read_csv(f'input/{prefecture[2]}_station_geo_fix_fix.csv', index_col=0)

place_types = [
    'art_gallery',
    'bar',
    'book_store',
    'cafe',
    'convenience_store',
    'department_store',
    'gym',
    'lodging', #ホテル
    'park',
    'restaurant'
]




def get_url(location, place_type):
    option = "&radius=" + radius + "&type=" + place_type + "&language=ja&key="
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + location + option + Places_key
    return url


def req_Response(url):
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    content = json.loads(response.read().decode('utf-8'))
    return content


def make_place_list(url):
    places = []
    while True:
        content = req_Response(url)
        for i in range(len(content['results'])):
            place = []
            place.append(str(content['results'][i]['name']))
            if 'rating' not in str(content['results'][i]):
                content['results'][i]['rating'] = np.nan
            place.append(str(content['results'][i]['rating']))
            places.append(place)

        time.sleep(2) #next_page_tokenが有効になるまで少し時間がかかる!!!

        next_page_token = content.get('next_page_token')
        if next_page_token:
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?language=ja&pagetoken=" + next_page_token +"&key=" + Places_key
        elif content['status'] == 'INVALID_REQUEST':
            print('!!!   INVALID_REQUEST   !!!')
            sys.exit()
        else:
            break
    places.append([np.nan, np.nan])
    places = pd.DataFrame(places)
    return places



def main():
    counts = pd.DataFrame(index=station['station'].values, columns=place_types)
    for iloc in range(len(station)):
        place_i = pd.DataFrame()
        location = station.loc[iloc, 'station']
        lat = station.loc[iloc, 'lat']
        lng = station.loc[iloc, 'lng']
        location_geo = f'{lat},{lng}'
        for itype in range(len(place_types)):
            place_type = place_types[itype]
            url = get_url(location_geo, place_type)
            place_ii = make_place_list(url)
            place_ii.columns = [place_type, place_type+'_rating']
            print('local: '+str(iloc+1)+'/'+str(len(station)),
                  '   place: '+str(itype+1)+'/'+str(len(place_types)))
            place_i = pd.concat([place_i, place_ii], axis=1)
            counts.loc[location, place_type] = np.sum(place_ii[place_type].notnull())
        place_i.to_csv('input/' + location + '.csv')
    counts.to_csv(f'input/{prefecture[2]}_counts.csv')


if __name__ == '__main__':
    main()
