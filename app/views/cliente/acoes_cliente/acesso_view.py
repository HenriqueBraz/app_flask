from app import app
from flask import render_template, request, flash, url_for, redirect
from app.forms.client_forms import access_forms
from app.models.acesso_model import AcessoModel



@app.route('/listar_acesso<int:id>', methods=["GET", "POST"])
def listar_acessos(id):
    db = AcessoModel()
    result = db.check_accounting(id)
    if result is None:
        return redirect(url_for('cadastrar_acesso', id=id))

    return redirect(url_for('editar_acesso', id=id))


@app.route('/cadastrar_acesso/<int:id>', methods=["GET", "POST"])
def cadastrar_acesso(id):
    form = access_forms.AccessForm()
    db = AcessoModel()
    if form.validate_on_submit():
        codigoAcessoSimples = request.form['codigoAcessoSimples']
        AcessoECAC = request.form['AcessoECAC']
        usernamePF = request.form['usernamePF']
        senhaPF = request.form['senhaPF']
        senhaPrefeitura = request.form['senhaPrefeitura']
        senhaINSS = request.form['senhaINSS']
        responsavelReceita = request.form['responsavelReceita']
        if db.check_accounting(id) is not None:
            return redirect(url_for('editar_acesso', id_empresa=id))

        elif db.insert_accounting(id, codigoAcessoSimples, AcessoECAC, usernamePF, senhaPF, senhaPrefeitura, senhaINSS,
                                  responsavelReceita):
            flash('Acesso cadastrado com sucesso!')

        else:
            flash('Houve um erro ao inserir o acesso, contate o administrador do sistema')

    return render_template('cliente/acesso/cadastar_acesso.html', form=form, pagina='Cadastrar Acesso')


@app.route('/editar_acesso/<int:id>', methods=["GET", "POST"])
def editar_acesso(id):
    db = AcessoModel()
    result = db.get_accounting(id)
    tributacao = result[-1]
    if tributacao == 'SIMPLES NACIONAL':
        tributacao = 1

    form = access_forms.AccessForm(
        id_empresa=result[1],
        codigoAcessoSimples=result[2],
        AcessoECAC=result[3],
        usernamePF=result[4],
        senhaPF=result[5],
        senhaPrefeitura=result[6],
        senhaINSS=result[7],
        responsavelReceita=result[8],
    )
    if form.validate_on_submit():
        codigoAcessoSimples = request.form['codigoAcessoSimples']
        AcessoECAC = request.form['AcessoECAC']
        usernamePF = request.form['usernamePF']
        senhaPF = request.form['senhaPF']
        senhaPrefeitura = request.form['senhaPrefeitura']
        senhaINSS = request.form['senhaINSS']
        responsavelReceita = request.form['responsavelReceita']
        if db.update_accounting(id, codigoAcessoSimples, AcessoECAC, usernamePF, senhaPF, senhaPrefeitura, senhaINSS,
                                responsavelReceita):
            flash('Alterações salvas com sucesso!')
        else:
            flash('Houve um erro ao inserir a cliente, contate o administrador do sistema')

    return render_template('cliente/acesso/editar_acesso.html', form=form, id_empresa=id, tributacao=tributacao, pagina='Editar Acesso')


@app.route('/excluir_acesso/<int:id>', methods=["GET", "POST"])
def excluir_acesso(id):
    db = AcessoModel()
    result = db.get_company(id)
    flag = 1
    if request.method == 'POST':
        if request.form['submit_button'] == 'Excluir Acesso':
            if result:
                if db.update_status_acesso(result[0]):
                    flash('Acesso excluído com sucesso!')
                    flag = 0
    return render_template('cliente/acesso/excluir_acesso.html', result=result, flag=flag, id_empresa=id,  pagina='Excluir Acesso')





