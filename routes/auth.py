# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo responsável pela rotas da autenticação
############################################################################################################

############################################################################################################
# Importando os bibliotecas necessárias
############################################################################################################
from flask import render_template, redirect, request, url_for # Importa as funções responsáveis para renderizar templates, redirecionar, etc.
from flask_login import (
    current_user,
    login_user,
    logout_user
) # Importa as funções para verificar se o usuário está logado
from extensions import db, login_manager
from controllers.auth_controller import LoginForm, CreateAccountForm # Importa as classes de formulários
from models.auth_model import Users # Importa a classe de usuário
from utils import verify_pass # Importa a função de verificação de senha
from flask import Blueprint # Utilizado para criar o blueprint

############################################################################################################
# Criando o blueprint da autenticação
############################################################################################################
blueprint = Blueprint(
    'auth_blueprint',
    __name__,
    url_prefix=''
)

############################################################################################################
# Rota padrão
############################################################################################################
@blueprint.route('/') # Define a rota padrão
def route_default(): # Define a função para a rota padrão
    return redirect(url_for('auth_blueprint.login')) # Redireciona para a página de login

############################################################################################################
# Rota de login
############################################################################################################
@blueprint.route('/login', methods=['GET', 'POST']) # Define a rota de login
def login(): # Define a função para a rota de login
    login_form = LoginForm(request.form) # Cria um objeto do formulário de login
    if 'login' in request.form: # Verifica se o formulário foi submetido

        # Lendo os dados do formulário
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first() # Localiza o usuário no sistema

        # Verifica se o usuário existe e se a senha é válida
        if user and verify_pass(password, user.password):
            login_user(user) # Faz o login do usuário
            return redirect(url_for('auth_blueprint.route_default')) # Redireciona para a página padrão após o login

        # Caso a senha seja inválida ou o usuário não exista, retorna uma mensagem de erro
        return render_template('accounts/login.html', msg='Wrong user or password', form=login_form)

    # Caso o formulário não seja submetido, renderiza a página de login
    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form) # Renderiza a página de login
    return redirect(url_for('home_blueprint.index')) # Redireciona para a página inicial

############################################################################################################
# Rota de criação de conta
############################################################################################################
@blueprint.route('/register', methods=['GET', 'POST']) # Define a rota de criação de conta
def register(): # Define a função para a rota de criação de conta
    create_account_form = CreateAccountForm(request.form) # Cria um objeto do formulário de criação de conta
    if 'register' in request.form: # Verifica se o formulário foi submetido

        # Lendo os dados do formulário
        username = request.form['username']
        email = request.form['email']

        # Verifica se o nome de usuário ou o email já existem
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html', msg='Username already registered', success=False, form=create_account_form) # Renderiza a página de criação de conta com mensagem de erro

        # Verifica se o email já existe
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html', msg='Email already registered', success=False, form=create_account_form)

        # Cria um novo usuário e salva-o no banco de dados
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Faz o logout do usuário e redireciona para a página de login
        logout_user()
        return render_template('accounts/register.html', msg='User created successfully.', success=True, form=create_account_form) # Renderiza a página de criação de conta com mensagem de sucesso
    else: # Caso o formulário não seja submetido, renderiza a página de criação de
        return render_template('accounts/register.html', form=create_account_form) # Renderiza a página de criação de conta

############################################################################################################
# Rota de logout
############################################################################################################
@blueprint.route('/logout') # Define a rota de logout
def logout(): # Define a função para a rota de logout
    logout_user() # Faz o logout do usuário
    return redirect(url_for('auth_blueprint.login')) # Redireciona para a página de login

############################################################################################################
# Configura o login manager para as rotas de erro
############################################################################################################
@login_manager.unauthorized_handler # Função chamada quando um usuário não está logado
def unauthorized_handler(): # Função chamada quando um usuário não está logado
    return render_template('home/page-403.html'), 403 # Renderiza a página de erro 403

@blueprint.errorhandler(403) # Função chamada quando um usuário não tem permissão para acessar uma página
def access_forbidden(error): # Função chamada quando um usuário não tem permissão para acessar uma página
    return render_template('home/page-403.html'), 403 # Renderiza a página de erro 403

@blueprint.errorhandler(404) # Função chamada quando uma página não é encontrada
def not_found_error(error): # Função chamada quando uma página não é encontrada
    return render_template('home/page-404.html'), 404 # Renderiza a página de erro 404

@blueprint.errorhandler(500) # Função chamada quando um erro interno ocorre
def internal_error(error): # Função chamada quando um erro interno ocorre
    return render_template('home/page-500.html'), 500 # Renderiza a página de erro 500

############################################################################################################