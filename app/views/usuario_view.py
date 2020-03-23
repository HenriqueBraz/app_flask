# -*- coding: utf-8 -*-
from flask_paginate import get_page_parameter, Pagination
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from app.forms.user_forms import edit_forms
from app.models.usuario_model import UsuarioModel
from flask import render_template, session, request, flash



@app.route("/listar_usuarios", methods=["GET"])
def usuarios():
    db = UsuarioModel()
    users = db.get_users()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(users), search=search, record_name='users', per_page=1,  css_framework='bootstrap4')
    group = session.get('group')
    if group == "Administrador":
        return render_template('usuario/listar_usuarios.html', result=users, group=group, pagina='Listar Usuários', pagination=pagination)
    else:
        user_id = session.get('user_id')
        user = db.get_user(user_id)
        print(user)
        return render_template('usuario/listar_usuarios.html', result=user, group=group, pagina='Listar Usuários', pagination=pagination)


@app.route("/edita_usuario/<int:id>", methods=["GET", "POST"])
def edita_usuario(id):
    db = UsuarioModel()
    result = db.find_one_id(id)
    if session.get('group') == "Usuario":
        form = edit_forms.EditFormUser(
            username=result[0],
            nome=result[1],
            email=result[2],
            password=result[3],
            confirm=result[3],
            group=result[4]
        )
        if form.validate_on_submit():
            username = request.form['username']
            name = request.form['nome']
            email = request.form['email']
            password = request.form['password']
            group = request.form['group']
            error = None
            if error is None:
                password = generate_password_hash(password)
                if check_password_hash(result[3], password):
                    if db.update_user(username, name, email, result[3], group, id):
                        flash('Alterações salvas com sucesso!')

                elif db.update_user(username, name, email, password, group, id):
                    flash('Alterações salvas com sucesso!')

                else:
                    flash('Erro ao realizar as alterações, contate o administrador do sistema.')
    else:
        form = edit_forms.EditFormAdmin(
            username=result[0],
            nome=result[1],
            email=result[2],
            password=result[3],
            confirm=result[3],
            group=result[4]
        )
        if form.validate_on_submit():
            username = request.form['username']
            name = request.form['nome']
            email = request.form['email']
            password = request.form['password']
            group = request.form['group']

            error = None
            result = db.find_all_username(username)
            if result is None:
                error = 'Esse Username já existe! Por favor escolha outro!.'
                flash(error)

            if error is None:
                password = generate_password_hash(password)
                if check_password_hash(result[3], password):
                    if db.update_user(username, name, email, result[3], group, id):
                        flash('Alterações salvas com sucesso!')

                elif db.update_user(username, name, email, password, group, id):
                    flash('Alterações salvas com sucesso!')

                else:
                    flash('Erro ao realizar as alterações, contate o administrador do sistema.')

    return render_template('usuario/editar_usuario.html', form=form, pagina='Editar Usuário')


@app.route("/exclui_usuario/<int:id>", methods=["GET", "POST"])
def exclui_usuario(id):
    db = UsuarioModel()
    result = db.get_user(id)
    flag = 1
    if request.method == 'POST':
        if request.form['submit_button'] == 'Excluir usuário':
            if result:
                if db.update_status_user(result[0]):
                    flash('usuário excluído com sucesso!')
                    flag = 0

    return render_template('usuario/excluir_usuario.html', pagina='Excluir Usuário', result=result, flag=flag)
