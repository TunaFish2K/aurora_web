from flask import Flask
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PropertiesEdit(FlaskForm):
    edit=TextAreaField("Properties内容",validators=[DataRequired()])
    submit=SubmitField("保存")
