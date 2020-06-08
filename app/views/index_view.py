from werkzeug.utils import redirect
from app import app
from app.forms.auth_forms import login_form
from flask import render_template, url_for, session
import pygal
import json


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
    with open('/home/henrique/novo-rumo-py/bar.json', 'r') as bar_file:
        data = json.load(bar_file)

    chart = pygal.Pie()
    chart.force_uri_protocol = 'http'
    chart.title = 'Gráfico em Barras'
    chart.add('IE', 19.5)
    chart.add('Firefox', 36.6)
    chart.add('Chrome', 36.3)
    chart.add('Safari', 4.5)
    chart.add('Opera', 2.3)
    graph_data = chart.render_data_uri()

    chart = pygal.Bar()
    chart.force_uri_protocol = 'http'
    chart.title = 'Gráfico em Barras'
    chart.add('IE', 19.5)
    chart.add('Firefox', 36.6)
    chart.add('Chrome', 36.3)
    chart.add('Safari', 4.5)
    chart.add('Opera', 2.3)
    graph_data2 = chart.render_data_uri()

    return render_template('index/index.html', email=email, form=form, pagina='', graph_data=graph_data, graph_data2=graph_data2)


@app.route('/ping')
def ping():
    return 'sbphqk, sbphqk, Novo Rumo chamando......'

'''
@app.route('/teste')
def teste():
    return render_template('teste.html')
'''