from werkzeug.utils import redirect
from app import app
from flask import render_template, request, flash, url_for, session

from app.forms.billings_forms import billings_forms
from app.models.cliente_model import ClienteModel


@app.route('/faturamento_individual', methods=["GET", "POST"])
def inserir_faturamento_individual():
    form = billings_forms.IndividualBillingForm()
    db = ClienteModel()
    result = db.get_companies()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    if form.validate_on_submit():
        cliente = request.form['cliente']
        mes = request.form['mes']
        valor = session.get('valor')


    print(form.errors)
    return render_template('faturamentos/faturamento_individual.html', form=form)