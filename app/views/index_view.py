from werkzeug.utils import redirect
from app import app
from app.forms.auth_forms import login_form
from flask import render_template, url_for, session


@app.route("/")
def rotas():
    # return render_template("rotas.html")
    return redirect(url_for('login', flag=1))


@app.route("/favicon.ico")
def favicon():
    return redirect(url_for('login', flag=1))


@app.route('/index', methods=["GET"])
def index():
    form = login_form.LoginForm()
    email = session.get('email')
    return render_template('index/index.html', content_type='application/json', email=email, form=form, pagina='')

@app.route('/ping')
def ping():
    return 'sbphqk, sbphqk, Novo Rumo chamando......'

'''
@app.route('/teste')
def teste():
    return render_template('teste.html')
'''