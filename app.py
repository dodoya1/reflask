#フラスクをインポートする。
from flask import Flask,flash
#render_templateは、htmlを読み込むため。requestは、request.methodで、GETかPOSTどちらなのかを調べることができる。
from flask import render_template,request,redirect
#SQLALCHEMYを使うための初期設定。
from flask_sqlalchemy import SQLAlchemy
#ユーザーDBの作成のために必要なライブラリとログインのために必要なライブラリをインポートする。
from flask_login import UserMixin,LoginManager,login_user,logout_user,login_required
#Bootstrapを使うために必要。
from flask_bootstrap import BOOTSTRAP_VERSION, Bootstrap
#パスワードをハッシュ化して保存するためのライブラリをインポート。
from werkzeug.security import generate_password_hash, check_password_hash
#ハッシュ値を使う時などランダムな値を使う時に使う。
import os
#時刻に関するライブラリをインポートする。
from datetime import datetime
#世界標準時を日本時間に直すライブラリをインポートする。
import pytz

app = Flask(__name__)
#SQLALCHEMYを使うための初期設定
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
#セッション情報(ログインしているか否か)を暗号化する。
app.config['SECRET_KEY'] = os.urandom(24)
db=SQLAlchemy(app)
#Bootstrapを使うためにインスタンス化。
bootstrap = Bootstrap(app)

#ログイン機能を持ったLoginManagerをインスタンス化(初期化)。
login_manager=LoginManager()
#appと紐付け。
login_manager.init_app(app)

#Post(投稿)データベースを作る。
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))

#User(ユーザー)データベースを作る。
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12))

#ログイン機能に関するおまじない。
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#ホーム画面
@app.route("/", methods=["GET","POST"])
#このルーティングにアクセスするにはログインが必要である、ということ(アクセス制限)。
@login_required
def index():
    if request.method=="GET":
        #Post.query.all()とすることで、投稿データを全て取ってくる(引用してくる)。list形式。
        posts=Post.query.all()
        #posts=postsとすることで、index.htmlに値を受け渡す。　
        return render_template("index.html",posts=posts)

#新規ユーザー登録画面
#methods ["GET","POST"]により、POSTも受け取れるようになる。
@app.route("/signup", methods=["GET","POST"])
def signup():
    #request.methodで、GETかPOSTどちらなのかを調べることができる。
    if request.method=="POST":
        username=request.form.get("username")
        password =request.form.get("password")

        #UserテーブルにDB作成する。
        user=User(username=username,password=generate_password_hash(password,method="sha256"))
        #追加する。
        db.session.add(user)
        #変更をDBに反映する。
        db.session.commit()

        return redirect("/login")
    else:
        return render_template("signup.html")

#ログイン登録画面
#methods ["GET","POST"]により、POSTも受け取れるようになる。
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
    else:
        return render_template('login.html')

#ログアウト
@app.route('/logout')
#このルーティングにアクセスするにはログインが必要である、ということ(アクセス制限)。
@login_required
def logout():
    #ログアウトする。
    logout_user()
    return redirect('/login')


#新規投稿画面
#methods ["GET","POST"]により、POSTも受け取れるようになる。
@app.route("/create", methods=["GET","POST"])
#このルーティングにアクセスするにはログインが必要である、ということ(アクセス制限)。
@login_required
def create():
    #request.methodで、GETかPOSTどちらなのかを調べることができる。
    if request.method=="POST":
        #request.formによって、新規投稿画面(/create)のformで入力した値を受け取ることができる。
        #さらに「.get("title")」とすることで、フォームのtitleで入力された値を受け取ることができる。
        title=request.form.get("title")
        body=request.form.get("body")

        #Postクラスに、titleとbodyを入れてデータを新規作成する。idとcreated_atは勝手に決定する。
        post=Post(title=title,body=body)
        #追加する。
        db.session.add(post)
        #変更をDBに反映する。
        db.session.commit()

        #ホーム画面に戻る。
        return redirect("/")
    else:
        return render_template("create.html")

#投稿編集画面
#methods ["GET","POST"]により、POSTも受け取れるようになる。
@app.route("/<int:id>/update", methods=["GET","POST"])
#このルーティングにアクセスするにはログインが必要である、ということ(アクセス制限)。
@login_required
def update(id):
    #Post.query.get(id)とすることで、指定したidの投稿データを取ってくる(引用してくる)。
    post=Post.query.get(id)
    #request.methodで、GETかPOSTどちらなのかを調べることができる。
    if request.method=="GET":
        #先ほど指定したidで取ってきた投稿をupdate.htmlに渡す。
        return render_template("update.html",post=post)
    else:
        #上書きすることで更新を行う。
        post.title=request.form.get("title")
        post.body=request.form.get("body")

        #変更をDBに反映する。(更新する場合はcommitするだけでよい。)
        db.session.commit()

        #ホーム画面に戻る。
        return redirect("/")

#削除機能
#GETのみを受け付ける。
@app.route("/<int:id>/delete")
#このルーティングにアクセスするにはログインが必要である、ということ(アクセス制限)。
@login_required
def delete(id):
    #Post.query.get(id)とすることで、指定したidの投稿データを取ってくる(引用してくる)。
    post=Post.query.get(id)
    
    #投稿を削除する。
    db.session.delete(post)
    #変更をDBに反映する。
    db.session.commit()

    #ホーム画面に戻る。
    return redirect("/")