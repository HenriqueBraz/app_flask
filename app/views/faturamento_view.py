from datetime import datetime
from werkzeug.utils import redirect
from app import app
from flask import render_template, request, flash, url_for, session
from app.forms.billings_forms import billings_forms
from app.models.faturamento_model import FaturamentoModel


@app.route('/faturamento_individual_sn', methods=["GET", "POST"])
def inserir_faturamento_coletivo_sn():
    db = FaturamentoModel()
    user_id = session.get('user_id')
    tipo = 'sn'
    now = datetime.now()
    data_mes = now.strftime('%m')
    data_ano = now.strftime('%Y')
    data_mes_ano = now.strftime('%m/%Y')
    form = billings_forms.BillingForm(
        mes=data_mes
    )
    result = db.get_companies_sn()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if request.method == 'POST':
        letra = request.form['letra']
        mes = request.form['mes']
        if request.form['ano']:
            ano = request.form['ano']
        else:
            ano = data_ano

        if mes != data_mes and ano == data_ano:
            data_mes_ano = mes + '/' + data_ano
            result = db.get_companies(letra, user_id, tipo)
            if result:
                result2 = []
                for i in range(len(result)):
                    if result[i][1] == data_mes_ano or result[i][1] == None:
                        result2.append(result[i])

                return render_template('faturamentos/listar_faturamento_sn.html', result=result2, tipo=tipo,
                                       data_mes_ano=data_mes_ano)
            else:
                flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))

        elif mes == data_mes and ano != data_ano:
            data_mes_ano = data_mes + '/' + ano
            result = db.get_companies(letra, user_id, tipo)
            if result:
                result2 = []
                for i in range(len(result)):
                    if result[i][1] == data_mes_ano or result[i][1] == None:
                        result2.append(result[i])

                return render_template('faturamentos/listar_faturamento_sn.html', result=result2, tipo=tipo,
                                       data_mes_ano=data_mes_ano)
            else:
                flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))

        else:
            result = db.get_companies(letra, user_id, tipo)
            if result:
                return render_template('faturamentos/listar_faturamento_sn.html', result=result, tipo=tipo,
                                       data_mes_ano=data_mes_ano)
            else:
                flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))

    return render_template('faturamentos/faturamento_individual_sn.html', form=form, valor=data_ano)


@app.route('/faturamento_individual_lp', methods=["GET", "POST"])
def inserir_faturamento_coletivo_lp():
    db = FaturamentoModel()
    user_id = session.get('user_id')
    tipo = 'lp'
    now = datetime.now()
    data_mes = now.strftime('%m')
    data_ano = now.strftime('%Y')
    data_mes_ano = now.strftime('%m/%Y')
    form = billings_forms.BillingForm(
        mes=data_mes
    )
    result = db.get_companies_sn()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if request.method == 'POST':
        letra = request.form['letra']
        mes = request.form['mes']
        if request.form['ano']:
            ano = request.form['ano']
        else:
            ano = data_ano

        if mes != data_mes and ano == data_ano:
            data_mes_ano = mes + '/' + data_ano
            result = db.get_companies(letra, user_id, tipo)
            if result:
                result2 = []
                for i in range(len(result)):
                    if result[i][1] == data_mes_ano or result[i][1] == None:
                        result2.append(result[i])

                return render_template('faturamentos/listar_faturamento_lp.html', result=result2, tipo=tipo,
                                       data_mes_ano=data_mes_ano)
            else:
                flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))

        elif mes == data_mes and ano != data_ano:
            data_mes_ano = data_mes + '/' + ano
            result = db.get_companies(letra, user_id, tipo)
            if result:
                result2 = []
                for i in range(len(result)):
                    if result[i][1] == data_mes_ano or result[i][1] == None:
                        result2.append(result[i])

                return render_template('faturamentos/listar_faturamento_lp.html', result=result2, tipo=tipo,
                                       data_mes_ano=data_mes_ano)
            else:
                flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))

        else:
            result = db.get_companies(letra, user_id, tipo)
            if result:
                return render_template('faturamentos/listar_faturamento_lp.html', result=result, tipo=tipo,
                                       data_mes_ano=data_mes_ano)
            else:
                flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))
    return render_template('faturamentos/faturamento_individual_lp.html', form=form, valor=data_ano)


@app.route('/faturamento_individual_r', methods=["GET", "POST"])
def inserir_faturamento_coletivo_r():
    db = FaturamentoModel()
    user_id = session.get('user_id')
    tipo = 'r'
    now = datetime.now()
    data_mes = now.strftime('%m')
    data_ano = now.strftime('%Y')
    data_mes_ano = now.strftime('%m/%Y')
    form = billings_forms.BillingForm(
        mes=data_mes
    )
    result = db.get_companies_sn()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if request.method == 'POST':
        letra = request.form['letra']
        mes = request.form['mes']
        if request.form['ano']:
            ano = request.form['ano']
        else:
            ano = data_ano

        if mes != data_mes and ano == data_ano:
            data_mes_ano = mes + '/' + data_ano
            result = db.get_companies(letra, user_id, tipo)
            if result:
                result2 = []
                for i in range(len(result)):
                    if result[i][1] == data_mes_ano or result[i][1] == None:
                        result2.append(result[i])

                return render_template('faturamentos/listar_faturamento_r.html', result=result2, tipo=tipo,
                                       data_mes_ano=data_mes_ano)
            else:
                flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))

        elif mes == data_mes and ano != data_ano:
            data_mes_ano = data_mes + '/' + ano
            result = db.get_companies(letra, user_id, tipo)
            if result:
                result2 = []
                for i in range(len(result)):
                    if result[i][1] == data_mes_ano or result[i][1] == None:
                        result2.append(result[i])

                return render_template('faturamentos/listar_faturamento_r.html', result=result2, tipo=tipo,
                                       data_mes_ano=data_mes_ano)
            else:
                flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))

        else:
            result = db.get_companies(letra, user_id, tipo)
            if result:
                return render_template('faturamentos/listar_faturamento_r.html', result=result, tipo=tipo,
                                       data_mes_ano=data_mes_ano)
            else:
                flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))

    return render_template('faturamentos/faturamento_individual_r.html', form=form, valor=data_ano)
