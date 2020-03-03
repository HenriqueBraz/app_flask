import os
from flask import Flask
import json
from flask_wtf import CSRFProtect
from flask_jwt_extended import JWTManager
import flask_heroku

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
ALLOWED_EXTENSIONS = set(['pdf', 'jpeg', 'png'])


app = Flask(__name__)



with open('config.json') as f:
    conf = json.load(f)

JWTManager(app)

from .views import usuario_view, auth_view, index_view, cliente_view, contabilidade_view, socios_view
from .models import usuario_model, cliente_model, contabilidade_model, socios_model

DEBUG = True
app.config['SECRET_KEY'] = conf["SECRET_KEY"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
csrf = CSRFProtect(app)
csrf.init_app(app)
app.register_blueprint(auth_view.bp)
#flask_heroku.settings(locals())




