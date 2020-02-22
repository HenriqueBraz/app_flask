from werkzeug.utils import redirect

from app import app
from flask import render_template, request, session, flash, url_for
from app.forms.company_forms import register_company_form
from app.models.empresa_model import EmpresaModel


@app.route('/cadastrar_empresa', methods=["GET", "POST"])
def cadastrar_empresa():
    form = register_company_form.ClientRegisterForm()
    if form.validate_on_submit():
        db = EmpresaModel()
        empresa = request.form['empresa']
        natureza_juridica = request.form['natureza_juridica']
        porte = request.form['porte']
        endereco = request.form['endereco']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        estado = request.form['estado']
        capital_social = request.form['capital_social']
        nire = request.form['nire']
        cnpj = request.form['cnpj']
        inscricao_estadual = request.form['inscricao_estadual']
        ccm = request.form['ccm']
        tributacao = request.form['tributacao']
        cnae_principal = request.form['cnae_principal']
        cnae_secundaria = request.form['cnae_secundaria']
        dia_faturamento = request.form['dia_faturamento']
        folha_pagamento = request.form['folha_pagamento']
        certificado_digital = request.form['certificado_digital']
        observacoes = request.form['observacoes']
        id_responsavel = session.get('user_id')
        if db.insert_empresa(natureza_juridica, porte, id_responsavel, empresa, endereco, bairro, cidade, estado,
                             capital_social, nire, cnpj, inscricao_estadual, ccm, cnae_principal, cnae_secundaria,
                             tributacao, dia_faturamento, folha_pagamento, certificado_digital, observacoes):
            message = 'Empresa cadastrada com sucesso!'
            flash(message)
            return redirect(url_for('cadastrar_empresa', form=form))

        else:
            flash('Houve um erro ao inserir a empresa, contate o administrador do sistema')

    return render_template('empresa/cadastrar_empresa.html', form=form, pagina='')


@app.route('/listar_empresas', methods=["GET"])
def listar_empresas():
    form = register_company_form.ClientListForm()
    return render_template('empresa/listar_empresa.html', content_type='application/json', form=form,
                           pagina='Listar Cliente')
