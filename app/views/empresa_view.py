from app import app
from flask import render_template, request
from app.forms.client_forms import client_form
from app.models.model import UsuarioModel


@app.route('/cadastrar_cliente', methods=["GET", "POST"])
def cadastrar_cliente():
    form = client_form.ClientRegisterForm()
    if form.validate_on_submit():
        db = UsuarioModel()
        empresa = request.form['empresa']
        natureza_juridica = request.form[' natureza_juridica']
        porte = request.form['porte']
        endereço = request.form['endereço']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        estado = request.form['estado']
        capital_social = request.form['capital_social']
        nire = request.form['nire']
        cnpj = request.form['cnpj']
        inscrição_estadual = request.form['inscrição_estadual']
        ccm = request.form['ccm']
        tributacao = request.form['tributacao']
        cnae_principal = request.form['cnae_principal']
        cnae_secundaria = request.form['cnae_secundaria']
        dia_faturamento = request.form['dia_faturamento']
        folha_pagamento = request.form['folha_pagamento']
        certificado_digital = request.form['certificado_digital ']
        observacoes = request.form['observacoes']



    return render_template('empresa/cadastrar_empresa.html', form=form, pagina='')


@app.route('/listar_clientes', methods=["GET"])
def listar_clientes():
    form = client_form.ClientListForm()
    return render_template('empresa/listar_empresa.html', content_type='application/json', form=form,
                           pagina='Listar Cliente')
