# flaskをインポートして使えるようにする
import sqlite3
from flask import Flask, render_template, request, redirect, session

# appという名前でFlaskアプリを作っていくよ
app = Flask(__name__)

app.secret_key = "sunabaco"


# ルーティングの作成 ('')のなかがルーティング
@app.route('/')
def helloworld():
    print("4444A")
    return "Hello world"


@app.route('/name/<name>')
def greet(name):
    return name + "さん、こんにちは！"


@app.route('/template')
def template():
    py_name = 'すなばこ'
    return render_template("index.html",name = py_name)


@app.route('/weather')
def weather():
    now_weather = '晴れ'
    return render_template('weather.html',weather = now_weather)


@app.route('/temptest')
def address():
    name = "sunabaco"
    age = "21"
    address = "kumamoto"
    return render_template("temptest.html",py_name = name,py_age = age,py_address = address)


@app.route('/dbtest')
def dbtest():
    # dbtest.dbへの接続
    conn = sqlite3.connect('dbtest.db')
    # 中身を見れるようにする
    c = conn.cursor()
    # sql文の実行
    c.execute("select name, age, address from address")
    # とってきたデータを格納
    user_info = c.fetchone()
    # データベースとの接続を終了
    c.close()
    # print(user_info)
    return render_template("dbtest.html",user_info=user_info)


@app.route('/add',methods = ["GET"])
def add_get():
    if 'user_id' in session:
        return render_template("add.html")
    else:
        return redirect('/login')


@app.route('/add',methods = ["POST"])
def add_post():
    user_id = session['user_id']
    # 入力フォームのデータを取得
    task = request.form.get("task")
    # DB接続
    conn = sqlite3.connect('dbtest.db')
    c = conn.cursor()
    c.execute("insert into task values(null,?,?)",(task,user_id))
    conn.commit()
    c.close()
    return redirect("/list")


@app.route("/list")
def list():
    if 'user_id' in session:
        user_id = session['user_id']
        conn = sqlite3.connect('dbtest.db')
        c = conn.cursor()
        c.execute("select name from user where id = ?",(user_id,))
        user_name = c.fetchone()[0]
        c.execute("select id,task from task where user_id = ?",(user_id,))
        task_list = []
        for row in c.fetchall():
            # i = row [0]
            # print(str(i)+"週目"+str(row))
            task_list.append({"id":row[0],"task":row[1]})
        c.close()
        # print(task_list)
        return render_template("list.html", task_list=task_list , user_name = user_name)
    else:
        return redirect('/login')


@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' in session:
        conn = sqlite3.connect('dbtest.db')
        c = conn.cursor()
        c.execute("select task from task where id = ?",(id,))
        task = c.fetchone()
        c.close()
        if task is not None:
            task = task[0]
        else:
            return "タスクがないよ"
        item = {"id":id, "task":task}
        return render_template("edit.html",item=item)
    else:
        return redirect('/login')


@app.route('/edit',methods=['POST'])
def edit_post():
    # 入力フォームのデータを取ってくる
    task_id = request.form.get("task_id")
    task = request.form.get("task")
    # データベースと接続
    conn = sqlite3.connect('dbtest.db')
    c = conn.cursor()
    # データの更新
    c.execute("update task set task = ? where id = ?",(task,task_id))
    conn.commit()
    c.close()
    # /listを表示
    return redirect('/list')


# 削除機能をつけよう
# リストの編集ボタンの横に削除ボタンを作る
# 削除用のルーティングを作りタスクを削除
# /listを表示する

# 削除に必要なものはタスクのID

@app.route("/del/<int:id>")
def del_task(id):
    if 'user_id' in session:
        # データベースと接続
        conn = sqlite3.connect('dbtest.db')
        c = conn.cursor()
        # データの更新
        c.execute("delete from task where id = ?",(id,))
        conn.commit()
        c.close()
        return redirect("/list")
    else:
        return redirect('/login')


@app.route('/regist', methods=['GET'])
def regist_get():
    if 'user_id' in session:
        return redirect('/list')
    else:
        return render_template("regist.html")


@app.route('/regist',methods=['POST'])
def regist_post():
    # 入力フォームのデータを取得
    name = request.form.get("user_name")
    password = request.form.get("password")
    # DB接続
    conn = sqlite3.connect('dbtest.db')
    c = conn.cursor()
    c.execute("insert into user values(null,?,?)",(name,password))
    conn.commit()
    c.close()
    return redirect('/list')


@app.route('/login',methods=['GET'])
def login_get():
    if 'user_id' in session:
        return redirect('/login')
    else:
        return render_template('login.html')


@app.route('/login',methods=['POST'])
def login_post():
    # 入力フォームのデータを取得
    name = request.form.get("user_name")
    password = request.form.get("password")
    # DB接続
    conn = sqlite3.connect('dbtest.db')
    c = conn.cursor()
    c.execute("select id from user where name = ? and password = ?",(name,password))
    user_id = c.fetchone()
    c.close()
    if user_id is None:
        return render_template('login.html')
    else:
        session['user_id'] =  user_id[0]
    return redirect('/list')


@app.route('/logout')
def logout():
    session.pop('user_id',None)
    return redirect('/login')














@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404





if __name__ == '__main__':
    # コードを走らせるための記述、開発用サーバーを起動する
    app.run(debug=True)