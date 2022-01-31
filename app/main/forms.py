from re import L
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import PasswordField,SubmitField, StringField,TextAreaField
from wtforms.validators import DataRequired,Length

class UserChangeForm(FlaskForm):
    password=PasswordField(validators=[DataRequired(),Length(min=1,max=32)])
    submit=SubmitField("修改Profile")

class UserNewForm(UserChangeForm):
    username=StringField(validators=[DataRequired(),Length(min=1,max=64)])
    submit=SubmitField("新建Profile")

class UserDeleteForm(FlaskForm):
    repeat=StringField(validators=[DataRequired(),Length(min=1,max=64)])
    submit=SubmitField("确认")

class ServerSettingsForm(FlaskForm):
    key=StringField(validators=[DataRequired()])
    value=StringField(validators=[DataRequired()])
    submit=SubmitField("设置")

class CommandForm(FlaskForm):
    command=TextAreaField("指令")
    submit=SubmitField("运行")