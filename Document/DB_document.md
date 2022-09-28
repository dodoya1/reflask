# DBについての説明

・Postテーブル

投稿に関するDBです。以下のようなテーブルとなっています。

idとcreated_atは自動でDBに入れられ、titleとbodyを指定しています。

Postテーブル

| id | title | body | created_at |
| :---: | :---: | :---: | :---: |
| TD | TD | TD | TD |
| TD | TD | TD | TD |

・Userテーブル

ユーザーに関するDBです。以下のようなテーブルとなっています。

idは自動でDBに入れられ、usernameとpasswordを指定しています。

passwordはハッシュ化されて保存されます。

Userテーブル

| id | username | password |
| :---: | :---: | :---: |
| TD | TD | TD |
| TD | TD | TD |