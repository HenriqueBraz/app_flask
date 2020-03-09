from datetime import datetime
from werkzeug.utils import redirect
from app import app
from flask import render_template, request, flash, url_for, session
from app.forms.occurrences_forms import occurrences_forms
from app.models.cliente_model import ClienteModel
from app.models.ocorrencia_model import OcorrenciaModel


@app.route('/listar_ocorrencias_sn', methods=["GET"])
def listar_ocorrencias_sn():
    db = OcorrenciaModel()
    lista_ocorrencias = db.get_occurrences_sn()
    flag = 1
    return render_template('ocorrencias/listar_ocorrencias_sn.html', flag=flag, result=lista_ocorrencias,
                           pagina='Listar Ocorrencias')


@app.route('/listar_ocorrencias_lp', methods=["GET"])
def listar_ocorrencias_lp():
    db = OcorrenciaModel()
    lista_ocorrencias = db.get_occurrences_lp()
    flag = 0
    return render_template('ocorrencias/listar_ocorrencias_lp.html', flag=flag, result=lista_ocorrencias,
                           pagina='Listar Ocorrencias')


@app.route('/ver_ocorrencia<int:id><int:flag>', methods=["GET", "POST"])
def ver_ocorrencia(id, flag):
    db = OcorrenciaModel()
    result = db.get_occurrence(id)
    print(flag)
    return render_template('ocorrencias/ver_ocorrencia.html', result=result, flag=flag, pagina='Ver Ocorrencia')


@app.route('/incluir_ocorrencia', methods=["GET", "POST"])
def incluir_ocorrencia():
    form = occurrences_forms.OccurrencesRegisterForm()
    db = ClienteModel()
    result = db.get_companies()
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


@app.route('/alterar_ocorrencia<int:id><int:flag>', methods=["GET", "POST"])
def alterar_ocorrencia(id, flag):
    db = OcorrenciaModel()
    result = db.get_occurrence_edit(id)
    id_ocorrencia = result[4]
    form = occurrences_forms.OccurrencesEditForm(
        cliente=result[3],
        observacoes=result[2],
        responsavel=result[1],
    )
    if form.validate_on_submit():
        id_cliente = result[0]
        responsavel = session.get('username')
        observacoes = request.form['observacoes']

        if db.update_occurrence(id_cliente, responsavel, observacoes, id_ocorrencia):
            flash('Alterações salvas com sucesso!')

        else:
            flash('Houve um erro ao realizar a alteração, contate o administrador do sistema')

    return render_template('ocorrencias/alterar_ocorrencia.html', flag=flag, form=form, pagina='Alterar Ocorrencia')


@app.route('/excluir_ocorrencia<int:id><int:flag>', methods=["GET", "POST"])
def excluir_ocorrencia(id, flag):
    db = OcorrenciaModel()
    result = db.get_occurrence(id)
    flag1 = 1
    if request.method == 'POST':
        if request.form['submit_button'] == 'Excluir ocorrencia':
            if result:
                if db.update_status_partner(result[7]):
                    flash('ocorrência excluída com sucesso!')
                    flag1 = 0
    return render_template('ocorrencias/excluir_ocorrencia.html', result=result, flag=flag, flag1=flag1,
                           pagina='Excluir Ocorrencia')
