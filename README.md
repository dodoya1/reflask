# プロジェクトの説明

FlaskによるWebアプリ「バビ検」を開発しました。このプロジェクトは、Flskによって作られています。Flaskは、プログラミング言語Python用の、軽量なウェブアプリケーションフレームワークです。

メイン機能は既に実装しましたが、現在も細かな修正や更なる機能の実装をしています。

# 「バビ検」とは

バビ検とは、提示された文章をユーザーがバビ語に翻訳するサイトです。与えられた文章の長さ、翻訳するまでにかかった時間から得点が算出され、ランキングが決定します。

バビ語とは、入れ詞の一種です。例えば「おはよう」はバビ語で「おぼはばよぼうぶ」となります。つまり、言葉の間に「ばびぶべぼ」を入れます。付け足す音は、直前の文字の母音とするという決まりがあります。「ん」には「ぶ」を適用します。

# コードの説明

コードの説明はDocumentフォルダ内のファイルに記載している。

・DB_document.mdにはDBに関する説明。

・function_document.mdには各機能についての説明。

・routing.mdには各ルーティングの説明。

・SCREEN_document.mdには各画面(.html)についての説明。

# 導入手順

1. pythonのダウンロード[https://www.python.org/downloads/](https://www.python.org/downloads/)

1. 仮想環境の作成 
    - Mac

      ターミナルで以下を実行
      ```
      $ python3 -m venv venv
      ```
      <br>

    - Windows
      
      ```
      > py -3 -m venv venv
      ```
      <br>

2. 仮想環境の有効化
    - Mac

      ターミナルで以下を実行
      ```
      $ . venv/bin/activate
      ```
      <br>

    - Windows

      ```
      > venv\Scripts\activate
      ```
      <br>

3. ライブラリのインストール
      ```
      $ pip install Flask
      ```
    さらに、.pyファイルを確認し、不足している必要なライブラリのインストールをしてください。

4. サーバーの起動
    ```
    (venv) flask --app app --debug run
    ```


## 備考
- データベースを作成するために、ターミナルにおいてPython3を実行し、対話モードにした後、
    ```
    from app import db
    db.create_all()
    ```
    のように実行する必要があるかもしれません。
    詳細は[Flaskドキュメント](https://flask.palletsprojects.com/en/2.2.x/)を確認してください。

# 参考文献

## Flask関連

[【完全版】この動画1本でFlaskの基礎を習得！（Flask超入門）](https://youtu.be/VtJ-fGm4gNg)

[Flaskドキュメント](https://flask.palletsprojects.com/en/2.2.x/)

## Bootstrap関連

Bootstrapの使い方は、基本的に[Bootstrapドキュメント](https://getbootstrap.jp/docs/5.0/getting-started/introduction/)を見ながら、classを付与するだけ。

[Bootstrap 4入門](https://youtube.com/playlist?list=PLh6V6_7fbbo9sHm8E3F7lZuDDxDJkheKD)→めちゃくちゃわかりやすい動画で、参考にすると良い。Bootstrapとは、ざっくり言うと、CSS書くのが面倒だからちょこちょこって書き加えたら良い感じに装飾してくれるWebアプリケーションフレームワークのこと。

◎[チートシート～Bootstrap5設置ガイド](https://bootstrap-guide.com/sample/cheatsheet)、[Bootstrap 5 CheatSheet](https://bootstrap-cheatsheet.themeselection.com/)→どういった装飾になるのかを見ながら選ぶことができ、非常にわかりやすい。

◎[Start Bootstrap](https://startbootstrap.com/)→自分の好みのテンプレートをダウンロードし、コードをいじってカスタマイズすることができます。一からコードを書く必要がないので、Bootstrapを使う際はこちらを使えば良いでしょう。使い方は[この動画](https://youtu.be/xdqs06t1Rp8)を見ると良いでしょう。

また、Bootstrapのデフォルト状態では少し物足りないと感じた場合は、もちろんクラスを追加するなどして調整することができる。

## その他

[renderとredirectの違いって何？](https://media.wemotion.co.jp/class-diary/%E3%80%90%E7%9F%AD%E7%B7%A8%E3%82%B3%E3%83%A9%E3%83%A0%E3%80%91render%E3%81%A8redirect%E3%81%AE%E9%81%95%E3%81%84%E3%81%A3%E3%81%A6%E4%BD%95%EF%BC%9F%E3%80%90rails%E3%80%91/)

> **Render**→「viewを指定するだけの処理」

> **Redirect**→データ送信など「Controllerの処理を必要とするもの」

> 例えばログイン機能などでログインに失敗した時にエラーページを表示するのが**Render**。

> **Redirect**が、ログインに成功したときなどにデータを更新/送信する場合などに使われるもの。