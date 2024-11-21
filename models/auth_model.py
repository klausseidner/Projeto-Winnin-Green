# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo responsável pela modelagem do banco de dados e as funções relacionadas
############################################################################################################
from flask_login import UserMixin # Utilizado para permitir que os objetos da classe Users sejam utilizados como usuários
from extensions import db, login_manager # Importa o banco de dados e o gerenciador de login
from utils import hash_pass # Importa a função de criptografia de senha

############################################################################################################
# Classe responsável pela modelagem do banco de dados
############################################################################################################
class Users(db.Model, UserMixin):
    __tablename__ = 'Users' # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True) # Chave primária
    username = db.Column(db.String(64), unique=True) # Campo para o nome de usuário
    email = db.Column(db.String(64), unique=True) # Campo para o e-mail
    password = db.Column(db.LargeBinary) # Campo para a senha criptografada

############################################################################################################
    # Método construtor que inicializa os atributos da classe
############################################################################################################
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # dependendo se o valor é iterável ou não,
            # devemos descompactar seu valor (quando **kwargs é request.form, alguns valores será uma lista de 1 elemento)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0] # Pegamos apenas o primeiro elemento da lista

            # Criptografamos a senha caso seja uma string (senha)
            if property == 'password':
                value = hash_pass(value)  # Criptografamos a senha
            setattr(self, property, value) # Atribuimos o valor ao atributo da classe

############################################################################################################
    # Método que retorna uma representação do objeto
############################################################################################################
    def __repr__(self):
        return str(self.username) # Retornamos a representação do nome do usuário

############################################################################################################
# Configura o gerenciador de login para usar a classe Users
############################################################################################################
@login_manager.user_loader # Define a função que retorna o usuário a partir do ID do usuário
def user_loader(id): # Função que retorna o usuário a partir do ID do usuário
    return Users.query.filter_by(id=id).first() # Retorna o usuário com o ID especificado

############################################################################################################
# Método que verifica se o usuário está logado
############################################################################################################
@login_manager.request_loader # Define a função que verifica se o usuário está logado
def request_loader(request): # Função que verifica se o usuário está logado
    username = request.form.get('username') # Pega o nome de usuário do formulário
    user = Users.query.filter_by(username=username).first() # Verifica se o usuário existe no banco de dados
    return user if user else None # Retorna o usuário se ele existir, senão retorna None

############################################################################################################