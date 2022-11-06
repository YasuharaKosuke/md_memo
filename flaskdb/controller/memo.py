from flask import Blueprint, request, session, render_template, redirect, flash, url_for, Markup
from werkzeug.utils import secure_filename
import sys

from flaskdb.service.memoMDE import memo_MDE
from flaskdb.service.mainService import catch_img, file_name_list, private_dir, private_file_rename, private_image_dir
from flaskdb.service.memoService import allowed_file, insert_memo, select_memo, update_edit_memo, update_memo, delete_memo

memo_module = Blueprint("memo", __name__)


@memo_module.route("/view/<string:file>", methods=["GET"])
def memo_view(file):
    if not "username" in session:
        flash("もう一度ログインしてください。", "danger")
        return redirect(url_for("auth.login"))
    content = memo_MDE(file).read_md()
    return render_template('memo/memo_view.html', md=content, file=file)


@memo_module.route("/edit/<string:file>", methods=["GET", "POST"])
def memo_edit(file):
    if not "username" in session:
        flash("もう一度ログインしてください。", "danger")
        return redirect(url_for("auth.login"))
    session['now_url'] = request.url
    img_list = catch_img(session['username'])
    if request.method == "POST":
        content = request.form["data"] 
        title = request.form["title"]
        # ファイル名変更チェック
        if title != file:
            # 重複チェック
            mdfile_list = file_name_list()
            if title in mdfile_list:
                memo_MDE(file).write_md(content)
                markcontent = memo_MDE(file).read_md()
                return render_template("memo/memo_edit.html", data=content, markcontent=markcontent, file=file, errortext = True, img=img_list)    

            update_edit_memo(file, title)
            private_file_rename(file, title)
        memo_MDE(title).write_md(content)
        markcontent = memo_MDE(title).read_md()
        return render_template("memo/memo_edit.html", data=content, markcontent=markcontent, file=title, img=img_list)
    else:
        content, markcontent = memo_MDE(file).read_edit_md()
        return render_template("memo/memo_edit.html", data=content, markcontent=markcontent, file=file, img=img_list)


@memo_module.route("/add", methods=["GET", "POST"])
def memo_add():
    if not "username" in session:
        flash("もう一度ログインしてください。", "danger")
        return redirect(url_for("auth.login"))
    session['now_url'] = request.url
    img_list = catch_img(session['username'])
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["data"] 
        mdfile_list = file_name_list()
        if title in mdfile_list:
            return render_template("memo/memo_add.html", data=content, file="", errortext = True, img=img_list)
        insert_memo(title, 0)
        memo_MDE(title).write_md(content)
        return redirect(url_for("memo.memo_edit", file=title))
    else:
        return render_template("memo/memo_add.html", file="", img=img_list)


@memo_module.route("/delete/<string:file>", methods=["GET"])
def memo_delete(file):
    memo_MDE(file).delete_md()
    delete_memo(file)
    return redirect(url_for("app.index"))

@memo_module.route("/public/<string:file>", methods=["GET"])
def memo_share(file):
    if not "username" in session:
        return redirect(url_for("auth.login"))

    memo_list = select_memo()
    username = session["username"]
    for memo in memo_list:
        if username == memo.user_name and file == memo.file_name:
            return redirect(url_for("app.index"))
            
    update_memo(file, 1)
    return redirect(url_for("app.index"))


@memo_module.route("/stop/<string:file>", methods=["GET"])
def memo_stop(file):
    update_memo(file, 0)
    return redirect(url_for('app.index'))


@memo_module.route("/upload_file", methods=["POST"])
def uploads_file():
    back_url = session["now_url"]
    session["now_url"] = ""
    if 'file' not in request.files:
        flash('ファイルがありません')
        return redirect(back_url)
    file = request.files["file"]
    if file.filename == '':
        flash('ファイルがありません')
        return redirect(back_url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(private_image_dir(session["username"]) + "/" + filename)
        return redirect(back_url)

