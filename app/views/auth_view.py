import datetime
import functools
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from app import app
from app.forms.auth_forms import login_form, register_form
from flask import render_template, request, url_for, flash, session, Blueprint, g
from app.models.usuario_model import UsuarioModel

bp = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = register_form.RegisterForm()
    if form.validate_on_submit():
        db = UsuarioModel()
        username = request.form['username']
        name = request.form['nome']
        password = request.form['password']
        email = request.form['email']
        error = None
        if db.find_username(username) is not None:
            error = 'Username {} já existe. Por favor escolha outro Username!'.format(username)
            flash(error)
        if error is None:
            print('Estou inserindo no banco')
            db.insert_user(username, generate_password_hash(password), name, email)
            message = 'Cadastro efetuado com sucesso!'
            flash(message)
            return redirect(url_for('register', form=form))

    return render_template('auth/register.html', form=form, pagina=' Cadastro')


@app.route('/login/<int:flag>', methods=["GET", "POST"])
def login(flag):
    if session.get('username'):
        return redirect(url_for('index'))

    else:
        form = login_form.LoginForm(username=session.get('username'))
        form2 = login_form.LoginFormForgotPass()
        now = datetime.datetime.now()
        if request.method == 'POST':
            if request.form['action'] == 'Entrar':
                if form.validate_on_submit():
                    db = UsuarioModel()
                    username = request.form['username']
                    password = request.form['password']
                    error = None
                    result = db.find_all_username(username)
                    if result is None:
                        error = 'Credenciais inválidas!'
                        flash(error)

                    elif not check_password_hash(result[2], password):
                        error = 'Credenciais inválidas!'
                        flash(error)

                    if error is None:
                        print(result)
                        session.clear()
                        session['user_id'] = result[0]
                        session['group'] = result[9]
                        session['username'] = result[1]
                        session['email'] = result[4]
                        session['nome'] = result[3]
                        session['last_active'] = now
                        return redirect(url_for('index'))

            elif request.form['action'] == 'Resetar':
                if form2.validate_on_submit():
                    email = request.form['email']
                    if email:
                        email = request.form['email']
                        flag = 0
                        flash('Instruções de reset de senha enviadas para {} com sucesso!'.format(email))
                        return redirect(url_for('login', flag=flag))
                    else:
                        flag = 1
                        return redirect(url_for('login', flag=flag))
                else:
                    email = request.form['email']
                    flash('Email {} inválido!'.format(email))
                    return redirect(url_for('login', flag=flag))

    return render_template('auth/login.html', content_type='application/json', flag=flag, form=form, form2=form2, pagina='')


@app.before_request
def before_request():
    try:
        g.user = session['username']
        g.id = session['user_id']
        g.email = session['email']
    except Exception:
        pass
    now = datetime.datetime.now()
    try:
        last_active = session['last_active']
        delta = now - last_active
        if delta.seconds > 900: #desloga após 15 min
            session['last_active'] = now
            return redirect(url_for('logout'))
        else:
            session['last_active'] = now
    except:
        pass



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login', flag=1))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login', flag=1))

        return view(**kwargs)

    return wrapped_view
