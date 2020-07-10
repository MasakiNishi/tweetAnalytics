# spamアカウントのツイートにspamフラグを付与する

spam_twitter = set() #変数が未定義だったため追加

#  08_spam_detector.pyであぶり出したスパムアカウントのリスト
spam_list = ['********', '********', '********']

count = 0
rtcount = 0
retweeted_name = ""

for d in tweetdata.find({'retweeted_status':{"$ne": None}}):
    try:
        retweeted_name = d['entities']['user_mentions'][0]['screen_name']
    except:
        pattern = r".*@([0-9a-zA-Z_]*).*"
        ite = re.finditer(pattern, d['text'])
        for it in ite:
            retweeted_name = it.group(1)
            break

    if retweeted_name in spam_list:
        # スパムアカウントへのリツイートにspamフラグを付与
        tweetdata.update({'_id' : d['_id']},{'$set': {'spam':True}})
        rtcount += 1
        # スパムツイートをしたアカウントもブラックリスト入り
        spam_twitter.add(d['user']['screen_name'])
        
print(rtcount, '件のリツイートをスパムに分類しました')

# ブラックリスト入りのユーザーのツイートをスパムに分類
count = 0
for d in tweetdata.find({},{'user.screen_name':1}):
    sc_name = d['user']['screen_name'] 

    if sc_name in spam_twitter:
        count += 1
        tweetdata.update({'_id' : d['_id']},{'$set': {'spam':True}})

print(count, "件のツイートをスパムに分類しました")