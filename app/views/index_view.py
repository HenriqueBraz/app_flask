from math import ceil

from pygal.style import CleanStyle, Style

from app.models.financeiro_model import FinanceiroModel
from app.models.graficos_model import GraficoModel
from werkzeug.utils import redirect
from app import app
from datetime import datetime
from app.forms.auth_forms import login_form
from flask import render_template, url_for, session, g
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
    user_id = session.get('user_id')
    form = login_form.LoginForm()
    db = GraficoModel()
    now = datetime.now()
    ano = now.strftime('%Y')
    mes = now.strftime('%m')

    este_mes = "150,00"
    ultimo_mes = "100,00"
    if este_mes > ultimo_mes:
        this_month = "monthchart"
        last_month = "lastmonthchart"
    else:
        this_month = "lastmonthchart"
        last_month = "monthchart"



    result = db.get_numero_empresas(user_id)
    numero_clientes = result[0]
    if not numero_clientes:
        numero_clientes = "0"

    total_clientes = result[1]
    porcentagem = int(ceil((numero_clientes * 100) / total_clientes))
    porcentagem = porcentagem - (porcentagem % 10)

    result = db.get_tributacao('SIMPLES NACIONAL', 'PRESUMIDO', 'REAL', user_id)
    chart = pygal.Pie(style=CleanStyle)
    chart.force_uri_protocol = 'http'
    chart.title = 'Faturamento por Cliente'
    chart.add('Simples Nacional', result[0])
    chart.add('Lucro Presumido', result[1])
    chart.add('Lucro Real', result[2])
    graph_data = chart.render_data_uri()

    result = db.get_ocorrencias(user_id)
    custom_style = Style(
        colors=('#9e0808', '#041e70', '#04753c'))
    chart = pygal.Bar(style=custom_style)
    chart.force_uri_protocol = 'http'
    chart.title = 'Ocorrências em Aberto / Fechado / Andamento'
    chart.add('Aberto', result[0])
    chart.add('Andamento', result[2])
    chart.add('Fechado', result[1])
    graph_data2 = chart.render_data_uri()

    result1 = db.get_cobrancas('Continuo')
    result2 = db.get_cobrancas('Nao_Continuo')
    chart = pygal.Bar(style=CleanStyle)
    chart.force_uri_protocol = 'http'
    chart.title = 'Cobranças, ano ' + str(ano) + ':'
    chart.x_labels = ('Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez')
    chart.add('Contínuo', result1)
    chart.add('Não Contínuo', result2)
    graph_data3 = chart.render_data_uri()

    return render_template('index/index.html', form=form, graph_data=graph_data,
                           graph_data2=graph_data2, graph_data3=graph_data3, total_clientes=total_clientes, numero_clientes=numero_clientes,
                           porcentagem=porcentagem, este_mes=este_mes, ultimo_mes=ultimo_mes, flag_index=1)


@app.route('/ping')
def ping():
    return 'sbphqk, sbphqk, Novo Rumo chamando......'


'''
@app.route('/teste')
def teste():
    return render_template('teste.html')
'''
