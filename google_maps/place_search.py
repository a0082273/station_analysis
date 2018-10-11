# http://hiiragiy.hateblo.jp/entry/2017/08/24/145754
# https://developers.google.com/places/web-service/search?hl=ja

import urllib.request, json, time
import pandas as pd
import numpy as np
import api_key

Places_key = api_key.places
radius = '500'

location_dict = {
    # 'sakashita': '35.574221,137.531073',
    # 'ochiaigawa': '35.525171,137.529964',
    'nakatsugawa': '35.50009,137.502939',
    # 'minosakamoto': '35.479396,137.449556',
    'ena': '35.455031,137.40803',
    # 'takenami': '35.437954,137.353982',
    # 'kamado': '35.411317,137.305626',
    'mizunami': '35.369016,137.252072',
    'tokishi': '35.359764,137.182195',
    'tajimi': '35.334979,137.121042',
    # 'kokoke': '35.303213,137.101232',
    # 'jokoji': '35.278604,137.081095',
    # 'kozoji': '35.264438,137.043071',
    # 'jinryo': '35.256577,137.010463',
    # 'kasugai': '35.243034,136.98509',
    # 'kachigawa': '35.229857,136.956302',
    # 'shinmoriyama': '35.207303,136.9512',
    # 'ozone': '35.191489,136.936846',
    # 'chikusa': '35.170167,136.930662',
    # 'tsurumai': '35.156389,136.917527',
    # 'kanayama': '35.143045,136.900905',
    # 'nagoya': '35.171348,136.883000'
}

place_types = [
    # 'art_gallery',
    # 'bakery',
    # 'bar',
    # 'beauty_salon',
    # 'book_store',
    # 'bus_station',
    # 'cafe',
    # 'car_rental',
    # 'city_hall',
    # 'clothing_store',
    # 'convenience_store',
    # 'department_store',
    # 'doctor',
    # 'electronics_store',
    # 'florist',
    # 'gym',
    # 'hair_care',
    # 'home_goods_store',
    # 'hospital',
    # 'laundry',
    # 'library',
    # 'liquor_store',
    # 'local_government_office',
    # 'lodging', #ホテル
    # 'meal_delivery',
    # 'meal_takeaway',
    # 'movie_theater',
    # 'night_club',
    'park',
    # 'parking',
    # 'restaurant',
    # 'school',
    # 'shopping_mall',
    # 'spa',
    # 'store',
    # 'university'
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

        time.sleep(2)

        next_page_token = content.get('next_page_token')
        if next_page_token:
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?language=ja&pagetoken="+ next_page_token +"&key=" + Places_key
        else:
            break
    places.append([np.nan, np.nan])
    places = pd.DataFrame(places)
    return places



if __name__ == '__main__':
    for iloc in range(len(location_dict)):
        place_i = pd.DataFrame()
        location = list(location_dict.keys())[iloc]
        location_geo = list(location_dict.values())[iloc]
        for itype in range(len(place_types)):
            place_type = place_types[itype]
            url = get_url(location_geo, place_type)
            place_ii = make_place_list(url)
            place_ii.columns = [place_type, place_type+'_rating']
            print('local: '+str(iloc+1)+'/'+str(len(location_dict)), '   place: '+str(itype+1)+'/'+str(len(place_types)))
            place_i = pd.concat([place_i, place_ii], axis=1)
        place_i.to_csv('input/' + location + radius + '.csv')
