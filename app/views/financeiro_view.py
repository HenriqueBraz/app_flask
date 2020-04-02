from werkzeug.utils import redirect
from app import app
from flask import render_template, url_for, session
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
    result = db.finantials_companie(id)
    if result:
        return redirect(url_for('listar_cobrancas', id=id, nome=nome))

    return redirect(url_for('incluir_cobranca', id=id, nome=nome))


@app.route('/listar_cobrancas/<int:id>/<string:nome>', methods=["GET"])
def listar_cobrancas(id, nome):
    db = FinanceiroModel()
    result = db.get_companies(id)
    return render_template('/financeiro/listar_cobrancas.html', result=result, id=id, nome=nome)


@app.route('/incluir_cobranca/<int:id>/<string:nome>', methods=["GET", "POST"])
def incluir_cobranca(id, nome):
    form = finantial_forms.FinantialForm()
    return render_template('/financeiro/incluir_cobranca.html', form=form, id=id, nome=nome)


@app.route('/inativar_financeiro', methods=["GET"])
def inativar_financeiro():
    return render_template('/financeiro/inativar_financeiro.html')
