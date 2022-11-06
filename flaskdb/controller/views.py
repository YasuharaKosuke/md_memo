from flask import Blueprint, request, session, render_template, redirect, flash, url_for

from flaskdb import apps, db, da
from flaskdb.model.userModel import User

from flaskdb.service.memoService import select_memo, select_all_memo

app = Blueprint("app", __name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if not "username" in session:
        flash("もう一度ログインしてください。", "danger")
        return redirect(url_for("auth.login"))

    memo_list = select_all_memo()
    memo_md = []
    for num in range(len(memo_list)):
        if session['username'] == memo_list[num].user_name:
            memo_md.append(memo_list[num])
    return render_template("index.html", mdfiles = memo_md)


# This is a very danger method
@app.route("/receive", methods=["GET", "POST"])
def receive():
    if request.method == "GET":
        username = request.args.get("username")
        password = request.args.get("password")
    else:
        username = request.form["username"]
        password = request.form["password"]

    return render_template("receive.html", username=username, password=password)


@app.route("/initdb", methods=["GET", "POST"])
def initdb():
    db.drop_all()
    db.create_all()
    
    admin = User(username="admin", password="password")
    user = User(username="user", password="password")
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()
    return "initidb() method was executed. "
