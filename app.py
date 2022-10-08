#フラスクをインポートする。
from flask import Flask,flash,session #session追加
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
#外部ファイルをインポート
import problem_generate
#URLを関数名で指定するために
from flask import url_for
#タイマー
import time

app = Flask(__name__)
#SQLALCHEMYを使うための初期設定
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///babi.db"
#セッション情報(ログインしているか否か)を暗号化する。
app.config['SECRET_KEY'] = os.urandom(24)
db=SQLAlchemy(app)
#Bootstrapを使うためにインスタンス化。
bootstrap = Bootstrap(app)

#ログイン機能を持ったLoginManagerをインスタンス化(初期化)。
login_manager=LoginManager()
#appと紐付け。
login_manager.init_app(app)

#User(ユーザー)データベースを作る。
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12))

#Result(過去正解問題)データベースを作る。
class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #ユーザーid(対象者)
    user_id=db.Column(db.Integer,nullable=False)
    #原文
    original=db.Column(db.String, nullable=False)
    #ひらがな
    hiragana=db.Column(db.String, nullable=False)
    #バビ語
    babi=db.Column(db.String, nullable=False)
    #出題日時
    start = db.Column(db.Float)
    #正解までにかかった時間
    time=db.Column(db.Float)
    #文字数
    length=db.Column(db.Integer,nullable=False)
    #得点(デフォルトは0)
    score=db.Column(db.Integer,default=0)
    #判定
    judgment=db.Column(db.Integer)
    #間違えた回数。(デフォルトは0)
    mistake=db.Column(db.Integer,default=0)
    #終了時間(年月日時)
    finish_time = db.Column(db.DateTime)

#ログイン機能に関するおまじない。
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#ホーム画面
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

#問題作成
@app.route("/problem_generation", methods=["GET"])
def problem_generation():
    #原文、原文(平仮名ver)、バビ語を受け取る。
    original,hiragana,babi=problem_generate.generate()
    #原文(平仮名ver)の長さ
    length=len(hiragana)
    #問題を解答する対象ユーザー。ログインしていない場合は、0。
    if "user_id" in session:
        user_id=session['user_id']
    else:
        user_id=0
    #Problemテーブルに問題保存する。
    problem=Problem(user_id=user_id,original=original,hiragana=hiragana,babi=babi,length=length)
    #追加する。
    db.session.add(problem)
    #変更をDBに反映する。
    db.session.commit()
    #今Problemテーブルに追加したデータのidを取得。
    problem_id=problem.id
    return redirect(f"/questions/{problem_id}")

#問題出題・解答画面
@app.route("/questions/<int:questions_id>", methods=["GET","POST"])
def questions(questions_id):
    #指定したidのProblemデータを取得。
    problem=Problem.query.get(questions_id)
    #翻訳語の文の長さ。
    length=problem.length
    if request.method=="POST":
        #解答を受け取る。
        answer=request.form.get("answer")
        #解答が正解の場合。
        if answer==problem.babi:
            #問題正解時刻を変数に代入する。
            stop_time=time.time()
            #正解までにかかった時間を出力。
            result_time=stop_time-problem.start
            #Problemテーブルに情報を追加する。かかった時間は小数点以下2桁（小数点第三位を四捨五入）とする。
            problem.time=round(result_time, 2)
            #得点算出する。(得点)=(文字数)-(かかった時間-(文字数)*3)*2。×2は、得点を高くしてエンターテイメント性を高めるため。
            score=length-(int(result_time)-(length)*3)*2
            #もし0点以下の場合は、10点にする。(正解したご褒美)
            if score<=0:
                score=10
            #int型に直す。
            result_time=int(result_time)
            #Problemテーブルに情報を追加する。
            problem.finish_time=datetime.now(pytz.timezone('Asia/Tokyo'))
            problem.score=score
            problem.judgment=1
            #変更をDBに反映する。(更新する場合はcommitするだけでよい。)
            db.session.commit()

            return redirect(f"/results/{questions_id}")
        #解答が不正解の場合。
        #return redirect(f"/questions/{questions_id}")
        else:
            #間違えた回数を更新。
            problem.mistake+=1
            db.session.commit()
            #間違えた回数が3回の場合。
            if problem.mistake==3:
                #不正解であったとProbelemテーブルを更新。
                problem.finish_time=datetime.now(pytz.timezone('Asia/Tokyo'))
                problem.judgment=0
                db.session.commit()
                return redirect(f"/results/{questions_id}")
            else:
                return render_template("question.html",problem=problem)
    else:
        #ログインしていないユーザーの場合。
        if problem.user_id==0:
            #試験開始時刻をProblemテーブルに保存する。
            problem.start=time.time()
            db.session.commit()
            return render_template("question.html",problem=problem)
        #問題の解答対象ユーザーの場合。
        if problem.user_id==session['user_id']:
            #試験開始時刻をProblemテーブルに保存する。
            problem.start=time.time()
            db.session.commit()
            return render_template("question.html",problem=problem)
        else:
            return redirect("/")

