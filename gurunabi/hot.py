#!/usr/bin/env python
# -*- coding: utf-8 -*-
#*****************************************************************************************
# ぐるなびWebサービスのレストラン検索APIで緯度経度検索を実行しパースするプログラム
# 注意：ここでは緯度と経度の値は固定でいれています。
# 　　　APIアクセスキーの値にはユーザ登録で取得したものを入れてください。
#*****************************************************************************************
import sys
from urllib.parse import urlencode
from urllib.request import urlopen
import json
import pandas as pd


####
# 変数の型が文字列かどうかチェック
####
def is_str( data = None ) :
  # if isinstance( data, str ) or isinstance( data, unicode ) :
  if isinstance( data, str ) :
    return True
  else :
    return False



####
# 初期値設定
####
# APIアクセスキー
keyid     = "5ab0657f540edfef"
# エンドポイントURL
url       = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
# 緯度,経度
#nakatsu
# latitude  = "35.50009"
# longitude = "137.502939"
#ena
# latitude  = '35.455031'
# longitude = '137.40803'
#mizunami
# latitude  = "35.36"
# longitude = "137.25"
# latitude  = "35.369016"
# longitude = "137.252072"
#tokishi
# latitude  = "35.359764"
# longitude = "137.182195"
#tajimi
# latitude  = "35.334979"
# longitude = "137.121042"
#nagoya
latitude  = "35.171348"
longitude = "136.883000"
# 範囲
range_     = "1"
# hit_per_page = "100"
order = "4"
# datum = "world"
# datum = "tokyo"

####
# APIアクセス
####
# URLに続けて入れるパラメータを組立
query = [
  ( "key", keyid ),
  ( "format", "json" ),
  # ( "datum", datum ),
  ( "lat", latitude ),
  ( "lng", longitude ),
  ( "range", range_ ),
  # ( "count", hit_per_page ),
  # ( "order", order )
]
# URL生成
url += "?{0}".format( urlencode( query ) )
# print(url)
# url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=5ab0657f540edfef&format=json&lat=35.369016&lng=137.252072&range=5&order=4"
# url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=5ab0657f540edfef&format=json&lat=34.671234&lng=135.521234&range=5&order=4"
# url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=5ab0657f540edfef&format=json&lat=35.36&lng=137.25&range=5&order=4"
try :
  result = urlopen( url ).read()
except ValueError :
  print(u"APIアクセスに失敗しました。")
  sys.exit()



####
# 取得した結果を解析
####
# print(result)
data = json.loads( result )
data = data["results"]
# print(data)
# エラーの場合
if "error" in data :
  if "message" in data :
    print(u"{0}".format( data["message"] ))
  else :
    print(u"データ取得に失敗しました。")
  sys.exit()

# ヒット件数取得
total_hit_count = None
if "results_returned" in data :
  total_hit_count = data["results_available"]

# ヒット件数が0以下、または、ヒット件数がなかったら終了
if total_hit_count is None or int(total_hit_count) <= 0 :
  # print(data)
  print(total_hit_count)
  print(u"指定した内容ではヒットしませんでした。")
  sys.exit()

# レストランデータがなかったら終了
if not "shop" in data :
  print(u"レストランデータが見つからなかったため終了します。")
  sys.exit()

# ヒット件数表示
print(u"{0}件ヒットしました。".format( total_hit_count ))
# print("----")

# 出力件数
# disp_count = 0



# レストランデータ取得
restaurant_df = pd.DataFrame(index=range(int(total_hit_count)),
                             columns=['id', '名前', 'アクセス', 'カテゴリー',
                                      '平均予算', '座席数'])

for i, rest in enumerate(data["shop"]) :
  line                 = []
  id                   = ""
  name                 = ""
  access               = ""
  code_category_name_s = ""
  budget               = ""
  capacity             = ""

  # 店舗番号
  if "id" in rest and is_str( rest["id"] ) :
    id = rest["id"]
  line.append( id )

  # 店舗名
  if "name" in rest and is_str( rest["name"] ) :
    name = u"{0}".format( rest["name"] )
  line.append( name )

  # アクセス
  if "access" in rest and is_str( rest["access"] ) :
    access = u"{0}".format( rest["access"] )
  line.append( access )

  # 店舗の小業態
  if "genre" in rest and "name" in rest["genre"] :
    category_name_s_0 = rest["genre"]["name"]
    if is_str( category_name_s_0 ) :
      code_category_name_s = u"{0}".format( category_name_s_0 )
  line.append( code_category_name_s )

  # 平均予算
  if "budget" in rest and "average" in rest["budget"] :
    budget = rest["budget"]["average"]
    if is_str( budget ) :
      budget = u"{0}".format( budget )
  line.append( budget )

  # 総席数
  if "capacity" in rest and is_str( rest["capacity"] ) :
    capacity = u"{0}".format( rest["capacity"] )
  line.append( capacity )


  # タブ区切りで出力
  # print("\t".join( line ))
  # disp_count += 1
  # print(len(line))
  # print(line)
  restaurant_df.iloc[i, :] = line[:]


# 出力件数を表示して終了
# print("----")
# print(u"{0}件出力しました。".format( disp_count ))
# sys.exit()
restaurant_df.to_csv("restaurants_hot_mizunami500m.csv", index=0)
