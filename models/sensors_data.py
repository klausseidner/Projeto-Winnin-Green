# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo responsável pela modelagem do banco de dados e as funções relacionadas
############################################################################################################
from extensions import db # Importa o banco de dados
from datetime import datetime, timezone 

############################################################################################################
# Classe responsável pela modelagem do banco de dados
############################################################################################################
class SensorsData(db.Model):
    __tablename__ = 'Sensors_Data' # Nome da tabela no banco de dados
    id = db.Column(db.Integer, primary_key=True) # Chave primária
    name = db.Column(db.String(64)) # Campo para nome da planta
    plant_id = db.Column(db.Integer, db.ForeignKey('Plants.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    soil_moisture = db.Column(db.Float, nullable=True)
    air_humidity = db.Column(db.Float, nullable=True)
    air_temperature = db.Column(db.Float, nullable=True)
    is_greenhouse_door_open = db.Column(db.Boolean, nullable=True)
    water_for_irrigation_ml = db.Column(db.Float, nullable=True)
    light_uptime = db.Column(db.Float, nullable=True)

    plant = db.relationship('Plants', backref=db.backref('sensor_data', lazy='dynamic'))
    
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
