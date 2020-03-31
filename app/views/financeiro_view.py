from werkzeug.utils import redirect
from app import app
from app.forms.auth_forms import login_form
from flask import render_template, url_for, session

from app.models.financeiro_model import FinanceiroModel


@app.route('/listar_financeiro', methods=["GET"])
def listar_financeiro():
    db = FinanceiroModel()
    result = db.get_companies()
    print(result)

    return render_template('/financeiro/listar_clientes.html', result=result)


@app.route('/cobranca_financeiro', methods=["GET"])
def cobranca_financeiro():
    return render_template('/financeiro/cobranca_financeiro.html')


@app.route('/inativar_financeiro', methods=["GET"])
def inativar_financeiro():
    return render_template('/financeiro/inativar_financeiro.html')
