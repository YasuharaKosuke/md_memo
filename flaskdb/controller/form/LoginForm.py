from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length
from flaskdb.service.widgets import ButtonField

class LoginForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators = [
            DataRequired(message="ユーザー名は必要です。"),
            length(max=64, message="ユーザー名は64文字以内にしてください。"),
        ],
    )
    password = PasswordField(
        "パスワード",
        validators = [
            DataRequired(message="パスワードは必要です。"),
        ],
    )
    cancel = ButtonField("キャンセル")
    submit = SubmitField("ログイン")

    def copy_from(self, user):
        self.username.data = user.username
        self.password.data = user.password

    def copy_to(self, user):
        user.username = self.username.data
        user.password = self.password.data
