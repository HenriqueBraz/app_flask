from datetime import datetime
from werkzeug.utils import redirect
from app import app
from flask import render_template, request, flash, url_for
from app.forms.occurrences_forms import occurrences_forms
from app.models.cliente_model import ClienteModel
from app.models.ocorrencia_model import OcorrenciaModel


@app.route('/incluir_ocorrencia', methods=["GET", "POST"])
def incluir_ocorrencia():
    form = occurrences_forms.OccurrencesRegisterForm()
    db = ClienteModel()
    result = db.get_companies()
    form.cliente.choices = [(row[0], row[1]) for row in result]
    id = form.cliente.choices.row[0]
    print(id)

    db = OcorrenciaModel()
    if form.validate_on_submit():
        cliente = request.form['cliente']
        observacoes = request.fomr['observacoes']

    if db.insert_ocorrencia(cliente, observacoes):

        message = 'Ocorrencia cadastrada com sucesso!'
        flash(message)
        return redirect(url_for('incluir_ocorrencia', form=form))

    else:
        message = 'Houve um erro ao inserir a cliente, contate o administrador do sistema'
        flash(message)


    return render_template('ocorrencias/incluir_ocorrencia.html', form=form, pagina='Incluir Ocorrencia')
