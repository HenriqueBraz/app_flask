from datetime import datetime
from werkzeug.utils import redirect
from app import app
from flask import render_template, url_for, session, request, flash
from app.forms.finantial_forms import finantial_forms
from app.models.financeiro_model import FinanceiroModel


def real_br_money_mask(my_value):
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',', 'v')
    c = b.replace('.', ',')
    return c.replace('v', '.')


@app.route('/selecionar_clientes', methods=["GET", "POST"])
def selecionar_clientes():
    form = finantial_forms.FinantialForms()
    if request.method == 'POST':
        letra = request.form['letra']
        return redirect(url_for('listar_financeiro', letra=letra))

    return render_template('/financeiro/selecionar_clientes.html', form=form)


@app.route('/listar_financeiro/<string:letra>', methods=["GET", "POST"])
def listar_financeiro(letra):
    db = FinanceiroModel()
    user_id = session['user_id']
    result = db.get_companies(user_id, letra)
    if result:
        return render_template('/financeiro/listar_clientes.html', result=result, letra=letra)
    else:
        flash('Não existem empresas cadastradas que comecem com a letra {}'.format(letra))
        return redirect(url_for('selecionar_clientes'))


@app.route('/select_financeiro/<int:id>/<string:nome>/<string:letra>', methods=["GET", "POST"])
def select_financeiro(id, nome, letra):
    db = FinanceiroModel()
    now = datetime.now()
    mes = now.strftime('%m')
    ano = now.strftime('%Y')
    result = db.get_levyings(id, mes, ano)
    if result:
        return redirect(url_for('listar_cobrancas', id=id, nome=nome, letra=letra))

    return redirect(url_for('incluir_cobranca', id=id, nome=nome, letra=letra))


@app.route('/listar_cobrancas/<int:id>/<string:nome>/<string:letra>', methods=["GET", "POST"])
def listar_cobrancas(id, nome, letra):
    db = FinanceiroModel()
    now = datetime.now()
    data = now.strftime('%m')
    ano = now.strftime('%Y')
    mes = data
    form = finantial_forms.FinantialForms(
        mes=data
    )
    if request.method == 'POST':
        mes = request.form['mes']

    result = db.get_levyings(id, mes, ano)
    soma1 = db.get_levyings_sum(id, mes, ano)
    soma2 = []
    for i in range(len(soma1)):
        if soma1[i] is None:
            soma2.append(0.0)
        else:
            soma2.append(soma1[i])

    soma2 = soma2[0] + soma2[1]
    soma = real_br_money_mask(soma2)
    return render_template('/financeiro/listar_cobrancas.html', result=result, form=form, id=id, nome=nome, soma=soma,
                           ano=ano, mes=mes, letra=letra)


@app.route('/incluir_cobranca/<int:id>/<string:nome>/<string:letra>', methods=["GET", "POST"])
def incluir_cobranca(id, nome, letra):
    servico, data, valor, tipo_cobranca = None, None, None, None
    flag = 0
    db = FinanceiroModel()
    form = finantial_forms.FinantialForms()
    if request.method == 'POST':
        if request.form['valor']:
            valor = request.form['valor']
            valor = valor.replace('.', '')
            valor = valor.replace(',', '.')
            flag += 1

        if request.form['tipo_cobranca']:
            tipo_cobranca = request.form['tipo_cobranca']
            flag += 1

        if request.form['data']:
            data = request.form['data']
            data = datetime.strptime(data, '%d/%m/%Y').date()
            flag += 1

        if request.form['servico']:
            servico = request.form['servico']
            flag += 1

        if flag == 4:
            if tipo_cobranca == 'Continuo':
                mes = data.strftime('%m')
                ano = data.strftime('%Y')
                dia = data.strftime('%d')
                for i in range(int(mes), 13):
                    data2 = ano + '-' + str(i) + '-' + dia
                    data2 = datetime.strptime(data2, '%Y-%m-%d').date()
                    if db.insert_finantal_levying(id, data2, servico, valor, tipo_cobranca):
                        flag = True

                    else:
                        flag = False

                if flag:
                    flash('Cobrança(s) cadastrada(s) com sucesso!')
                    return redirect(url_for('listar_cobrancas', id=id, nome=nome, letra=letra))
                else:
                    flash('Houve um erro ao inserir a(a) cobrança(s), contate o administrador do sistema')
                    return redirect(url_for('listar_cobrancas', id=id, nome=nome, letra=letra))


            else:
                if db.insert_finantal_levying(id, data, servico, valor, tipo_cobranca):
                    flash('Cobrança cadastrada com sucesso!')
                    return redirect(url_for('listar_cobrancas', id=id, nome=nome, letra=letra))

                else:
                    flash('Houve um erro ao inserir a cobrança, contate o administrador do sistema')


        else:
            flash('Escolha uma data!')

    return render_template('/financeiro/incluir_cobranca.html', form=form, id=id, nome=nome, letra=letra)


