import hashlib
import os
from werkzeug.utils import redirect, secure_filename
from app import app, ALLOWED_EXTENSIONS, PATH
from flask import render_template, request, flash, url_for, send_from_directory

from app.forms.client_forms import client_form
from app.models.anexos_model import AnexoModel

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/listar_anexos<int:id>', methods=["GET"])
def listar_anexos(id):
    db = AnexoModel()
    result = db.get_anexos(id)
    if len(result) == 0:
        empresa = db.get_company_name(id)
        return redirect(url_for('inserir_anexo', id=id, empresa=empresa[0]))

    else:
        empresa = result[0][-1]

        return render_template("cliente/anexos/listar_anexos.html", result=result, id=id,  empresa=empresa,  pagina='Listar Anexos')


@app.route('/inserir_anexo/<int:id>/<string:empresa>', methods=["GET", "POST"])
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

        if request.files['image4']:
            file.append(request.files['image4'])

        if request.files['image5']:
            file.append(request.files['image5'])

        anexos = len(file)
        path = []
        filename = []
        size = []
        md5 = []
        type = []
        print(anexos)

        for i in range(anexos):
            if allowed_file(file[i].filename):
                filename.append(secure_filename(file[i].filename))
                file[i].save(os.path.join(app.config['UPLOAD_FOLDER'], filename[i]))
                path.append(PATH + '/' + filename[i])
                size.append(int(os.path.getsize(path[i])))
                md5.append(hashlib.md5(b'filename').hexdigest())
                temp = filename[i].split('.')
                type.append(temp[1])

                if  db.insert_anexo(id, path[i], filename[i], descricao, size[i], type[i], md5[i]):
                    flash('anexo {} inserido com sucesso!'.format(file[i].filename))

                else:
                    flash('Erro ao inserir o arquivo {}, contate o administrador do sistema.'.format(file[i].filename))


            else:
                flash('O arquivo {} não é um PDF e não foi inserido!'.format(file[i].filename))

        return redirect(url_for('listar_anexos', id=id, form=form))

    return render_template("cliente/anexos/inserir_anexo.html", id=id, empresa=empresa, form=form, pagina='Inserir Anexo')


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





