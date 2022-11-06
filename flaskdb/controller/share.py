from crypt import methods
from flask import Blueprint, render_template, url_for, session, flash, redirect
from flaskdb.service.memoService import delete_memo, select_memo, update_memo
from flaskdb.service.shareMDE import share_read_md

share_module = Blueprint("share", __name__)

@share_module.route("/share")
def share_index():
    if not "username" in session:
        flash("もう一度ログインしてください。", "danger")
        return redirect(url_for("auth.login"))

    memo_list = select_memo()
    return render_template('memoShare/share_index.html', mdfiles = memo_list)

@share_module.route("/share/view/<string:file>/<string:username>", methods=["GET"])
def share_view(file, username):
    if not "username" in session:
        flash("もう一度ログインしてください。", "danger")
        return redirect(url_for("auth.login"))
    content = share_read_md(username, file)
    return render_template('memoShare/share_view.html', md=content, file=file)

@share_module.route("/share/stop/<string:file>", methods=["GET"])
def share_stop(file):
    update_memo(file, 0)
    return redirect(url_for('share.share_index'))
   