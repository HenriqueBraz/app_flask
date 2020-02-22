import functools
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from app import app
from app.forms.auth_forms import login_form, register_form
from flask import render_template, request, url_for, flash, session, Blueprint, g
from app.models.model import UsuarioModel

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


@app.route('/login', methods=["GET", "POST"])
def login():
    if session.get('username'):
        print(session.get)
        return redirect(url_for('index'))

    else:
        form = login_form.LoginForm(username=session.get('username'))
        if form.validate_on_submit():
            db = UsuarioModel()
            username = request.form['username']
            password = request.form['password']
            error = None
            result = db.find_all_username(username)
            if result is None:
                error = 'Credenciais inválidas.'
                flash(error)

            elif not check_password_hash(result[2], password):
                error = 'Credenciais inválidas.'
                flash(error)

            if error is None:
                session.clear()
                session['user_id'] = result[0]
                session['group'] = result[9]
                session['username'] = result[1]
                return redirect(url_for('index'))

        return render_template('auth/login.html', content_type='application/json', form=form, pagina='')



@bp.before_app_request
def load_logged_in_user():
    db = UsuarioModel()
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None

    else:
        g.user = db.find_one_id(user_id)



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))

        return view(**kwargs)

    return wrapped_view
