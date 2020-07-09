from app import app, ALLOWED_EXTENSIONS
from flask import render_template, request, flash, url_for, redirect, session
from app.forms.client_forms import client_form
from app.models.cliente_model import ClienteModel
from app.models.usuario_model import UsuarioModel
from app.static.validadores.back_validadores import Validadores


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/cadastrar_cliente', methods=["GET", "POST"])
def cadastrar_cliente():
    user_id = session['user_id']
    user_name = session['nome']
    db = UsuarioModel()
    result = db.get_users()
    form = client_form.ClientForm()
    form.nome_responsavel.choices = [(row[0], row[2]) for row in result]
    form.nome_responsavel.choices.insert(0, (user_id, user_name))
    db = ClienteModel()
    result = db.get_info_nj()
    form.natureza_juridica.choices = [(row[0], (row[1] + ' - ' + row[2])) for row in result]
    result = db.get_info_porte()
    form.porte.choices = [(row[0], row[1]) for row in result]

    if request.method == 'POST':
        nome_responsavel = request.form['nome_responsavel']
        empresa = request.form['empresa']
        natureza_juridica = int(request.form['natureza_juridica'])
        porte = int(request.form['porte'])
        cep = request.form['cep']
        endereco = request.form['endereco']
        numero = request.form['numero']
        complemento = request.form['complemento']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        estado = request.form['estado']
        nome = request.form['nome']
        telefone = request.form['telefone']
        celular = request.form['celular']
        email = request.form['email']
        capital_social = request.form['capital_social']
        nire = request.form['nire']
        cnpj = request.form['cnpj']
        inscricao_estadual = request.form['inscricao_estadual']
        ccm = request.form['ccm']
        tributacao = request.form['tributacao']
        cnae_principal = request.form.getlist('cnae[]')
        dia_faturamento = request.form['dia_faturamento']
        folha_pagamento = request.form['folha_pagamento']
        certificado_digital = request.form['certificado_digital']
        impugnacao = request.form['impugnacao']
        observacoes = request.form['observacoes']
        id_responsavel = int(nome_responsavel)
        validadores = Validadores()
        cnaes = validadores.valida_cnae("https://servicodados.ibge.gov.br/api/v2/cnae/subclasses/", cnae_principal)
        if cnaes[0] == 0:
            flash('Erro de CNAE! O(s) CNAE(s) precisam ser válidos.')
            return render_template('cliente/cadastrar_cliente.html', form=form)


        # TODO codar validação para CNAES do mesmo nome
        # TODO verificar se a validação do mesmo cnpj esta funcionando corretamente
        if db.search_cnpj(cnpj) == 0:
            if validadores.validar_cnpj(cnpj):
                if db.insert_company(nome_responsavel, natureza_juridica, porte, id_responsavel, empresa, endereco,
                                     bairro,
                                     cep, cidade, numero, complemento, estado,
                                     capital_social, nire, cnpj, inscricao_estadual, ccm, str(cnaes[1]),
                                     tributacao, dia_faturamento, folha_pagamento, certificado_digital, impugnacao,
                                     observacoes, nome, telefone, email, celular):

                    flash('Empresa cadastrada com sucesso!')
                    return redirect(url_for('listar_clientes', form=form))
                else:
                    flash('Houve um erro ao inserir a cliente, contate o administrador do sistema')

            else:
                flash('Erro de CNPJ! Entre com um CNPJ válido.')

        else:
            flash('Empresa não cadastrada, CNPJ já existe no sistema!')

    return render_template('cliente/cadastrar_cliente.html', form=form)


@app.route('/listar_clientes', methods=["GET"])
def listar_clientes():
    db = ClienteModel()
    user_id = session['user_id']
    lista_clientes = db.get_companies(user_id)
    return render_template('cliente/listar_clientes.html', result=lista_clientes, pagina='Listar Clientes')


