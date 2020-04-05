from datetime import datetime
from werkzeug.utils import redirect
from app import app
from flask import render_template, url_for, session, request, flash
from app.forms.finantial_forms import finantial_forms
from app.models.financeiro_model import FinanceiroModel


@app.route('/listar_financeiro', methods=["GET"])
def listar_financeiro():
    db = FinanceiroModel()
    user_id = session['user_id']
    result = db.get_companies(user_id)

    return render_template('/financeiro/listar_clientes.html', result=result)


@app.route('/select_financeiro/<int:id>/<string:nome>', methods=["GET"])
def select_financeiro(id, nome):
    db = FinanceiroModel()
    result = db.get_levyings(id)
    if result:
        return redirect(url_for('listar_cobrancas', id=id, nome=nome))

    return redirect(url_for('incluir_cobranca', id=id, nome=nome))


@app.route('/listar_cobrancas/<int:id>/<string:nome>', methods=["GET"])
def listar_cobrancas(id, nome):
    db = FinanceiroModel()
    result = db.get_levyings(id)
    print(result)
    return render_template('/financeiro/listar_cobrancas.html', result=result, id=id, nome=nome)


@app.route('/incluir_cobranca/<int:id>/<string:nome>', methods=["GET", "POST"])
def incluir_cobranca(id, nome):
    db = FinanceiroModel()
    form = finantial_forms.FinantialForms()
    if form.validate_on_submit():
        data = request.form['data']
        data = datetime.strptime(data, "%m/%d/%Y")
        servico = request.form['servico']
        valor = request.form['valor']
        tipo_cobranca  = request.form['tipo_cobranca']
        if db.insert_finantal_levying(id, data, servico, valor, tipo_cobranca):
            message = 'Cobrança cadastrada com sucesso!'
            flash(message)
            return redirect(url_for('listar_cobrancas', id=id, nome='nome'))

        else:
            message = 'Houve um erro ao inserir a cobrança, contate o administrador do sistema'
            flash(message)

    print(form.errors)
    print('erros de form')
    return render_template('/financeiro/incluir_cobranca.html', form=form, id=id, nome=nome)


@app.route('/inativar_financeiro', methods=["GET"])
def inativar_financeiro():
    return render_template('/financeiro/inativar_financeiro.html')
