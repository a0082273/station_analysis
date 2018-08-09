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
keyid     = "8ec78e8fb17b8f62fae624b03fc6c169"
# エンドポイントURL
# url       = "https://api.gnavi.co.jp/RestSearchAPI/20150630/"
url       = "https://api.gnavi.co.jp/RestSearchAPI/20180807/"
# 緯度,経度
#nakatsu
# latitude  = "35.50009"
# longitude = "137.502939"
#ena
# latitude  = '35.455031'
# longitude = '137.40803'
#mizunami
latitude  = "35.369016"
longitude = "137.252072"
#tokishi
# latitude  = "35.359764"
# longitude = "137.182195"
#tajimi
# latitude  = "35.334979"
# longitude = "137.121042"
# 範囲
range_     = "2"
input_coordinates_mode = "2"
hit_per_page = "100"

####
# APIアクセス
####
# URLに続けて入れるパラメータを組立
query = [
  ( "format",    "json"    ),
  ( "keyid",     keyid     ),
  ( "latitude",  latitude  ),
  ( "longitude", longitude ),
  ( "range",     range_     ),
  ( "input_coordinates_mode", input_coordinates_mode ),
  ( "hit_per_page", hit_per_page)
]
# URL生成
url += "?{0}".format( urlencode( query ) )
# API実行
try :
  result = urlopen( url ).read()
except ValueError :
  print(u"APIアクセスに失敗しました。")
  sys.exit()



####
# 取得した結果を解析
####
data = json.loads( result )
# エラーの場合
if "error" in data :
  if "message" in data :
    print(u"{0}".format( data["message"] ))
  else :
    print(u"データ取得に失敗しました。")
  sys.exit()

# ヒット件数取得
total_hit_count = None
if "total_hit_count" in data :
  total_hit_count = data["total_hit_count"]

# ヒット件数が0以下、または、ヒット件数がなかったら終了
if total_hit_count is None or int(total_hit_count) <= 0 :
  print(u"指定した内容ではヒットしませんでした。")
  sys.exit()

# レストランデータがなかったら終了
if not "rest" in data :
  print(u"レストランデータが見つからなかったため終了します。")
  sys.exit()

# ヒット件数表示
print(u"{0}件ヒットしました。".format( total_hit_count ))
# print("----")

# 出力件数
# disp_count = 0



# レストランデータ取得
restaurant_df = pd.DataFrame(index=range(int(total_hit_count)),
                             columns=['id', '名前', '最寄り駅から徒歩', 'カテゴリー',
                                      '平均予算', '宴会・パーティ平均予算', 'ランチタイム予算'])

for i, rest in enumerate(data["rest"]) :
  line                 = []
  id                   = ""
  name                 = ""
  access_walk          = ""
  # code_category_name_s = []
  code_category_name_s = ""
  budget               = ""
  party                = ""
  lunch                = ""

  # 店舗番号
  if "id" in rest and is_str( rest["id"] ) :
    id = rest["id"]
  line.append( id )

  # 店舗名
  if "name" in rest and is_str( rest["name"] ) :
    name = u"{0}".format( rest["name"] )
  line.append( name )

  if "access" in rest :
    access = rest["access"]
    # 最寄の路線
    if "walk"    in access and is_str( access["walk"] ) :
      access_walk = u"{0}分".format( access["walk"] )
  # line.extend( [ access_walk ] )
  line.append( access_walk )

  # 店舗の小業態
  if "code" in rest and "category_name_s" in rest["code"] :
    # for category_name_s in rest["code"]["category_name_s"] :
    #   if is_str( category_name_s ) :
    #     code_category_name_s.append( u"{0}".format( category_name_s ) )
    category_name_s_0 = rest["code"]["category_name_s"]
    if is_str( category_name_s_0 ) :
      code_category_name_s.append( u"{0}".format( category_name_s_0 ) )
  # line.extend( code_category_name_s )
  line.append( code_category_name_s )

  # 平均予算
  if "budget" in rest and is_str( rest["budget"] ) :
    budget = u"{0}".format( rest["budget"] )
  line.append( budget )

  # 宴会・パーティ平均予算
  if "party" in rest and is_str( rest["party"] ) :
    party = u"{0}".format( rest["party"] )
  line.append( party )

  # ランチタイム予算
  if "lunch" in rest and is_str( rest["lunch"] ) :
    lunch = u"{0}".format( rest["lunch"] )
  line.append( lunch )

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
restaurant_df.to_csv("restaurants_mizunami500m.csv", index=0)
