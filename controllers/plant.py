# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo responsável pelos formulários de login e criação de contas
############################################################################################################
from flask_wtf import FlaskForm # Utilizado para criação de formulários
from flask_wtf.file import FileAllowed
from wtforms import FloatField, StringField, BooleanField,FileField# Utilizado para criação de campos de entrada
from wtforms.validators import DataRequired # Utilizado para validar os dados

############################################################################################################
# Formulário de planta
############################################################################################################
class PlantController(FlaskForm):
    name = StringField('name', id='name_create', validators=[DataRequired()])
    current_plant = BooleanField('current_plant', id='current_plant')
    image = FileField('Imagem da Planta', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Somente imagens!')])
    
    # Novos campos para as configurações da planta
    recommended_air_humidity = FloatField('Umidade do ar recomendada (%)', validators=[DataRequired()])
    max_temperature = FloatField('Temperatura máxima (°C)', validators=[DataRequired()])
    recommended_soil_humidity = FloatField('Umidade do solo recomendada (%)', validators=[DataRequired()])

############################################################################################################