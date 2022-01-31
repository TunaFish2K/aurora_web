from flask import render_template,abort, request, url_for, redirect
from . import main
from .forms import *
from flask_login import current_user, login_required, login_user
from ..models import User
from .. import db,Config
import psutil

error=""

@main.route('/')
@login_required
def index():
    global error
    error=""
    mem=psutil.virtual_memory()
    max = float(mem.total) / 1024 / 1024
    used = float(mem.used) / 1024 / 1024
    free = float(mem.free) / 1024 / 1024
    mems=[int(max),int(used),int(free)]
    return render_template("index.html",user=current_user._get_current_object(),config=Config,mems=mems)

@main.route('/user/')
@login_required
def user():
    global error
    error=""
    if not current_user._get_current_object().username.startswith("!"):
        abort(403)
    return render_template("user.html",users=User.query.all(),config=Config,error=error)

@main.route("/user/<string:username>/",methods=["GET","POST"])
@login_required
def user_detail(username:str):
    global error
    error=""
    if not current_user._get_current_object().username.startswith("!"):
        abort(403)
    form=UserChangeForm()
    user=User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        user.password=form.password.data
        db.session.commit()
        print("User pass"+form.password.data)
        return redirect(url_for("main.user_detail",username=username))
    return render_template("user_detail.html",user=user,form=form,config=Config)

@main.route("/user/new/",methods=["GET","POST"])
@login_required
def new_user():
    global error
    if not current_user._get_current_object().username.startswith("!"):
        abort(403)
    form=UserNewForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        try:
            db.session.add(User(username=username,password=password))
            db.session.commit()
        except:
            error="2"
            return redirect(url_for("main.user"))
        error=""      
        return redirect(url_for("main.user"))
    return render_template("user_new.html",form=form,config=Config)

@main.route("/user/delete/<name>",methods=["GET","POST"])
@login_required
def delete(name:str):
    global error
    if not current_user._get_current_object().username.startswith("!"):
        abort(403)
    form=UserDeleteForm()
    user=User.query.filter_by(username=name).first_or_404()
    if form.validate_on_submit():
        repeat=form.repeat.data
        if repeat != name:
            return redirect(url_for("main.user"))
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("main.user"))
    return render_template("user_delete.html",form=form,config=Config)

@main.route("/server/",methods=["GET","POST"])
@login_required
def server():
    settings_form=ServerSettingsForm()
    command_form=CommandForm()
    if settings_form.validate_on_submit():
        key=settings_form.key.data
        value=settings_form.value.data
        return redirect(url_for("server.mc_set",key=key,value=value))
    elif command_form.validate_on_submit():
        return redirect(url_for("server.mc_command",com=command_form.command.data))
    return render_template("server.html",user=current_user._get_current_object(),config=Config,settings_form=settings_form,command_form=command_form)