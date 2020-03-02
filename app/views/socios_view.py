from datetime import datetime

from werkzeug.utils import redirect

from app import app
from flask import render_template, request, flash, url_for
from app.forms.client_forms import partner_structure_forms
from app.models.socios_model import SociosModel


@app.route('/listar_socios<int:id>', methods=["GET"])
def listar_socios(id):
    db = SociosModel()
    result = db.get_partners(id)
    if len(result) == 0:
        return redirect(url_for('cadastrar_socio', id=id))

    return render_template("cliente/quadro_societario/listar_socios.html", result=result, pagina='Lista Socios')


@app.route("/cadastrar_socio<int:id>", methods=["GET", "POST"])
def cadastrar_socio(id):
    form = partner_structure_forms.PartnerForm()
    db = SociosModel()
    if form.validate_on_submit():
        nome = request.form['nome']
        endereco = request.form['endereco']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        naturalidade = request.form['naturalidade']
        nacionalidade = request.form['nacionalidade']
        estadoCivil = request.form['estadoCivil']
        profissao = request.form['profissao']
        rg = request.form['rg']
        rgDataExpedicao = request.form['rgDataExpedicao']
        rgDataExpedicao = datetime.strptime(rgDataExpedicao, "%d/%m/%Y")
        cpf = request.form['cpf']
        dataNascimento = request.form['dataNascimento']
        dataNascimento = datetime.strptime(dataNascimento, "%d/%m/%Y")
        nomeMae = request.form['nomeMae']
        nomePai = request.form['nomePai']
        participacaoCapitalSocial = request.form['participacaoCapitalSocial']
        socioAdministrador = request.form['socioAdministrador']
        proLabore = request.form['proLabore']
        proLaboreValor = request.form['proLaboreValor']
        reponsavelReceita = request.form['reponsavelReceita']
        pis = request.form['pis']

        if db.insert_partner(id, nome, endereco, bairro, cidade, naturalidade, nacionalidade, estadoCivil, profissao,
                             rg,
                             rgDataExpedicao, cpf, dataNascimento, nomeMae, nomePai, participacaoCapitalSocial,
                             socioAdministrador, proLabore, proLaboreValor, reponsavelReceita, pis):

            flash('Sócio cadastrado com sucesso!')
            return redirect(url_for('cadastrar_socio', id=id))

        else:
            flash('Houve um erro ao inserir o sócio, contate o administrador do sistema')

    return render_template("/cliente/quadro_societario/cadastar_socio.html", form=form, pagina='Cadastrar Sócio')


@app.route('/editar_socio<int:id>', methods=["GET", "POST"])
def editar_socio(id):
    db = SociosModel()
    result = db.get_partner(id)
    print(result)
    form = partner_structure_forms.PartnerForm(
        nome=[result[2]],
        endereco=[result[3]],
        bairro=[result[4]],
        cidade=[result[5]],
        naturalidade=[result[6]],
        nacionalidade=[result[7]],
        estadoCivil=[result[8]],
        profissao=[result[9]],
        rg=[result[10]],
        rgDataExpedicao=[result[11]],
        cpf=[result[12]],
        dataNascimento=[result[13]],
        nomeMae=[result[14]],
        nomePai=[result[15]],
        participacaoCapitalSocial=[result[16]],
        socioAdministrador=[result[17]],
        proLabore=[result[18]],
        proLaboreValor=[result[19]],
        reponsavelReceita=[result[20]],
        pis=[result[21]]
    )
    if form.validate_on_submit():
        nome = request.form['nome']
        endereco = request.form['endereco']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        naturalidade = request.form['naturalidade']
        nacionalidade = request.form['nacionalidade']
        estadoCivil = request.form['estadoCivil']
        profissao = request.form['profissao']
        rg = request.form['rg']
        rgDataExpedicao = request.form['rgDataExpedicao']
        rgDataExpedicao = datetime.strptime(rgDataExpedicao, "%d/%m/%Y")
        cpf = request.form['cpf']
        dataNascimento = request.form['dataNascimento']
        dataNascimento = datetime.strptime(dataNascimento, "%d/%m/%Y")
        nomeMae = request.form['nomeMae']
        nomePai = request.form['nomePai']
        participacaoCapitalSocial = request.form['participacaoCapitalSocial']
        socioAdministrador = request.form['socioAdministrador']
        proLabore = request.form['proLabore']
        proLaboreValor = request.form['proLaboreValor']
        reponsavelReceita = request.form['reponsavelReceita']
        pis = request.form['pis']

        if db.insert_partner(id, nome, endereco, bairro, cidade, naturalidade, nacionalidade, estadoCivil, profissao,
                             rg, rgDataExpedicao, cpf, dataNascimento, nomeMae, nomePai, participacaoCapitalSocial,
                             socioAdministrador, proLabore, proLaboreValor, reponsavelReceita, pis):

            flash('Modificações salvas com sucesso!')

            return redirect(url_for('cadastrar_socio', id=id))

        else:
            flash('Houve um erro ao salvar as modificações, contate o administrador do sistema')

    return render_template("cliente/quadro_societario/editar_socio.html", form=form, pagina='Editar Socio')


@app.route('/excluir_socio<int:id>', methods=["GET", "POST"])
def excluir_socio(id):
    pass
    return render_template("cliente/quadro_societario/excluir_socio.html", pagina='Editar Socio')
