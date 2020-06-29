from math import ceil
from pygal.style import CleanStyle, Style
from app.models.graficos_model import GraficoModel
from werkzeug.utils import redirect
from app import app
from datetime import datetime
from app.forms.auth_forms import login_form
from flask import render_template, url_for, session, g
import pygal


def real_br_money_mask(my_value):
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',', 'v')
    c = b.replace('.', ',')
    return c.replace('v', '.')


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

    este_mes = db.get_levyings_sum(mes)
    if este_mes[0]:
        este_mes2 = este_mes[0]
        este_mes = real_br_money_mask(este_mes[0])
    else:
        este_mes = '0'
        este_mes2 = 0.0

    if mes != 1:
        mes = str(int(mes) - 1)
        ultimo_mes = db.get_levyings_sum(mes)
        if ultimo_mes[0]:
            ultimo_mes2 = ultimo_mes[0]
            ultimo_mes = real_br_money_mask(ultimo_mes[0])
        else:
            ultimo_mes = '0'
            ultimo_mes2 = 0.0

    else:
        ultimo_mes = db.get_levyings_sum(mes)
        ultimo_mes = real_br_money_mask(ultimo_mes[0])
        ultimo_mes2 = ultimo_mes[0]

    if este_mes2 > ultimo_mes2:
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
                           graph_data2=graph_data2, graph_data3=graph_data3, total_clientes=total_clientes,
                           numero_clientes=numero_clientes,
                           porcentagem=porcentagem, este_mes=este_mes, ultimo_mes=ultimo_mes, flag_index=1,
                           this_month=this_month, last_month=last_month)


@app.route('/ping')
def ping():
    return 'sbphqk, sbphqk, Novo Rumo chamando......'


'''
@app.route('/teste')
def teste():
    return render_template('teste.html')
'''
