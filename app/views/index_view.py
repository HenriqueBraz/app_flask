from app.models.graficos_model import GraficoModel
from werkzeug.utils import redirect
from app import app
from datetime import datetime
from app.forms.auth_forms import login_form
from flask import render_template, url_for, session
import pygal


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
    db = GraficoModel()
    now = datetime.now()
    ano = now.strftime('%Y')

    result = db.get_tributacao('SIMPLES NACIONAL', 'PRESUMIDO', 'REAL')
    chart = pygal.Pie()
    chart.force_uri_protocol = 'http'
    chart.title = 'Faturamento por Cliente'
    chart.add('Simples Nacional', result[0])
    chart.add('Lucro Presumido', result[1])
    chart.add('Lucro Real', result[2])
    graph_data = chart.render_data_uri()

    result = db.get_ocorrencias()
    chart = pygal.Bar()
    chart.force_uri_protocol = 'http'
    chart.title = 'Ocorrências em Aberto / Fechado'
    chart.add('Aberto', result[0])
    chart.add('Fechado', result[1])
    graph_data2 = chart.render_data_uri()

    result1 = db.get_cobrancas('Continuo')
    result2 = db.get_cobrancas('Nao_Continuo')
    print(result1)
    print(result2)
    chart = pygal.Line()
    chart.title = 'Cobranças, ano ' + str(ano) + ':'
    chart.x_labels = ('Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez')
    chart.add('Contínuo', result1)
    chart.add('Não Contínuo', result2)
    graph_data3 = chart.render_data_uri()

    return render_template('index/index.html', email=email, form=form, pagina='', graph_data=graph_data,
                           graph_data2=graph_data2, graph_data3=graph_data3)


@app.route('/ping')
def ping():
    return 'sbphqk, sbphqk, Novo Rumo chamando......'


'''
@app.route('/teste')
def teste():
    return render_template('teste.html')
'''
