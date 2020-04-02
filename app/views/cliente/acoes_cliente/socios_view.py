from datetime import datetime
from werkzeug.utils import redirect
from app import app
from flask import render_template, request, flash, url_for
from app.forms.client_forms import partner_structure_forms
from app.models.socios_model import SociosModel


@app.route('/select_socios<int:id>', methods=["GET"])
def select_socios(id):
    db = SociosModel()
    result = db.get_partners(id)
    print(result)
    if result == ():
        return redirect(url_for('cadastrar_socio', id=id))

    else:
        return redirect(url_for('listar_socios', id=id))


@app.route('/listar_socios/<int:id>', methods=["GET"])
def listar_socios(id):
    db = SociosModel()
    result = db.get_partners(id)
    return render_template("cliente/quadro_societario/listar_socios.html", result=result, id_empresa=id )


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

    return render_template("/cliente/quadro_societario/cadastar_socio.html", form=form, id_empresa=id,  pagina='Cadastrar Sócio')


@app.route('/editar_socio<int:id_socio>', methods=["GET", "POST"])
def editar_socio(id_socio):
    db = SociosModel()
    id_empresa = db.get_id_company(id_socio)
    result = db.get_partner(id_socio)
    result11 = result[11]
    result13 = result[13]
    result11 = str(result11).split("-")
    result11 = result11[2] + "/" + result11[1] + "/" + result11[0]
    result13 = str(result13).split("-")
    result13 = result13[2] + "/" + result13[1] + "/" + result13[0]
    form = partner_structure_forms.PartnerForm(
        nome=result[2],
        endereco=result[3],
        bairro=result[4],
        cidade=result[5],
        naturalidade=result[6],
        nacionalidade=result[7],
        estadoCivil=result[8],
        profissao=result[9],
        rg=result[10],
        rgDataExpedicao=datetime.strptime(result11, '%d/%m/%Y').date(),
        cpf=result[12],
        dataNascimento=datetime.strptime(result13, '%d/%m/%Y').date(),
        nomeMae=result[14],
        nomePai=result[15],
        participacaoCapitalSocial=result[16],
        socioAdministrador=result[17],
        proLabore=result[18],
        proLaboreValor=result[19],
        reponsavelReceita=result[20],
        pis=result[21]
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

    return render_template("cliente/quadro_societario/editar_socio.html", form=form, id_empresa=id_empresa[0], pagina='Editar Socio')


@app.route('/excluir_socio<int:id_socio>', methods=["GET", "POST"])
def excluir_socio(id_socio):
    db = SociosModel()
    result = db.select_partner(id_socio)
    print(result)
    flag = 1
    if request.method == 'POST':
        if request.form['submit_button'] == 'Excluir socio':
            if result:
                if db.update_status_partner(result[0]):
                    flash('sócio excluído com sucesso!')
                    flag = 0
    return render_template("cliente/quadro_societario/excluir_socio.html", result=result, flag=flag, id_empresa=result[-1],  pagina='Excluir Socio')
