# ポジネガデータの表示
date_dict = defaultdict(int)
spam_dict = defaultdict(int)
count = defaultdict(int)
tweetcount = defaultdict(int)
rtcount  = defaultdict(int)
onlyspamcount = defaultdict(int)
excludespamtweetcount = defaultdict(int)
excludespamrtcount = defaultdict(int)
onlyemospamcount = defaultdict(int)
excludeemospamtweetcount = defaultdict(int)
excludeemospamrtcount = defaultdict(int)
onlybothspamcount = defaultdict(int)
excludebothspamtweetcount = defaultdict(int)
excludebothspamrtcount = defaultdict(int)

for d in tweetdata.find({},{'created_datetime':1,'emo_val':1, 'retweeted_status':1,'spam':1,'emospam':1}):
    str_date = date_to_Japan_time(d['created_datetime']).strftime('%Y\t%m/%d %H %a')
    date_dict[str_date] += 1
    
    if 'emo_val' in d:
        count[str_date] += d['emo_val']
        
        # spamの除去
    if ('spam' in d) and (d['spam'] == True):
        onlyspamcount[str_date] += d['emo_val']
    else:
        onlyspamcount[str_date] += 0
        # spamでのRetweet数のカウント
        if 'retweeted_status' not in d:
            excludespamrtcount[str_date]  += 0
            excludespamtweetcount[str_date] += d['emo_val']
        elif obj_nullcheck(d['retweeted_status']):
            excludespamrtcount[str_date]  += d['emo_val']
            excludespamtweetcount[str_date] += 0
        else:
            excludespamrtcount[str_date]  += 0
            excludespamtweetcount[str_date] += d['emo_val']
            
        # emospamの除去
    if ('emospam' in d) and (d['emospam'] == True):
        onlyemospamcount[str_date] += d['emo_val']
    else:
        onlyemospamcount[str_date] += 0
        # spamでのRetweet数のカウント
        if 'retweeted_status' not in d:
            excludeemospamrtcount[str_date]  += 0
            excludeemospamtweetcount[str_date] += d['emo_val']
        elif obj_nullcheck(d['retweeted_status']):
            excludeemospamrtcount[str_date]  += d['emo_val']
            excludeemospamtweetcount[str_date] += 0
        else:
            excludeemospamrtcount[str_date]  += 0
            excludeemospamtweetcount[str_date] += d['emo_val']
            
    # emoとspamの両方除去
    if ('emospam' in d) and (d['emospam'] == True) or ('spam' in d) and (d['spam'] == True) :
        onlybothspamcount[str_date] += d['emo_val']
    else:
        onlyemospamcount[str_date] += 0
        # spamでのRetweet数のカウント
        if 'retweeted_status' not in d:
            excludebothspamrtcount[str_date]  += 0
            excludebothspamtweetcount[str_date] += d['emo_val']
        elif obj_nullcheck(d['retweeted_status']):
            excludebothspamrtcount[str_date]  += d['emo_val']
            excludebothspamtweetcount[str_date] += 0
        else:
            excludebothspamrtcount[str_date]  += 0
            excludebothspamtweetcount[str_date] += d['emo_val']
    
    # Retweet数のカウント
    if 'retweeted_status' not in d:
        rtcount[str_date]  += 0
        tweetcount[str_date] += d['emo_val']
    elif obj_nullcheck(d['retweeted_status']):
        rtcount[str_date]  += d['emo_val']
        tweetcount[str_date] += 0
    else:
        rtcount[str_date]  += 0
        tweetcount[str_date] += d['emo_val']

print(("日付" + "\t\t\t" + "#ALL_emo" + "\t" + "#NotRT_emo" + "\t" + "#RT_emo" + "\t" "#spam_emo" + "\t" "#NotRT(exclude spam)_emo" + "\t" + "#RT(exclude spam)_emo" + "\t" "#emospam_emo" + "\t" "#NotRT(exclude emospam)_emo" + "\t" + "#RT(exclude emospam)_emo"+ "\t" "#bothspam" + "\t" "#NotRT(exclude bothspam)" + "\t" + "#RT(exclude bothspam)"))
keys = list(date_dict.keys())
keys.sort()
for k in keys:
    print((k  + "\t" +  str(count[k]) + "\t" +  str(tweetcount[k]) + "\t" +  str(rtcount[k]) \
          + "\t" +  str(onlyspamcount[k])+ "\t" +  str(excludespamtweetcount[k]) + "\t" +  str(excludespamrtcount[k]) \
          + "\t" +  str(onlyemospamcount[k])+ "\t" +  str(excludeemospamtweetcount[k]) + "\t" +  str(excludeemospamrtcount[k]) \
           + "\t" +  str(onlybothspamcount[k])+ "\t" +  str(excludebothspamtweetcount[k]) + "\t" +  str(excludebothspamrtcount[k])))