from flask import session
from flaskdb.model.memoModel import Memo
from flaskdb.model.userModel import User
import datetime
from flaskdb import db

def insert_memo(file, num):
    memo = Memo()
    username = session["username"]
    user = User.query.filter_by(username=username).first()
    memo.file_name = file
    memo.user_id = user.id
    memo.user_name = username
    memo.share = num
    memo.updated_at = datetime.datetime.now()
    db.session.add(memo)
    db.session.commit()

def select_memo():
    memo_list = Memo.query.filter(Memo.share == 1).all()
    for i in range(len(memo_list)):
        days = memo_list[i].updated_at.strftime('%Y/%m/%d %H:%M')
        memo_list[i].updated_at = days
    return memo_list

def select_all_memo():
    memo_list = Memo.query.order_by(Memo.id.asc()).all()
    return memo_list

def delete_memo(file):
    memo_id = Memo.query.filter(Memo.user_name == session["username"] , Memo.file_name == file).one()
    db.session.delete(memo_id)
    db.session.commit()

def update_memo(file, num):
    memo = Memo.query.filter(Memo.user_name == session["username"] , Memo.file_name == file).one()
    memo.share = num
    db.session.commit()

def update_edit_memo(file, title):
    memo = Memo.query.filter(Memo.user_name == session["username"] , Memo.file_name == file).one()
    memo.updated_at = datetime.datetime.now()
    memo.file_name = title
    db.session.commit()

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
