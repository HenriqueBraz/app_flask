from datetime import datetime
from werkzeug.utils import redirect
from app import app
from flask import render_template, request, url_for, flash
from app.forms.accounting_forms import accounting_form
from app.models.contabilidade_model import ContabilidadeModel


@app.route('/contabilidade/<int:id>',  methods=["GET", "POST"])
def editar_contabilidade(id):
    db = ContabilidadeModel()
    result = db.get_accounting(id)
    if result is None:
        flash('Esta empresa não possui Contabilidade Anterior cadastrada. Tente outra Ação.')
        return redirect(url_for('listar_clientes'))

    else:
        form = accounting_form.RegisterFormAccouting(
        contabilidade = result[2],
        nome = result[3],
        telefone = result[4],
        email = result[5],
        dataEntrada = result[6]
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

        return render_template('cliente/contabilidade/editar_contabilidade.html', form=form, pagina='')


@app.route('/cadastrar_contabilidade/<int:id>',  methods=["GET", "POST"])
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
        if db.get_accounting(id) is not None:
            flash('Já foi cadastrada uma contabilidade para este cliente. Por favor escolha outro cliente ou tente outra Ação')

        elif db.insert_accounting(id, contabilidade, nome, telefone, email, dataEntrada):
            flash('Contabilidade cadastrada com sucesso!')

        else:
            flash('Houve um erro ao inserir a cliente, contate o administrador do sistema')

    return render_template('cliente/contabilidade/cadastrar_contabilidade.html', form=form, pagina='')


@app.route('/excluir_contabilidade/<int:id>',  methods=["GET", "POST"])
def excluir_contabilidade(id):
    db = ContabilidadeModel()
    result = db.get_accounting(id)
    if result is None:
        flash('Esta empresa não possui Contabilidade Anterior cadastrada. Tente outra Ação.')
        return redirect(url_for('listar_clientes'))
    else:
        flag = 1
        if request.method == 'POST':
            if request.form['submit_button'] == 'Excluir Contabilidade Anterior':
                if result:
                    if db.update_status_accounting(result[0]):
                        flash('cliente excluído com sucesso!')
                        flag = 0

        return render_template('cliente/contabilidade/excluir_contabilidade.html', pagina='Excluir Contabilidade Anterior', result=result, flag=flag)