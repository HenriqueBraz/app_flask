from datetime import datetime
from werkzeug.utils import redirect
from app import app
from flask import render_template, request, flash, url_for, session
from app.forms.billings_forms import billings_forms
from app.models.faturamento_model import FaturamentoModel


@app.route('/faturamento_individual_sn', methods=["GET", "POST"])
def faturamento_individual_sn():
    db = FaturamentoModel()
    tipo = 'sn'
    now = datetime.now()
    data_mes = now.strftime('%m')
    data_ano = now.strftime('%Y')
    form = billings_forms.BillingForm(
        mes=data_mes,
        ano = data_ano
    )
    result = db.get_companies_sn()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if request.method == 'POST':
        letra = request.form['letra']
        mes = request.form['mes']
        if request.form['ano']:
            ano = data_ano
        else:
            ano = data_ano
        return redirect(url_for('listar_faturamento', letra = letra, mes = mes, ano=ano, tipo = tipo))

    return render_template('faturamentos/faturamento_individual_sn.html', form=form, valor=data_ano)


@app.route('/faturamento_individual_lp', methods=["GET", "POST"])
def faturamento_individual_lp():
    db = FaturamentoModel()
    tipo = 'lp'
    now = datetime.now()
    data_mes = now.strftime('%m')
    data_ano = now.strftime('%Y')
    form = billings_forms.BillingForm(
        mes=data_mes
    )
    result = db.get_companies_sn()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if request.method == 'POST':
        letra = request.form['letra']
        mes = request.form['mes']
        if request.form['ano']:
            ano = data_ano
        else:
            ano = data_ano

        return redirect(url_for('listar_faturamento', letra=letra, mes=mes, ano=ano, tipo=tipo))

    return render_template('faturamentos/faturamento_individual_lp.html', form=form, valor=data_ano)


@app.route('/faturamento_individual_r', methods=["GET", "POST"])
def faturamento_individual_r():
    db = FaturamentoModel()
    tipo = 'r'
    now = datetime.now()
    data_mes = now.strftime('%m')
    data_ano = now.strftime('%Y')
    form = billings_forms.BillingForm(
        mes=data_mes
    )
    result = db.get_companies_sn()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if request.method == 'POST':
        letra = request.form['letra']
        mes = request.form['mes']
        if request.form['ano']:
            ano = data_ano
        else:
            ano = data_ano

        return redirect(url_for('listar_faturamento', letra=letra, mes=mes, ano=ano, tipo=tipo))

    return render_template('faturamentos/faturamento_individual_r.html', form=form, valor=data_ano)



@app.route('/listar_faturamento/<string:letra>/<string:mes>/<string:ano>/<string:tipo>', methods=["GET", "POST"])
def listar_faturamento(letra, mes, ano, tipo):
    db = FaturamentoModel()
    user_id = session.get('user_id')
    now = datetime.now()
    data_mes = now.strftime('%m')
    data_ano = now.strftime('%Y')
    data_mes_ano = now.strftime('%m/%Y')
    if mes != data_mes and ano == data_ano:
        data_mes_ano = mes + '/' + data_ano
        result = db.get_companies(letra, user_id, tipo)
        if result:
            result2 = []
            for i in range(len(result)):
                if result[i][1] == data_mes_ano or result[i][1] == None:
                    result2.append(result[i])

            if request.method == 'POST':
                flash('codar post')

            return render_template('faturamentos/listar_faturamento.html', result=result2, tipo=tipo,
                                   data_mes_ano=data_mes_ano)
        else:
            flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))
            if tipo == 'sn':
                return redirect(url_for('faturamento_individual_sn'))
            elif tipo == 'lp':
                return redirect(url_for('faturamento_individual_lp'))
            elif tipo == 'r':
                return redirect(url_for('faturamento_individual_r'))

    elif mes == data_mes and ano != data_ano:
        data_mes_ano = data_mes + '/' + ano
        result = db.get_companies(letra, user_id, tipo)
        if result:
            result2 = []
            for i in range(len(result)):
                if result[i][1] == data_mes_ano or result[i][1] == None:
                    result2.append(result[i])

            if request.method == 'POST':
                flash('codar post')

            return render_template('faturamentos/listar_faturamento.html', result=result2, tipo=tipo,
                                   data_mes_ano=data_mes_ano)
        else:
            flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))
            if tipo == 'sn':
                return redirect(url_for('faturamento_individual_sn'))
            elif tipo == 'lp':
                return redirect(url_for('faturamento_individual_lp'))
            elif tipo == 'r':
                return redirect(url_for('faturamento_individual_r')) #pass

    else:
        result = db.get_companies(letra, user_id, tipo)
        if result:
            if request.method == 'POST':
                flash('codar post')

            return render_template('faturamentos/listar_faturamento.html', result=result, tipo=tipo,
                                   data_mes_ano=data_mes_ano)
        else:
            flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))
            if tipo == 'sn':
                return redirect(url_for('faturamento_individual_sn'))
            elif tipo == 'lp':
                return redirect(url_for('faturamento_individual_lp'))
            elif tipo == 'r':
                return redirect(url_for('faturamento_individual_r'))





