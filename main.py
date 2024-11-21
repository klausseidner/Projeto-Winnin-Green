# -*- encoding: utf-8 -*-
############################################################################################################
#
# Ardudeck - Sistema completo para IoT
# Desenvolvido por: Klaus Seidner
# GitHub: https://github.com/klausseidner/ardudeck
#
############################################################################################################

############################################################################################################
# Importando bibliotecas
############################################################################################################
import os # Utilizado para manipular o sistema operacional
import sys # Utilizado para manipular o sistema operacional
import importlib.util # Utilizado para importar módulos dinamicamente
from extensions import db, login_manager # Utilizado para gerenciar o login do usuário
from flask_migrate import Migrate # Utilizado para realizar migrações do banco de dados
from flask_minify import Minify # Utilizado para minificar o código HTML e CSS
from sys import exit # Utilizado para encerrar o programa
from config import config_dict # Importando as configurações do sistema
from flask import Flask # Utilizado para criar o aplicativo Flask
from flask_login import LoginManager # Utilizado para gerenciar o login do usuário
from flask_sqlalchemy import SQLAlchemy # Utilizado para gerenciar o banco de dados
from importlib import import_module # Utilizado para importar módulos dinamicamente
base_dir = os.path.dirname(os.path.abspath(__file__)) # Definindo o diretório base do sistema
sys.path.append(base_dir) # Adicionando o diretório base ao caminho de importação
sys.path.append(os.path.join(base_dir, 'controllers')) # Adicionando o diretório do controllers ao caminho de importação
sys.path.append(os.path.join(base_dir, 'models')) # Adicionando o diretório do models ao caminho de importação
sys.path.append(os.path.join(base_dir, 'routes')) # Adicionando o diretório do routes ao caminho de importação

############################################################################################################
# Configurando as extensões do Flask
############################################################################################################
# db = SQLAlchemy() # Instanciando o SQLAlchemy
# login_manager = LoginManager() # Instanciando o LoginManager

############################################################################################################
# Registrando as extensões do Flask
############################################################################################################
def register_extensions(app):
    db.init_app(app) # Registrando o SQLAlchemy
    login_manager.init_app(app) # Registrando o LoginManager

############################################################################################################
# Função para registrar os blueprints dos módulos do sistema
############################################################################################################
def register_blueprints(app):
    base_dir = os.path.dirname(os.path.abspath(__file__)) # Obtém a pasta do arquivo
    
    # Carrega os módulos do sistema
    for module_name in ('auth', 'home', 'plants'): 
        # Define o caminho completo para o módulo
        module_path = os.path.join(base_dir, 'routes', f"{module_name}.py")
        
        # Carrega o módulo a partir do caminho específico
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec) # Carrega o módulo
        sys.modules[module_name] = module # Adiciona o módulo ao sys.modules
        spec.loader.exec_module(module) # Executa o módulo
        
        # Registra o blueprint
        app.register_blueprint(module.blueprint)

############################################################################################################
# Função para configurar o banco de dados do sistema
############################################################################################################
def configure_database(app):

    @app.before_first_request # Executado antes de qualquer requisição
    def initialize_database(): # Cria o banco de dados caso ele não exista
        try: # Tenta criar o banco de dados
            db.create_all() # Cria o banco de dados
        except Exception as e: # Se houver algum erro
            print('> Error: DBMS Exception: ' + str(e) ) # Imprime o erro
            # Fallback para SQLite
            basedir = os.path.abspath(os.path.dirname(__file__)) # Obtém a pasta do arquivo
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3') # Configura a URI do banco de dados
            print('> Fallback to SQLite ') # Imprime a mensagem de fallback para SQLite
            db.create_all() # Cria o banco de dados

    @app.teardown_request # Executado após cada requisição
    def shutdown_session(exception=None): # Fecha a sessão do banco de dados
        db.session.remove() # Fecha a sessão

############################################################################################################
# Função para criar o aplicativo Flask
############################################################################################################
def create_app(config):
    app = Flask(__name__, template_folder='views') # Criando o aplicativo Flask
    app.config.from_object(config) # Configurando o aplicativo com as configurações do módulo
    register_extensions(app) # Registrando as extensões do Flask
    register_blueprints(app) # Registrando os blueprints dos módulos
    configure_database(app) # Configurando o banco de dados do sistema
    return app # Retornando o aplicativo Flask

############################################################################################################

############################################################################################################
# Configurando o Flask
############################################################################################################
# ATENÇÃO: Não deixe TRUE para DEBUG em produção, pois isso pode ocasionar vulnerabilidades.
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# Definindo o modo de configuração do sistema (Debug ou Produção)
get_config_mode = 'Debug' if DEBUG else 'Production'

# Carregando a configuração do sistema de acordo com o modo desejado (Debug ou Produção)
try: # Tenta carregar a configuração do sistema
    app_config = config_dict[get_config_mode.capitalize()] # Carregando a configuração do sistema
except KeyError: # Caso a configuração seja inválida, encerra o programa
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ') # Exibe uma mensagem de erro

app = create_app(app_config) # Criando o aplicativo com a configuração carregada
Migrate(app, db) # Configurando o Flask Migrate para realizar migrações do banco de dados

# Configurando o Flask Minify para minificar o código HTML e CSS (em produção)
if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False) # Configura o Flask Minify para minificar o código HTML e CSS

# Exibindo informações do sistema (em modo de desenvolvimento)
if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG)             ) # Exibe a configuração do modo de desenvolvimento
    app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE' ) # Exibe a configuração da compressão de página
    app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI) # Exibe a configuração do banco de dados
    app.logger.info('ASSETS_ROOT      = ' + app_config.ASSETS_ROOT ) # Exibe a configuração da pasta de assets

# Inicializando o Flask
if __name__ == "__main__":
    app.run() # Iniciando o Flask

############################################################################################################