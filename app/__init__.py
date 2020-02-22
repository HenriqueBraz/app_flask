from flask import Flask
import json
from flask_wtf import CSRFProtect
from flask_jwt_extended import JWTManager
import flask_heroku



app = Flask(__name__)

with open('config.json') as f:
    conf = json.load(f)

JWTManager(app)

from .views import usuario_view, auth_view, index_view, empresa_view
from .models import usuario_model

DEBUG = True
app.config['SECRET_KEY'] = conf["SECRET_KEY"]
csrf = CSRFProtect(app)
csrf.init_app(app)
app.register_blueprint(auth_view.bp)
#flask_heroku.settings(locals())




