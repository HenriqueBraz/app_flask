import hashlib
import os
from datetime import datetime
from werkzeug.utils import redirect, secure_filename
from app import app, ALLOWED_EXTENSIONS, PATH
from flask import render_template, request, flash, url_for

from app.forms.client_forms import client_form
from app.models.anexos_model import AnexoModel

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/listar_anexos<int:id>', methods=["GET"])
def listar_anexos(id):
    db = AnexoModel()
    result = db.get_anexos(id)
    print(result)
    if len(result) == 0:
        empresa = db.get_company_name(id)
        return redirect(url_for('inserir_anexo', id=id, empresa=empresa[0]))

    else:
        empresa = result[0][-1]

        return render_template("cliente/anexos/listar_anexos.html", result=result, id=id,  empresa=empresa,  pagina='Listar Anexos')


@app.route('/inserir_anexo<int:id><string:empresa>', methods=["GET", "POST"])
def inserir_anexo(id, empresa):
    form = client_form.AnexoForm()
    db = AnexoModel()

    if form.validate_on_submit():

        descricao = request.form['descricao']

        file = []
        if request.files['image1']:
            file.append(request.files['image1'])

        if request.files['image2']:
            file.append(request.files['image2'])

        if request.files['image3']:
            file.append(request.files['image3'])

        anexos = len(file)
        range_anexo = 0
        path = []
        filename = []
        size = []
        md5 = []
        type = []
        flag = ''

        for i in range(anexos):
            if allowed_file(file[i].filename):
                filename.append(secure_filename(file[i].filename))
                file[i].save(os.path.join(app.config['UPLOAD_FOLDER'], filename[i]))
                path.append(PATH + '/' + filename[i])
                size.append(int(os.path.getsize(path[i])))
                md5.append(hashlib.md5(b'filename').hexdigest())
                temp = filename[i].split('.')
                type.append(temp[1])
                flag = 1
                range_anexo += 1

            else:
                flash('O arquivo {} não é um PDF e não foi inserido!'.format(file[i].filename))

        if db.insert_anexo(id, path, filename, descricao, size, type, md5, flag, range_anexo):


            flash('anexo inserido com sucesso!')
            return redirect(url_for('listar_anexos', id=id, form=form))

        else:
           flash('Houve um erro ao inserir u ou mais anexos, contate o administrador do sistema')

    print(form.errors)
    return render_template("cliente/anexos/inserir_anexo.html", id=id, empresa=empresa, form=form, pagina='Inserir Anexo')


@app.route('/excluir_anexo<int:id><int:id_anexo>', methods=["GET", "POST"])
def excluir_anexo(id, id_anexo):
    db = AnexoModel()
    result = db.update_status_anexo(id_anexo)
    if result:
        flash('anexo excluido com sucesso!')

    else:
        flash('Erro ao excluir o anexo, contate o administrador do sistema.')

    return redirect(url_for('listar_anexos', id=id))


@app.route('/baixar_anexo<int:id_anexo><int:id>', methods=["GET", "POST"])
def baixar_anexo(id_anexo, id):

    return('codar a parte de download de anexos!')

