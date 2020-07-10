# Tweet本文をMecabにかけて形態要素に分解
# Tweetデータに品詞ごとの属性noun, verb, adjective, adverbとして追加する。

# mecab 形態要素分解
def mecab_analysis(sentence):
    t = mc.Tagger('Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd') #パスを変更
    #sentence = u"今日は良い天気ですが、雨ですね。クルマがほしいです。走ります。"
    sentence = sentence.replace('\n', ' ')
    #print(sentence)
    #text = sentence.encode('utf-8')  #utf-8エンコード済みなのでコメントアウト
    #print(text)
    node = t.parseToNode(sentence) 
    result_dict = defaultdict(list)
    for i in range(140):
        if node.surface != "":  # ヘッダとフッタを除外
            word_type = node.feature.split(",")[0]
            if word_type in ["名詞", "形容詞", "動詞"]:
                plain_word = node.feature.split(",")[6]
                if plain_word !="*":
                    #result_dict[word_type.decode('utf-8')].append(plain_word.decode('utf-8')) 
                    result_dict[word_type].append(plain_word)

            # 地域名称を独立のFieldとして格納
            if (node.feature.split(",")[1] == "固有名詞") and (node.feature.split(",")[2] == "地域"):
                plain_word = node.feature.split(",")[6]
                if plain_word !="*":
                    #result_dict['地域名称'].append(plain_word.decode('utf-8'))#utf-8デコード済みなのでコメントアウト 
                    result_dict['地域名称'].append(plain_word)
                    
        node = node.next
        if node is None:
            break
    return result_dict

#進捗状況が分かるように以下三行追加
count = 0 
n_doc = tweetdata.find({}).count()
print(n_doc, '件を処理します...')

for d in tweetdata.find({},{'_id':1, 'id':1, 'text':1,'noun':1,'verb':1,'adjective':1,'adverb':1,'mecabed':1}): 
    #一度も形態素解析していないと動かないコードだったので上記変更。解析済みのmecabed=Trueはスキップする

    if d.get('mecabed') == True: #解析済みはスキップ
        continue
        
    res = mecab_analysis(unicodedata.normalize('NFKC', d['text'])) # 半角カナを全角カナに
#     print(res)
    for k in list(res.keys()):
        if k == '形容詞': # adjective  
            adjective_list = []    
            for w in res[k]:
                adjective_list.append(w)
            tweetdata.update({'_id' : d['_id']},{'$push': {'adjective':{'$each':adjective_list}}})
        elif k == '動詞': # verb
            verb_list = []
            for w in res[k]:
#                 print(k, w)
                verb_list.append(w)
            tweetdata.update({'_id' : d['_id']},{'$push': {'verb':{'$each':verb_list}}})
        elif k == '名詞': # noun
            noun_list = []
            for w in res[k]:
                noun_list.append(w)
            tweetdata.update({'_id' : d['_id']},{'$push': {'noun':{'$each':noun_list}}})
        elif k == '副詞': # adverb
            adverb_list = []
            for w in res[k]:
                adverb_list.append(w)
            tweetdata.update({'_id' : d['_id']},{'$push': {'adverb':{'$each':adverb_list}}})
    # 形態要素分解済みとしてMecabedフラグの追加
    tweetdata.update({'_id' : d['_id']},{'$set': {'mecabed':True}})
    
    count += 1 #進捗状況が分かるように追加
    
    if count % 10000 == 0: #進捗状況が分かるように追加
        print(str(count)+'件処理済', str(round((100*count/n_doc),2)) + '%')

#以下、終了表示を追加
print('終了') 
print('例として一件目のレコードを表示')
print(tweetdata.find_one())