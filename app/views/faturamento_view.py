from werkzeug.utils import redirect
from app import app
from flask import render_template, request, flash, url_for, session
from app.forms.billings_forms import billings_forms
from app.models.cliente_model import ClienteModel
from app.models.faturamento_model import FaturamentoModel


@app.route('/faturamento_individual', methods=["GET", "POST"])
def inserir_faturamento_individual():
    form = billings_forms.IndividualBillingForm()
    db = FaturamentoModel()
    result = db.get_companies()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if form.validate_on_submit():
        cliente = request.form['cliente']
        mes = request.form['mes']
        valor = session.get('valor')


    print(form.errors)
    return render_template('faturamentos/faturamento_individual.html', form=form)


@app.route('/faturamento_individual_lp', methods=["GET", "POST"])
def inserir_faturamento_coletivo_lp():
    form = billings_forms.IndividualBillingForm()
    db = FaturamentoModel()
    result = db.get_companies_lp()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if form.validate_on_submit():
        cliente = request.form['cliente']
        mes = request.form['mes']
        valor = session.get('valor')


    print(form.errors)
    return render_template('faturamentos/faturamento_individual_lp.html', form=form)

@app.route('/faturamento_individual_sn', methods=["GET", "POST"])
def inserir_faturamento_coletivo_sn():
    form = billings_forms.IndividualBillingForm()
    db = FaturamentoModel()
    result = db.get_companies_sn()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if form.validate_on_submit():
        cliente = request.form['cliente']
        mes = request.form['mes']
        valor = session.get('valor')


    print(form.errors)
    return render_template('faturamentos/faturamento_individual_sn.html', form=form)

@app.route('/faturamento_individual_r', methods=["GET", "POST"])
def inserir_faturamento_coletivo_r():
    form = billings_forms.IndividualBillingForm()
    db = FaturamentoModel()
    result = db.get_companies_r()
    print(result)
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if form.validate_on_submit():
        cliente = request.form['cliente']
        mes = request.form['mes']
        valor = session.get('valor')


    print(form.errors)
    return render_template('faturamentos/faturamento_individual_r.html', form=form)