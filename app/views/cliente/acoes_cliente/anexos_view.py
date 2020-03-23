import hashlib
import os
from werkzeug.utils import redirect, secure_filename
from app import app, ALLOWED_EXTENSIONS, PATH, MAX_IMAGE_FILESIZE
from flask import render_template, request, flash, url_for, send_from_directory
from app.forms.client_forms import client_form
from app.models.anexos_model import AnexoModel


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_size(filesize):
    return int(filesize) <= MAX_IMAGE_FILESIZE


@app.route('/listar_anexos<int:id>', methods=["GET"])
def listar_anexos(id):
    db = AnexoModel()
    result = db.get_anexos(id)
    if len(result) == 0:
        empresa = db.get_company_name(id)
        return redirect(url_for('inserir_anexo', id=id, empresa=empresa[0]))

    else:
        empresa = result[0][-1]

        return render_template("cliente/anexos/listar_anexos.html", result=result, id=id, empresa=empresa,
                               pagina='Listar Anexos')


@app.route('/inserir_anexo/<int:id>/<string:empresa>', methods=["GET", "POST"])
def inserir_anexo(id, empresa):
    form = client_form.AnexoForm()
    db = AnexoModel()

    if form.validate_on_submit():

        files = request.files.getlist('files[]')
        titulo = request.form['titulo']
        descricao = request.form.getlist('descricao[]')
        print(files)
        print(descricao)

        for i in range(len(files)):
            if files[i].filename == "":
                flash('O arquivo {} não possui um nome válido, não foi inserido'.format(files[i].filename))

            else:
                if allowed_file(files[i].filename):
                    filename = secure_filename(files[i].filename)
                    files[i].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    path = PATH + '/' + filename
                    size = int(os.path.getsize(path))
                    if allowed_file_size(size):
                        md5 = hashlib.md5(b'filename').hexdigest()
                        temp = filename.split('.')
                        typee = temp[1]
                        if db.insert_anexo(id, titulo, path, filename, descricao[i], size, typee, md5):
                            flash('anexo {} inserido com sucesso!'.format(files[i].filename))

                        else:
                            flash('Erro ao inserir o arquivo {}, contate o administrador do sistema.'.format(
                                files[i].filename))
                    else:
                        flash('O arquivo {} excedeu o tamanho máximo permitido e não foi inserido.'.format(
                            files[i].filename))
                else:
                    flash(
                        'O arquivo {} não é um PDF não foi inserido!'.format(
                            files[i].filename))


        return redirect(url_for('listar_anexos', id=id, form=form))

    return render_template("cliente/anexos/inserir_anexo.html", id=id, empresa=empresa, form=form,
                           pagina='Inserir Anexo')


@app.route('/excluir_anexo/<int:id>/<int:id_anexo>/', methods=["GET", "POST"])
def excluir_anexo(id, id_anexo):
    db = AnexoModel()
    result = db.update_status_anexo(id_anexo)
    if result:
        flash('anexo excluido com sucesso!')

    else:
        flash('Erro ao excluir o anexo, contate o administrador do sistema.')

    return redirect(url_for('listar_anexos', id=id))


@app.route('/baixar_anexo/<int:id_anexo>', methods=["GET", "POST"])
def baixar_anexo(id_anexo):
    db = AnexoModel()
    result = db.get_anexo(id_anexo)
    path = result[0]
    nome = result[1]
    return send_from_directory('uploads', nome, as_attachment=True)
