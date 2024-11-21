from flask_sqlalchemy import SQLAlchemy # Importa a biblioteca SQLAlchemy para o Flask
from flask_login import LoginManager # Importa a biblioteca LoginManager para o Flask

db = SQLAlchemy() # Instancia a biblioteca SQLAlchemy
login_manager = LoginManager() # Instancia a biblioteca LoginManager