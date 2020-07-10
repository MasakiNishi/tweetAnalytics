#Mecab インストール (Jupyter Notebook用)
!pip install mecab-python3
!pip install neologdn

import MeCab
import neologdn #基本的には未使用

#Mecabテスト
m_test = MeCab.Tagger('Ochasen')
print(m_test.parse('徳川家康が江戸幕府を建てました'))

m_test2 = MeCab.Tagger('Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd') #カスタム辞書
print(m_test2.parse('徳川家康が江戸幕府を建てました'))