#結果表示画面
@app.route("/results/<int:questions_id>", methods=["GET"])
def results(questions_id):
    #指定したidのProblemデータを取得。
    problem=Problem.query.get(questions_id)
    #問題解答対象者のユーザーnameを取得。
    #「problem.use_id==0」すなわち、ゲストユーザーの場合。
    if problem.user_id==0:
        username="ゲストユーザー"
        return render_template("result.html",problem=problem,username=username)
    else:
        user=User.query.get(problem.user_id)
        username=user.username
        return render_template("result.html",problem=problem,username=username)

#ランキング画面
@app.route("/ranking", methods=["GET"])
def ranking():
    problem_all=Problem.query.all()
    #得点が高い順にソートする。
    #[ユーザー、得点、ユーザーid]というリストを新たに作成する。
    ranking=[]
    for i in range(len(problem_all)):
        problem=Problem.query.get(i+1)
        #ゲストユーザーの場合。
        if problem.user_id==0:
            ranking.append([0,problem.score,0])
        else:
            user=User.query.get(problem.user_id)
            ranking.append([user.username,problem.score,problem.user_id])
    ranking = sorted(ranking, reverse=True, key=lambda x:x[1])
    ranking_len=len(ranking)
    return render_template("ranking.html",ranking=ranking,ranking_len=ranking_len)

#マイページ画面
@app.route("/mypage", methods=["GET"])
def mypage():
    user = User.query.get(session['user_id'])
    problem_all=Problem.query.all()
    #得点が高い順にソートする。
    #[Problemテーブルのid、得点、ユーザーid]というリストを新たに作成する。
    ranking=[]
    for i in range(len(problem_all)):
        problem=Problem.query.get(i+1)
        #ゲストユーザーの場合。
        if problem.user_id==0:
            ranking.append([i+1,problem.score,0])
        else:
            user=User.query.get(problem.user_id)
            ranking.append([i+1,problem.score,problem.user_id])
    #(最終)ランキング結果
    ranking = sorted(ranking, reverse=True, key=lambda x:x[1])

    #自分のランキングについての処理。
    #[id(Problemテーブルの)、得点、何位]
    my_result=[]
    #最高ランキング(初期値は十分大きい値)
    best_rank=10**23
    #最高得点
    best_score=0
    #順位
    count=0
    for rank in ranking:
        count+=1
        #自分対象の問題の場合
        if rank[2]==session['user_id']:
            best_rank=min(best_rank,count)
            best_score=max(best_score,rank[1])
            my_result.append([rank[0],rank[1],count])
        
    return render_template("mypage.html",user=user,best_rank=best_rank,my_result=my_result,best_score=best_score)

#ユーザー画面
@app.route("/users/<int:user_id>", methods=["GET"])
def users(user_id):
    user = User.query.get(user_id)
    return render_template("user.html",user=user)

#新規ユーザー登録画面
#methods ["GET","POST"]により、POSTも受け取れるようになる。
@app.route("/signup", methods=["GET","POST"])
def signup():
    #request.methodで、GETかPOSTどちらなのかを調べることができる。
    if request.method=="POST":
        username=request.form.get("username")
        password =request.form.get("password")

        if User.query.filter_by(username=username).first():
            flash("このユーザー名は既に使われているため使えません")
            return render_template("signup.html")
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
        #入力に一致したユーザー名が存在しない場合。
        if user == None:
            flash("ユーザー名またはパスワードが間違っています")
            return render_template('login.html')
        else:
            if check_password_hash(user.password, password):
                #sessionにuser情報を保存
                session['user_id'] = user.id
                login_user(user)
                return redirect('/')
            else:
                flash("ユーザー名またはパスワードが間違っています")
                return render_template('login.html')
    else:
        return render_template('login.html')

#ログアウト
@app.route('/logout')
#このルーティングにアクセスするにはログインが必要である、ということ(アクセス制限)。
@login_required
def logout():
    #セッション削除
    session.pop('user_id', None)
    #ログアウトする。
    logout_user()
    return redirect('/login')