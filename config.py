# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo de Configuração
############################################################################################################

############################################################################################################
# Importação de Bibliotecas
############################################################################################################
import os, random, string # Utilizado para gerar uma chave secreta aleatória

############################################################################################################
# Configurações do Sistema
############################################################################################################
class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__)) # Definindo a pasta base do sistema
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets') # Definindo a pasta de assets
    
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads') # Definindo a pasta de uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limite de 16MB
    print(UPLOAD_FOLDER) # Imprime a pasta de uploads
    SECRET_KEY  = os.getenv('SECRET_KEY', None) # Definindo a chave secreta do sistema
    # Gerando uma chave secreta aleatória se a chave não foi definida
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 )) # Gerando uma chave secreta aleatória

    SQLALCHEMY_TRACK_MODIFICATIONS = False # Desabilitando a modificação de objetos

    DB_ENGINE   = os.getenv('DB_ENGINE'   , None) # Definindo o motor de banco de dados
    DB_USERNAME = os.getenv('DB_USERNAME' , None) # Definindo o nome de usuário do banco de dados
    DB_PASS     = os.getenv('DB_PASS'     , None) # Definindo a senha do banco de dados
    DB_HOST     = os.getenv('DB_HOST'     , None) # Definindo o host do banco de dados
    DB_PORT     = os.getenv('DB_PORT'     , None) # Definindo a porta do banco de dados
    DB_NAME     = os.getenv('DB_NAME'     , None) # Definindo o nome do banco de dados

    USE_SQLITE  = True # Flag para indicar se o sistema será executado em modo de desenvolvimento

    # Definição da URL do banco de dados (em modo de desenvolvimento)
    if DB_ENGINE and DB_NAME and DB_USERNAME:
        try: # Tentando conectar ao banco de dados
            # Conectando ao banco de dados (SQLite) se não houver outro motor de banco de dados definido)
            SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
                DB_ENGINE,
                DB_USERNAME,
                DB_PASS,
                DB_HOST,
                DB_PORT,
                DB_NAME
            ) 
            USE_SQLITE  = False # Desabilitando o uso do SQLite
        except Exception as e: # Caso ocorra uma exceção durante a conexão ao banco de dados, exibe uma mensagem de erro e usa o SQLite
            print('> Error: DBMS Exception: ' + str(e) ) # Exibe uma mensagem de erro
            print('> Fallback to SQLite ') # Desabilita o uso do SQLite


    # Definição da URL do banco de dados (em modo de produção)
    if USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3') # Definindo a URL do banco de dados (SQLite)
    
############################################################################################################
# Configurações do Sistema (em modo de produção)
############################################################################################################
class ProductionConfig(Config):
    DEBUG = False # Desabilitando o modo de desenvolvimento
    # Seguridade das sessões
    SESSION_COOKIE_HTTPONLY = True # Garantindo que o cookie de sessão não seja acessível via JavaScript
    REMEMBER_COOKIE_HTTPONLY = True # Garantindo que o cookie de lembrança não seja acessível via JavaScript
    REMEMBER_COOKIE_DURATION = 3600 # Definindo a duração do cookie de lembrança em segundos

############################################################################################################
# Configurações do Sistema (em modo de desenvolvimento)
############################################################################################################
class DebugConfig(Config):
    DEBUG = True # Habilitando o modo de desenvolvimento

############################################################################################################
# Carregando as configurações do sistema
############################################################################################################
config_dict = {
    'Production': ProductionConfig, # Carregando as configurações do sistema em modo de produção
    'Debug'     : DebugConfig , # Carregando as configurações do sistema em modo de desenvolvimento
}

############################################################################################################