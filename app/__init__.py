import os
from flask import Flask
import json
from flask_wtf import CSRFProtect
from flask_jwt_extended import JWTManager
from flask_babel import Babel
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'uploads')
ALLOWED_EXTENSIONS = set(['pdf'])
MAX_IMAGE_FILESIZE = 0.5 * 1024 * 1024
BABEL_DEFAULT_LOCALE = 'pt'

app = Flask(__name__, static_url_path='')

with open('config.json') as f:
    conf = json.load(f)

JWTManager(app)

from .views import usuario_view, auth_view, index_view, faturamento_view
from app.views.cliente.acoes_cliente import contabilidade_view, socios_view, acesso_view, anexos_view
from app.views.cliente import cliente_view
from app.views import ocorrencia_view, financeiro_view
from .models import usuario_model, cliente_model, contabilidade_model, socios_model, acesso_model, faturamento_model, anexos_model, financeiro_model

DEBUG = True
app.config['SECRET_KEY'] = conf["SECRET_KEY"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True
csrf = CSRFProtect(app)
csrf.init_app(app)
app.register_blueprint(auth_view.bp)
babel = Babel(app)
bootstrap = Bootstrap(app)



