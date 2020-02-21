from app import app
from app.forms.auth_forms import login_form
from flask import render_template


@app.route('/index', methods=["GET"])
def index():
    form = login_form.LoginForm()
    return render_template('index/index.html', content_type='application/json', form=form, pagina='')




