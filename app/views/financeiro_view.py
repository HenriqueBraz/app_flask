from datetime import datetime
from werkzeug.utils import redirect
from app import app
from flask import render_template, url_for, session, request, flash
from app.forms.finantial_forms import finantial_forms
from app.models.financeiro_model import FinanceiroModel


@app.route('/listar_financeiro', methods=["GET"])
def listar_financeiro():
    db = FinanceiroModel()
    user_id = session['user_id']
    result = db.get_companies(user_id)

    return render_template('/financeiro/listar_clientes.html', result=result)


@app.route('/select_financeiro/<int:id>/<string:nome>', methods=["GET"])
def select_financeiro(id, nome):
    db = FinanceiroModel()
    result = db.get_levyings(id)
    if result:
        return redirect(url_for('listar_cobrancas', id=id, nome=nome))

    return redirect(url_for('incluir_cobranca', id=id, nome=nome))


@app.route('/listar_cobrancas/<int:id>/<string:nome>', methods=["GET"])
def listar_cobrancas(id, nome):
    db = FinanceiroModel()
    result = db.get_levyings(id)
    soma = db.get_levyings_sum(id)
    if soma[0] != None:
        soma = ("%.2f" % soma[0])
    else:
        soma = 0
    return render_template('/financeiro/listar_cobrancas.html', result=result, id=id, nome=nome, soma=soma)


@app.route('/incluir_cobranca/<int:id>/<string:nome>', methods=["GET", "POST"])
def incluir_cobranca(id, nome):
    db = FinanceiroModel()
    form = finantial_forms.FinantialForms()
    if form.validate_on_submit():
        data = request.form['data']
        if data == '':
            flash('Por favor, insira uma data para o campo Dia do Vencimento!')
            return redirect(url_for('editar_cobranca', id=id, nome=nome))

        data = datetime.strptime(data, "%m/%d/%Y")
        servico = request.form['servico']
        valor = request.form['valor']
        tipo_cobranca  = request.form['tipo_cobranca']
        if db.insert_finantal_levying(id, data, servico, valor, tipo_cobranca):
            message = 'Cobrança cadastrada com sucesso!'
            flash(message)
            return redirect(url_for('listar_cobrancas', id=id, nome=nome))

        else:
            message = 'Houve um erro ao inserir a cobrança, contate o administrador do sistema'
            flash(message)

    return render_template('/financeiro/incluir_cobranca.html', form=form, id=id, nome=nome)

@app.route('/editar_cobranca/<int:id>/<string:nome>', methods=["GET", "POST"])
def editar_cobranca(id, nome):
    db = FinanceiroModel()
    result = db.get_levying(id)
    id_cobranca = result[-1]
    data = result[2]
    data = data.strftime("%m/%d/%Y")
    tipo_cobranca = result[5]
    form = finantial_forms.FinantialForms(
        servico=result[3],
        valor=result[4]
    )
    if form.validate_on_submit():
        data = request.form['data']
        if data == '':
            flash('Campo Dia do Vencimento não pode estar vazio, nada foi modificado.')
            return redirect(url_for('editar_cobranca', id=id, nome=nome))

        data = datetime.strptime(data, "%m/%d/%Y")
        servico = request.form['servico']
        valor = request.form['valor']
        tipo_cobranca  = request.form['tipo_cobranca']
        if db.update_finantal_levying(data, servico, valor, tipo_cobranca, id_cobranca):
            message = 'Cobrança editada com sucesso!'
            flash(message)
            return redirect(url_for('listar_cobrancas', id=id, nome=nome))

        else:
            message = 'Houve um erro ao editar a cobrança, contate o administrador do sistema'
            flash(message)

    return render_template('/financeiro/editar_cobranca.html', form=form, id=id, nome=nome, data=data, tipo_cobranca=tipo_cobranca)


@app.route('/inativar_financeiro', methods=["GET"])
def inativar_financeiro():
    return render_template('/financeiro/inativar_financeiro.html')


@app.route('/excluir_cobranca/<int:id>/<string:nome>', methods=["GET", "POST"])
def excluir_cobranca(id, nome):
    db = FinanceiroModel()
    result = db.get_levying(id)
    id_cobranca = result[-1]
    flag = 1
    if request.method == 'POST':
        if request.form['submit_button'] == 'Excluir Cobrança':
            if result:
                if db.update_status_levying(id_cobranca):
                    flash('cobrança excluída com sucesso!')
                    flag = 0
    return render_template('financeiro/excluir_cobranca.html', id=id, result=result, flag=flag, nome=nome)
