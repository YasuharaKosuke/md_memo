from flask import Flask
apps = Flask(__name__, static_folder="view/static", template_folder="view/templates")
apps.config.from_object("flaskdb.config")

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(apps)

from flaskdb.repository.dataaccess import DataAccess
import flaskdb.var as v
da = DataAccess(v.HOSTNAME, v.PORT, v.DBNAME, v.USERNAME, v.PASSWORD)

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()
csrf.init_app(apps)

from flask_bootstrap import Bootstrap
bs = Bootstrap(apps)


from flask_easymde import EasyMDE
from flaskext.markdown import Markdown
apps.config["EasyMDE_JS_IIFE"] = True
apps.config["EasyMDE_USE_CDN"] = True
EasyMDE(apps)
Markdown(apps, extensions=["nl2br", "fenced_code"])

from flaskdb.controller.views import app
from flaskdb.controller.auth import auth_module
from flaskdb.controller.memo import memo_module
from flaskdb.controller.share import share_module

apps.register_blueprint(app)
apps.register_blueprint(auth_module)
apps.register_blueprint(memo_module)
apps.register_blueprint(share_module)
