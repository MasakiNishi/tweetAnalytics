#初期化
from requests_oauthlib import OAuth1Session
from requests.exceptions import ConnectionError, ReadTimeout, SSLError
import json, datetime, time, pytz, re, sys, traceback, unicodedata, pymongo
#from pymongo import Connection     # Connection classは廃止されたのでMongoClientに変更 
from pymongo import MongoClient
import numpy as np
from collections import defaultdict
from bson.objectid import ObjectId
import MeCab as mc

KEYS = { # 自分のアカウントで入手したキーを下記に記載
        'consumer_key':'******************************',
        'consumer_secret':'******************************',
        'access_token':'******************************',
        'access_secret': '******************************',
       }

twitter = None
connect = None
db      = None
tweetdata = None
meta    = None
posi_nega_dict = None

def initialize(): # twitter接続情報や、mongoDBへの接続処理等initial処理実行
    global twitter, twitter, connect, db, tweetdata, meta, posi_nega_dict, location_dict #posi_nega_dictとlocation_dictを追加_Akky
    twitter = OAuth1Session(KEYS['consumer_key'],KEYS['consumer_secret'],
                            KEYS['access_token'],KEYS['access_secret'])
#   connect = Connection('localhost', 27017)     # Connection classは廃止されたのでMongoClientに変更 
    connect = MongoClient('localhost', 27017)
    db = connect.cclemon
    tweetdata = db.tweetdata
    meta = db.metadata
    posi_nega_dict = db.posi_nega_dict
    location_dict = db.location_dict

initialize()