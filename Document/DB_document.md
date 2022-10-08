# DBについての説明

・Userテーブル

ユーザーに関するDBです。以下のようなテーブルとなっています。

idは自動でDBに入れられ、usernameとpasswordを指定しています。

passwordはハッシュ化されて保存されます。

Userテーブル

| id | username | password |
| :---: | :---: | :---: |
| TD | TD | TD |
| TD | TD | TD |

・Problemテーブル

出題した問題に関するDBです。以下のようなテーブルとなっています。

user_idは、問題解答対象となるユーザーid。ユーザーがログインしている場合は、session['user_id']を代入が、ログインしていないユーザーの場合は、0を代入する。

originalは、問題文(原文)。

hiraganaは、原文のひらがなver。

babiは、問題の解答となるバビ語。

startは、問題解答開始時間。

timeは、解答までにかかった時間。

lengthは、翻訳語の文章の長さ(hiraganaの長さ)。

scoreは、得点。

judgmentは、正解か不正解かの判定。正解は1、不正解は0とする。

mistakeは、間違えた回数。

finish_timeは、問題終了時刻。

Problemテーブル

| id | user_id | original | hiragana | babi | start | time | length | score | judgment | mistake | finish_time |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| TD | TD | TD | TD | TD | TD | TD | TD | TD | TD | TD | TD |
| TD | TD | TD | TD | TD | TD | TD | TD | TD | TD | TD | TD |