@app.route('/editar_cobranca/<int:id>/<string:nome>/<id_cobranca>/<string:letra>', methods=["GET", "POST"])
def editar_cobranca(id, nome, id_cobranca, letra):
    flag = 0
    db = FinanceiroModel()
    result = db.get_levying(id_cobranca)
    valor = str(result[4])
    valor_input = valor.replace('.', '')
    valor_input = valor_input.replace(',', '.')
    tipo_cobranca = result[5]
    id_cobranca = result[6]
    data_place_holder = result[2]
    data = datetime.strptime(data_place_holder, '%d/%m/%Y').date()
    servico = result[3]
    form = finantial_forms.FinantialForms(
        servico=result[3],
    )
    if request.method == 'POST':

        if (request.form['valor']):
            valor_input = request.form['valor']
            valor_input = valor_input.replace('.', '')
            valor_input = valor_input.replace(',', '.')
            flag = 1

        if (request.form['tipo_cobranca'] != tipo_cobranca):
            tipo_cobranca = request.form['tipo_cobranca']
            flag = 1

        if (request.form['data']):
            data = request.form['data']
            data = datetime.strptime(data, '%d/%m/%Y').date()
            flag = 1

        if (request.form['servico'] != servico):
            servico = request.form['servico']
            flag = 1

        if flag == 1:
            if db.update_finantal_levying(data, servico, valor_input, tipo_cobranca, id_cobranca):
                flash('Cobrança editada com sucesso!')
                return redirect(url_for('listar_cobrancas', id=id, nome=nome, letra=letra))

            else:
                message = 'Houve um erro ao editar a cobrança, contate o administrador do sistema'
                flash(message)
        else:
            flash('Nenhum campo foi modificado, cobrança não alterada!')
            return redirect(url_for('editar_cobranca', id=id, nome=nome, id_cobranca=id_cobranca, letra=letra))

    return render_template('/financeiro/editar_cobranca.html', form=form, id=id, nome=nome,
                           data_place_holder=data_place_holder, tipo_cobranca=tipo_cobranca, valor=valor, letra=letra)


@app.route('/inativar_financeiro', methods=["GET"])
def inativar_financeiro():
    return render_template('/financeiro/inativar_financeiro.html')


@app.route('/excluir_cobranca/<int:id>/<string:nome>/<id_cobranca>', methods=["GET", "POST"])
def excluir_cobranca(id, nome, id_cobranca):
    db = FinanceiroModel()
    result = db.get_levying(id_cobranca)
    flag = 1
    if request.method == 'POST':
        if request.form['submit_button'] == 'Excluir Cobrança':
            if result:
                if db.update_status_levying(id_cobranca):
                    flash('cobrança excluída com sucesso!')
                    flag = 0
    return render_template('financeiro/excluir_cobranca.html', id=id, result=result, flag=flag, nome=nome)
