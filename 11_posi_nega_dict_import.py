#辞書データをダウンロードし、python実行ファイルと同一フォルダにおいてください。

# 単語のポジ・ネガ辞書のインポート
# データは日本語評価極性辞書 - 乾・岡崎研究室からダウンロード
# http://www.cl.ecei.tohoku.ac.jp/index.php?Open%20Resources%2FJapanese%20Sentiment%20Polarity%20Dictionary

#　日本語評価極性辞書（用言編）ver.1.0（2008年12月版）のインポート
with open("wago.121808.pn", 'r') as f:
    for l in f.readlines():
        l = l.split('\t')
        l[1] = l[1].replace(" ","").replace('\n','')
        value = 1 if l[0].split('（')[0]=="ポジ" else -1
        print((l[1], value))
        
        posi_nega_dict.insert({"word":l[1],"value":value})  

# 日本語評価極性辞書（名詞編）ver.1.0（2008年12月版）のインポート
with open("pn.csv.m3.120408.trim", 'r') as f:
    for l in f.readlines():
        l = l.split('\t')

        if l[1]=="p":
            value = 1
        elif l[1]=="e":
            value = 0
        elif l[1]=="n":
            value = -1

        print((l[0], value))
        
        posi_nega_dict.insert({"word":l[0],"value":value}) 

print(posi_nega_dict)