from flask import redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from . import auth
from ..models import User
from .forms import LoginForm
from .. import Config

@auth.route("/login",methods=["GET","POST"])
def login():
    form=LoginForm()
    error="0"
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            next=request.args.get("next")
            if next is None or not next.startswith("/"):
                next=url_for("main.index")
            return redirect(next)
        error="1"
    return render_template("auth/login.html",form=form,error=error,config=Config)
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))