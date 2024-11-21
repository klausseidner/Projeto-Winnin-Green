# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo responsável pela modelagem do banco de dados e as funções relacionadas
############################################################################################################
from extensions import db # Importa o banco de dados

############################################################################################################
# Classe responsável pela modelagem do banco de dados
############################################################################################################
class Plants(db.Model):
    __tablename__ = 'Plants' # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    recommended_air_humidity = db.Column(db.Float, nullable=True)
    max_temperature = db.Column(db.Float, nullable=True)
    recommended_soil_humidity = db.Column(db.Float, nullable=True)
    image_filename = db.Column(db.String(256), nullable=True)  # Campo para o nome do arquivo da imagem
    
############################################################################################################
    # Método construtor que inicializa os atributos da classe
############################################################################################################
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # dependendo se o valor é iterável ou não,
            # devemos descompactar seu valor (quando **kwargs é request.form, alguns valores será uma lista de 1 elemento)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0] # Pegamos apenas o primeiro elemento da lista
            setattr(self, property, value) # Atribuimos o valor ao atributo da classe
