# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo responsável pelos formulários de login e criação de contas
############################################################################################################
from flask_wtf import FlaskForm # Utilizado para criação de formulários
from wtforms import StringField, PasswordField # Utilizado para criação de campos de entrada
from wtforms.validators import Email, DataRequired # Utilizado para validar os dados

############################################################################################################
# Formulário de login
############################################################################################################
class LoginForm(FlaskForm):
    username = StringField('Username', id='username_login', validators=[DataRequired()]) # Campo para o nome de usuário
    password = PasswordField('Password', id='pwd_login', validators=[DataRequired()]) # Campo para a senha

############################################################################################################
# Formulário de criação de conta
############################################################################################################
class CreateAccountForm(FlaskForm):
    username = StringField('Username', id='username_create', validators=[DataRequired()]) # Campo para o nome de usuário
    email = StringField('Email', id='email_create', validators=[DataRequired(), Email()]) # Campo para o e-mail
    password = PasswordField('Password', id='pwd_create', validators=[DataRequired()]) # Campo para a senha

############################################################################################################