import os
import hashlib
from werkzeug.utils import secure_filename
from app import app, ALLOWED_EXTENSIONS, PATH
from flask import render_template, request, session, flash, url_for, redirect
from app.forms.client_forms import client_form, access_forms
from app.models.acesso_model import AcessoModel
from app.models.cliente_model import ClienteModel
from app.models.usuario_model import UsuarioModel


@app.route('/listar_acesso<int:id>', methods=["GET", "POST"])
def listar_acessos(id):
    db = AcessoModel()
    result = db.check_accounting(id)
    print(result)
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
            return redirect(url_for('editar_acesso', id=id))

        elif db.insert_accounting(id, codigoAcessoSimples, AcessoECAC, usernamePF, senhaPF, senhaPrefeitura, senhaINSS,responsavelReceita):
            flash('Acesso cadastrado com sucesso!')

        else:
            flash('Houve um erro ao inserir o acesso, contate o administrador do sistema')

    return render_template('cliente/acesso/cadastar_acesso.html', form=form, pagina='Cadastrar Acesso')


@app.route('/editar_acesso/<int:id>', methods=["GET", "POST"])
def editar_acesso(id):
    db = AcessoModel()
    result = db.get_accounting(id)
    print(result)
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
        if db.update_accounting(id, codigoAcessoSimples, AcessoECAC, usernamePF, senhaPF, senhaPrefeitura, senhaINSS,responsavelReceita):
            flash('Alterações salvas com sucesso!')
        else:
            flash('Houve um erro ao inserir a cliente, contate o administrador do sistema')

    return render_template('cliente/acesso/editar_acesso.html', form=form, pagina='Editar Acesso')
