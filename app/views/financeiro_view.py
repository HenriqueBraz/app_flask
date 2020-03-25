from werkzeug.utils import redirect
from app import app
from app.forms.auth_forms import login_form
from flask import render_template, url_for, session


@app.route('/listar_financeiro', methods=["GET"])
def listar_financeiro():
    return render_template('/financeiro/listar_clientes.html')


@app.route('/cobranca_financeiro', methods=["GET"])
def cobranca_financeiro():
    return render_template('/financeiro/cobranca_financeiro.html')


@app.route('/inativar_financeiro', methods=["GET"])
def inativar_financeiro():
    return render_template('/financeiro/inativar_financeiro.html')
