from werkzeug.utils import redirect
from app import app
from flask import render_template, request, flash, url_for, session
from app.forms.occurrences_forms import occurrences_forms
from app.models.cliente_model import ClienteModel
from app.models.ocorrencia_model import OcorrenciaModel



@app.route('/listar_ocorrencias_lp', methods=["GET"])
def listar_ocorrencias_lp():
    db = OcorrenciaModel()
    lista_ocorrencias = db.get_occurrences_lp()
    flag = 0
    return render_template('ocorrencias/listar_ocorrencias_lp.html', flag=flag, result=lista_ocorrencias,
                           pagina='Listar Ocorrencias')


@app.route('/listar_ocorrencias_sn', methods=["GET"])
def listar_ocorrencias_sn():
    db = OcorrenciaModel()
    lista_ocorrencias = db.get_occurrences_sn()
    print(lista_ocorrencias)
    flag = 1
    return render_template('ocorrencias/listar_ocorrencias_sn.html', flag=flag, result=lista_ocorrencias,
                           pagina='Listar Ocorrencias')


@app.route('/listar_ocorrencias_r', methods=["GET"])
def listar_ocorrencias_r():
    db = OcorrenciaModel()
    lista_ocorrencias = db.get_occurrences_r()
    flag = 2
    return render_template('ocorrencias/listar_ocorrencias_r.html', flag=flag, result=lista_ocorrencias,
                           pagina='Listar Ocorrencias')


@app.route('/ver_ocorrencia<int:id>/<int:id_ocorrencia>/<int:flag>', methods=["GET", "POST"])
def ver_ocorrencia(id, id_ocorrencia, flag):
    db = OcorrenciaModel()
    print(id_ocorrencia)
    result = db.get_occurrence_edit(id_ocorrencia)
    form = occurrences_forms.OccurrencesViewForm(
        cliente=result[3],
        observacoes=result[2],
        responsavel=result[1],
        status=result[5],
    )
    return render_template('ocorrencias/ver_ocorrencia.html', flag=flag, form=form, pagina='Alterar Ocorrencia')


@app.route('/incluir_ocorrencia', methods=["GET", "POST"])
def incluir_ocorrencia():
    form = occurrences_forms.OccurrencesRegisterForm()
    db = ClienteModel()
    user_id = session['user_id']
    result = db.get_companies(user_id)
    form.cliente.choices = [(row[0], row[1]) for row in result]
    db = OcorrenciaModel()
    if form.validate_on_submit():
        id_cliente = request.form['cliente']
        observacoes = request.form['observacoes']
        responsavel = session.get('username')

        if db.insert_occurrence(id_cliente, responsavel, observacoes):

            message = 'Ocorrencia cadastrada com sucesso!'
            flash(message)
            return redirect(url_for('incluir_ocorrencia', form=form, pagina='Incluir Ocorrencia'))

        else:
            message = 'Houve um erro ao inserir a cliente, contate o administrador do sistema'
            flash(message)

    return render_template('ocorrencias/incluir_ocorrencia.html', form=form, pagina='Incluir Ocorrencia')


@app.route('/alterar_ocorrencia<int:id>/<int:id_ocorrencia>/<int:flag>', methods=["GET", "POST"])
def alterar_ocorrencia(id, id_ocorrencia, flag):
    db = OcorrenciaModel()
    result = db.get_occurrence_edit(id_ocorrencia)
    form = occurrences_forms.OccurrencesEditForm(
        cliente=result[3],
        observacoes=result[2],
        responsavel=result[1],
        status=result[5]
    )
    if form.validate_on_submit():
        id_cliente = result[0]
        responsavel = session.get('username')
        observacoes = request.form['observacoes']
        status = request.form['status']

        if db.update_occurrence(id_cliente, responsavel, observacoes, id_ocorrencia, status):
            flash('Alterações salvas com sucesso!')

        else:
            flash('Houve um erro ao realizar a alteração, contate o administrador do sistema')

    return render_template('ocorrencias/alterar_ocorrencia.html', flag=flag, form=form, pagina='Alterar Ocorrencia')


@app.route('/excluir_ocorrencia<int:id>/<int:id_ocorrencia>,<int:flag>', methods=["GET", "POST"])
def excluir_ocorrencia(id, id_ocorrencia, flag):
    db = OcorrenciaModel()
    result = db.get_occurrence(id_ocorrencia)
    flag1 = 1
    if request.method == 'POST':
        if request.form['submit_button'] == 'Excluir ocorrencia':
            if result:
                if db.update_status_partner(result[7]):
                    flash('ocorrência excluída com sucesso!')
                    flag1 = 0
    return render_template('ocorrencias/excluir_ocorrencia.html', result=result, flag=flag, flag1=flag1,
                           pagina='Excluir Ocorrencia')
