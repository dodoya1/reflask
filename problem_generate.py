import re
from pykakasi import kakasi
#外部ファイルをインポート(文章を自動生成するファイル)
import create_sentence
#カタカナをひらがなに変換する。
import jaconv

kakasi = kakasi()       # オブジェクトをインスタンス化

#問題を作成する関数。
def generate():
    original=create_sentence.main()    ##原文を自動生成する処理。原文
    hiragana=toHira(original)  #ひらがなに変換
    babi=tobabi(hiragana)      #バビ語に変換
    return original,hiragana,babi

#バビ語に変換する関数
def tobabi(hira: str) -> str:
    result = ''
    length = len(hira) - 1

    for idx, letter in enumerate(hira):
        next_letter = hira[idx+1:idx+2]

        if (next_letter in 'ぁぃぅぇぉゃゅょ') & (idx < length):
            pass
        elif letter in 'あかがさざただなはばぱまやらわゎ':
            result += (letter + 'ば')
        elif letter in 'いきぎしじちぢにひびぴみり':
            result += (letter + 'び')
        elif letter in 'うゔくぐすずつづぬふぶぷむゆるん':
            result += (letter + 'ぶ')
        elif letter in 'えけげせぜてでねへべぺめれ':
            result += (letter + 'べ')
        elif letter in 'おこごそぞとどのほぼぽもよろを':
            result += (letter + 'ぼ')
        elif letter in 'ぁゃ':
            result += (hira[idx-1:idx] + letter + 'ば')
        elif letter in 'ぃ':
            result += (hira[idx-1:idx] + letter + 'び')
        elif letter in 'ぅゅ':
            result += (hira[idx-1:idx] + letter + 'ぶ')
        elif letter in 'ぇ':
            result += (hira[idx-1:idx] + letter + 'べ')
        elif letter in 'ぉょ':
            result += (hira[idx-1:idx] + letter + 'ぼ')
        elif (letter in 'ー〜') & (idx < length):
            result += (letter + result[-1])
        else:
            result += letter
    return result

#(漢字やカタカナを)ひらがなに変換する関数
def toHira(text):
    # モードの設定：J(Kanji) to H(Hiragana)
    kakasi.setMode('J', 'H') 
    # 変換して出力
    conv = kakasi.getConverter()
    #漢字をひらがなorカタカナに
    rekatakana=conv.do(text)
    #カタカナをひらがなに変換する。
    change_word1 = jaconv.kata2hira(rekatakana)
    return change_word1