@app.route('/editar_cliente/<int:id>', methods=["GET", "POST"])
def editar_cliente(id):
    db = ClienteModel()
    result_a = db.get_nj_porte_nome(id)
    result = db.find_one_id(id)
    # TODO atualizar no banco
    # TODO arrumar template quando otiver somente 1 cnae, carde esta desalinhado
    cnaes = result[18]
    cnaes = cnaes.replace('"', '')
    cnaes = cnaes.replace("'", "")
    cnaes = cnaes.replace('[', '')
    cnaes = cnaes.replace(']', '')
    cnaes = cnaes.replace(']', '')
    cnaes = cnaes.replace(' ', '')
    cnaes = cnaes.split(',')

    form = client_form.ClientForm(
        nome_responsavel=result_a[2],
        empresa=result[5],
        natureza_juridica=result_a[0],
        porte=result_a[1],
        cep=result[6],
        endereco=result[7],
        numero=result[8],
        complemento=result[9],
        cidade=result[10],
        bairro=result[11],
        estado=result[12],
        capital_social=result[13],
        nire=result[14],
        cnpj=result[15],
        inscricao_estadual=result[16],
        ccm=result[17],
        tributacao=result[19],
        cnaes=cnaes,
        dia_faturamento=result[20],
        folha_pagamento=result[21],
        certificado_digital=result[22],
        impugnacao=result[23],
        observacoes=result[24],
        nome=result[28],
        telefone=result[29],
        email=result[30],
        celular=result[31]
    )
    tamanho = len(cnaes)
    user_id = result[3]
    db = UsuarioModel()
    result = db.get_users()
    form.nome_responsavel.choices = [(row[0], row[2]) for row in result]
    form.nome_responsavel.choices.insert(0, (user_id, result_a[2]))

    db = ClienteModel()
    result = db.get_info_nj()
    form.natureza_juridica.choices = [(row[0], (row[1] + ' - ' + row[2])) for row in result]
    form.natureza_juridica.choices.insert(0, (1, result_a[0]))
    result = db.get_info_porte()
    form.porte.choices = [(row[0], row[1]) for row in result]
    form.porte.choices.insert(0, (1, result_a[1]))

    if request.method == 'POST':
        nome_responsavel = request.form['nome_responsavel']
        empresa = request.form['empresa']
        natureza_juridica = request.form['natureza_juridica']
        porte = request.form['porte']
        cep = request.form['cep']
        endereco = request.form['endereco']
        numero = request.form['numero']
        complemento = request.form['complemento']
        cidade = request.form['cidade']
        bairro = request.form['bairro']
        estado = request.form['estado']
        capital_social = request.form['capital_social']
        nire = request.form['nire']
        cnpj = request.form['cnpj']
        inscricao_estadual = request.form['inscricao_estadual']
        ccm = request.form['ccm']
        tributacao = request.form['tributacao']
        cnae_principal = request.form.getlist('cnae[]')
        dia_faturamento = request.form['dia_faturamento']
        folha_pagamento = request.form['folha_pagamento']
        certificado_digital = request.form['certificado_digital']
        impugnacao = request.form['impugnacao']
        observacoes = request.form['observacoes']
        id_responsavel = nome_responsavel
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        celular = request.form['celular']
        validadores = Validadores()
        cnae = validadores.valida_cnae("https://servicodados.ibge.gov.br/api/v2/cnae/subclasses/", cnae_principal)
        if cnae == 1:
            flash('Erro de CNAE Secundário! Entre com um CNAE Secundário válido.')
            return redirect(url_for('editar_cliente', id=id))

        elif cnae == 2:
            flash('Erro de CNAE Primário! Entre com um CNAE Primário válido.')
            return redirect(url_for('editar_cliente', id=id))

        if validadores.validar_cnpj(cnpj):
            if db.update_company(empresa, natureza_juridica, porte, cep, endereco, numero, complemento, cidade, bairro,
                                 estado, capital_social, nire,
                                 cnpj, inscricao_estadual, ccm, tributacao, cnae_principal, cnae_secundaria,
                                 dia_faturamento, folha_pagamento, certificado_digital, impugnacao, observacoes,
                                 id_responsavel, id,
                                 nome, email, telefone, celular):

                flash('Alterações salvas com sucesso!')

            else:
                flash('Erro ao realizar as alterações, contate o administrador do sistema.')
        else:
            flash('Erro de CNPJ! Entre com um CNPJ válido.')

    return render_template('cliente/editar_cliente.html', form=form, cnaes=cnaes, tamanho=tamanho)


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
