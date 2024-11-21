# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo responsável pela modelagem do banco de dados e as funções relacionadas
############################################################################################################
from extensions import db # Importa o banco de dados

############################################################################################################
# Classe responsável pela modelagem do banco de dados
############################################################################################################
class SystemConfig(db.Model):
    __tablename__ = 'System_Configs'  # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True)
    current_plant_id = db.Column(db.Integer, db.ForeignKey('Plants.id'), nullable=False)

    # Relação com a tabela Plant
    current_plant = db.relationship('Plants', backref=db.backref('System_Configs', uselist=False))
    
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
