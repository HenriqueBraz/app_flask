from datetime import datetime

from app import app
from flask import render_template, request, session
from app.forms.billings_forms import billings_forms
from app.models.faturamento_model import FaturamentoModel


@app.route('/faturamento_individual', methods=["GET", "POST"])
def inserir_faturamento_individual():
    now = datetime.now()
    data = now.strftime('%m')
    form = billings_forms.BillingForm(
        mes=data
    )
    db = FaturamentoModel()
    result = db.get_companies()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if form.validate_on_submit():
        cliente = request.form['cliente']
        mes = request.form['mes']
        valor = session.get('valor')

    return render_template('faturamentos/faturamento_individual.html', form=form)


@app.route('/faturamento_individual_lp', methods=["GET", "POST"])
def inserir_faturamento_coletivo_lp():
    now = datetime.now()
    data = now.strftime('%m')
    data_ano = now.strftime('%Y')
    form = billings_forms.BillingForm(
        mes=data
    )
    db = FaturamentoModel()
    result = db.get_companies_lp()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if form.validate_on_submit():
        cliente = request.form['cliente']
        mes = request.form['mes']
        ano = request.form['ano']

    print(form.errors)
    return render_template('faturamentos/faturamento_individual_lp.html', form=form, valor=data_ano)


@app.route('/faturamento_individual_sn', methods=["GET", "POST"])
def inserir_faturamento_coletivo_sn():
    now = datetime.now()
    data = now.strftime('%m')
    data_ano = now.strftime('%Y')
    form = billings_forms.BillingForm(
        mes = data
    )
    db = FaturamentoModel()
    result = db.get_companies_sn()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if form.validate_on_submit():
        cliente = request.form['cliente']
        mes = request.form['mes']
        ano = request.form['ano']

    print(form.errors)
    return render_template('faturamentos/faturamento_individual_sn.html', form=form, valor=data_ano)


@app.route('/faturamento_individual_r', methods=["GET", "POST"])
def inserir_faturamento_coletivo_r():
    now = datetime.now()
    data = now.strftime('%m')
    data_ano = now.strftime('%Y')
    form = billings_forms.BillingForm(
        mes=data,
    )
    db = FaturamentoModel()
    result = db.get_companies_r()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if form.validate_on_submit():
        cliente = request.form['cliente']
        mes = request.form['mes']
        ano = request.form['ano']

    return render_template('faturamentos/faturamento_individual_r.html', form=form, valor=data_ano)


@app.route('/listar_faturamento_sn', methods=["GET", "POST"])
def listar_faturamento_sn():
    # form = billings_forms.BillingForm()
    db = FaturamentoModel()

    result = [['teste', 'teste', 'teste', 'teste', 'teste', 'teste'],['teste', 'teste', 'teste', 'teste', 'teste', 'teste']]
    print(result)

    return render_template('faturamentos/listar_faturamento_sn.html', resul=result)


@app.route('/listar_faturamento_lp', methods=["GET", "POST"])
def listar_faturamento_lp():
    # form = billings_forms.BillingForm()
    db = FaturamentoModel()

    return render_template('faturamentos/listar_faturamento_lp.html')


@app.route('/listar_faturamento_r', methods=["GET", "POST"])
def listar_faturamento_r():
    # form = billings_forms.BillingForm()
    db = FaturamentoModel()

    return render_template('faturamentos/listar_faturamento_r.html')
