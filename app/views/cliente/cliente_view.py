import os
import hashlib
from werkzeug.utils import secure_filename
from app import app, ALLOWED_EXTENSIONS, PATH
from flask import render_template, request, session, flash, url_for, redirect
from app.forms.client_forms import client_form
from app.models.cliente_model import ClienteModel
from app.models.usuario_model import UsuarioModel


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/cadastrar_cliente', methods=["GET", "POST"])
def cadastrar_cliente():
    db = UsuarioModel()
    result = db.get_users()
    form = client_form.ClientForm()
    form.nome_responsavel.choices = [(row[0], row[2]) for row in result]
    db = ClienteModel()
    result = db.get_info_nj()
    form.natureza_juridica.choices = [(row[0], (row[1] + ' - ' + row[2])) for row in result]
    result = db.get_info_porte()
    form.porte.choices = [(row[0], row[1]) for row in result]

    if form.validate_on_submit():
        nome_responsavel = request.form['nome_responsavel']
        empresa = request.form['empresa']
        natureza_juridica = request.form['natureza_juridica']
        porte = request.form['porte']
        endereco = request.form['endereco']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        estado = request.form['estado']
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
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
        id_responsavel = nome_responsavel


        if db.insert_company(nome_responsavel, natureza_juridica, porte, id_responsavel, empresa, endereco, bairro,
                             cidade, estado,
                             capital_social, nire, cnpj, inscricao_estadual, ccm, cnae_principal, cnae_secundaria,
                             tributacao, dia_faturamento, folha_pagamento, certificado_digital, observacoes, nome,
                             telefone, email):


            flash('Empresa cadastrada com sucesso!')
            return redirect(url_for('cadastrar_cliente', form=form))

        else:
           flash('Houve um erro ao inserir a cliente, contate o administrador do sistema')

    return render_template('cliente/cadastrar_cliente.html', form=form, pagina='')


@app.route('/listar_clientes', methods=["GET"])
def listar_clientes():
    db = ClienteModel()
    lista_clientes = db.get_companies()
    return render_template('cliente/listar_clientes.html', result=lista_clientes, pagina='Listar Clientes')


@app.route('/editar_cliente/<int:id>', methods=["GET", "POST"])
def editar_cliente(id):
    db = ClienteModel()
    result_a = db.get_nj_porte_nome(id)
    result = db.find_one_id(id)
    form = client_form.ClientForm(
        nome_responsavel=result_a[2],
        empresa=result[5],
        natureza_juridica=result_a[0],
        porte=result_a[1],
        endereco=result[6],
        cidade=result[8],
        bairro=result[7],
        estado=result[9],
        capital_social=result[10],
        nire=result[11],
        cnpj=result[12],
        inscricao_estadual=result[13],
        ccm=result[14],
        tributacao=result[17],
        cnae_principal=result[15],
        cnae_secundaria=result[16],
        dia_faturamento=result[18],
        folha_pagamento=result[19],
        certificado_digital=result[20],
        observacoes=result[21],
        nome=result[25],
        telefone=result[26],
        email=result[27]
    )

    db = UsuarioModel()
    result = db.get_users()
    form.nome_responsavel.choices = [(row[0], row[2]) for row in result]
    form.nome_responsavel.choices.insert(0, (1, result_a[2]))

    db = ClienteModel()
    result = db.get_info_nj()
    form.natureza_juridica.choices = [(row[0], (row[1] + ' - ' + row[2])) for row in result]
    form.natureza_juridica.choices.insert(0, (1, result_a[0]))
    result = db.get_info_porte()
    form.porte.choices = [(row[0], row[1]) for row in result]
    form.porte.choices.insert(0, (1, result_a[1]))

    if form.validate_on_submit():
        nome_responsavel = request.form['nome_responsavel']
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
        id_responsavel = nome_responsavel
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        if db.update_company(empresa, natureza_juridica, porte, endereco, cidade, bairro, estado, capital_social, nire,
                             cnpj, inscricao_estadual, ccm, tributacao, cnae_principal, cnae_secundaria,
                             dia_faturamento, folha_pagamento, certificado_digital, observacoes, id_responsavel, id,
                             nome, telefone, email):
            flash('Alterações salvas com sucesso!')

        else:
            flash('Erro ao realizar as alterações, contate o administrador do sistema.')

    return render_template('cliente/editar_cliente.html', form=form, pagina='')


@app.route('/excluir_cliente/<int:id>"', methods=["GET", "POST"])
def excluir_cliente(id):
    db = ClienteModel()
    result = db.get_company(id)
    flag = 1
    if request.method == 'POST':
        if request.form['submit_button'] == 'Excluir empresa':
            if result:
                if db.update_status_company(result[0]):
                    flash('cliente excluído com sucesso!')
                    flag = 0

    return render_template('cliente/excluir_cliente.html', pagina='Excluir Cliente', result=result, flag=flag)
