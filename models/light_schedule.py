# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo responsável pela modelagem do banco de dados e as funções relacionadas
############################################################################################################
from extensions import db  # Importa o banco de dados

############################################################################################################
# Classe responsável pela modelagem dos horários de luz
############################################################################################################
class LightSchedule(db.Model):
    __tablename__ = 'Light_Schedule'
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('Plants.id'), nullable=False)  # Relacionamento com a planta
    day_of_week = db.Column(db.String(10), nullable=False)  # Dia da semana
    start_time = db.Column(db.Time, nullable=False)  # Hora de início
    end_time = db.Column(db.Time, nullable=False)  # Hora de fim

    ############################################################################################################
    # Método construtor que inicializa os atributos da classe
    ############################################################################################################
    def __init__(self, plant_id, day_of_week, start_time, end_time):
        self.plant_id = plant_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time