from datetime import datetime
from werkzeug.utils import redirect
from app import app
from flask import render_template, request, url_for, flash
from app.forms.accounting_forms import accounting_form
from app.models.contabilidade_model import ContabilidadeModel


@app.route('/listar_contabilidade<int:id>', methods=["GET"])
def listar_contabilidade(id):
    db = ContabilidadeModel()
    result = db.check_accounting(id)
    if result is None:
        return redirect(url_for('cadastrar_contabilidade', id=id))

    return redirect(url_for('editar_contabilidade', id=id))


@app.route('/cadastrar_contabilidade/<int:id>', methods=["GET", "POST"])
def cadastrar_contabilidade(id):
    form = accounting_form.RegisterFormAccouting()
    if form.validate_on_submit():
        db = ContabilidadeModel()
        contabilidade = request.form['contabilidade']
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        dataEntrada = request.form['dataEntrada']
        dataEntrada = datetime.strptime(dataEntrada, "%d/%m/%Y")
        if db.check_accounting(id) is not None:
            return redirect(url_for('editar_contabilidade', id=id))

        elif db.insert_accounting(id, contabilidade, nome, telefone, email, dataEntrada):
            flash('Contabilidade cadastrada com sucesso!')

        else:
            flash('Houve um erro ao inserir a cliente, contate o administrador do sistema')

    return render_template('cliente/contabilidade/cadastrar_contabilidade.html', form=form, pagina='')


@app.route('/editar_contabilidade/<int:id>', methods=["GET", "POST"])
def editar_contabilidade(id):
    db = ContabilidadeModel()
    result = db.get_accounting(id)
    form = accounting_form.RegisterFormAccouting(
        contabilidade=result[2],
        nome=result[3],
        telefone=result[4],
        email=result[5],
        dataEntrada=result[6]
    )
    if form.validate_on_submit():
        db = ContabilidadeModel()
        contabilidade = request.form['contabilidade']
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        dataEntrada = request.form['dataEntrada']
        dataEntrada = datetime.strptime(dataEntrada, "%d/%m/%Y")
        if db.update_accounting(id, contabilidade, nome, telefone, email, dataEntrada):
            flash('Alterações salvas com sucesso!')
        else:
            flash('Houve um erro ao inserir a cliente, contate o administrador do sistema')

    return render_template('cliente/contabilidade/editar_contabilidade.html', form=form, id_empresa=id, pagina='')


@app.route('/excluir_contabilidade/<int:id>', methods=["GET", "POST"])
def excluir_contabilidade(id):
    db = ContabilidadeModel()
    result = db.get_accounting(id)
    flag = 1
    if request.method == 'POST':
        if request.form['submit_button'] == 'Excluir Contabilidade':
            if result:
                if db.update_status_accounting(result[0]):
                    flash('Contabilidade excluída com sucesso!')
                    flag = 0

    return render_template('cliente/contabilidade/excluir_contabilidade.html',pagina='Excluir Contabilidade Anterior', result=result, flag=flag)
