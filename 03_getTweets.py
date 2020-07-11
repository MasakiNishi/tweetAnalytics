# 検索ワードを指定して100件のTweetデータをTwitter REST APIsから取得する
def getTweetData(search_word, param_next = None):
    global twitter
    
    url = 'https://api.twitter.com/1.1/tweets/search/fullarchive/label' #エンドポイントを変更。label部分を自身のものに変える
    
    params = {'query': search_word,
                      'maxResults':'500', #Premium本番環境の場合は500まで、Sandboxでは100。
                      'fromDate':'201811301500', #指定例:YYYYMMDDHHMM
                      'toDate':'201911301500' #指定例:YYYYMMDDHHMM
                     }
    
    params['next'] = param_next

#     print(params)

#     # max_idの指定があれば設定する#     if max_id != -1:
#         params['max_id'] = max_id
#     # since_idの指定があれば設定する
#     if since_id != -1:
#         params['since_id'] = since_id


    req = twitter.get(url, params = params)   # Tweetデータの取得
    
    # 取得したデータの分解
    if req.status_code == 200: # 成功した場合
        response= json.loads(req.text)
#         print(response)

#### 以下の4行を修正
        if 'next' in response: 
            metadata = response['next']  #'next'パラメータ
        else:
            metadata  = 'finish'
#####


        statuses = response['results'] #各ツイートデータ
#        print(statuses)
        
        limit = req.headers['x-rate-limit-remaining'] if 'x-rate-limit-remaining' in req.headers else 0
        reset = req.headers['x-rate-limit-reset'] if 'x-rate-limit-reset' in req.headers else 0         
        return {"result":True, "metadata":metadata, "statuses":statuses, "limit":limit, "reset_time":datetime.datetime.fromtimestamp(float(reset)), "reset_time_unix":reset}
    else: # 失敗した場合
        print ("Error: %d" % req.status_code)
        print(req.text)
        return{"result":False, "status_code":req.status_code}

def obj_nullcheck(string): # Y if X else Z
    return False if string is None else True

def is_exist_id(id_str):
    return tweetdata.find({'id':long(id_str)},{'id':1}).count() > 0

#-------------繰り返しTweetデータを取得する-------------#
sid=-1
mid = -1 
count = 0
param_next = None

res = None
while(True):    
    try:
        n_doc = tweetdata.find({}).count()
        print('現在のDB内のツイートレコード数:' + str(n_doc))
        time.sleep(2) #Rate Limitを避けるため。SandBoxでは30回/1分。商用では60回/1分。
        count = count + 1
        print("リクエスト回数:", end="")
        sys.stdout.write("%d, "% count)
        
        res = getTweetData('*******', param_next) #検索ワードを指定・変更
        
        if res['result']==False:
            # 失敗したら終了する
            print("status_code", res['status_code'])
#             print(res['result'])
            break
        
        if int(res['limit']) == 0:    # 回数制限に達したので休憩
            # 日付型の列'created_datetime'を付加する
            print("Adding created_at field.")
            for d in tweetdata.find({'created_datetime':{ "$exists": False }},{'_id':1, 'created_at':1}):
                #print str_to_date_jp(d['created_at'])
                tweetdata.update({'_id' : d['_id']}, 
                     {'$set' : {'created_datetime' : str_to_date_jp(d['created_at'])}})
            #remove_duplicates()
            
            # 待ち時間の計算. リミット＋５秒後に再開する
            diff_sec = int(res['reset_time_unix']) - now_unix_time()
            print("sleep %d sec." % (diff_sec+5))
            if diff_sec > 0:
                time.sleep(diff_sec + 5)
        else:
            if len(res['statuses'])==0:
                sys.stdout.write("statuses is none. ")
            elif res['metadata']:
                # 結果をmongoDBに格納する
                meta.insert({"metadata":res['metadata'], "insert_date": now_unix_time()})
                for s in res['statuses']:
                    tweetdata.insert(s)
                param_next = res['metadata'] #'next' 

#####以下3行を追加
                if param_next == 'finish':
                    sys.stdout.write("next is none. finished.")
                    break
######

            else:
                sys.stdout.write("next is none. finished.")
                break
    except SSLError as xxx_todo_changeme:
        errno = xxx_todo_changeme.args
        print("SSLError({0})".format(errno))
        print("waiting 5mins")
        time.sleep(5*60)
    except ConnectionError as xxx_todo_changeme1:
        errno = xxx_todo_changeme1.args
        print("ConnectionError({0})".format(errno))
        print("waiting 5mins")
        time.sleep(5*60)
    except ReadTimeout as xxx_todo_changeme2:
        errno = xxx_todo_changeme2.args
        print("ReadTimeout({0})".format(errno))
        print("waiting 5mins")
        time.sleep(5*60)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.format_exc(sys.exc_info()[2])
        raise
    finally:
        info = sys.exc_info()
