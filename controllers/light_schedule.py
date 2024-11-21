# -*- encoding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import TimeField, HiddenField
from wtforms.validators import DataRequired

class LightScheduleForm(FlaskForm):
    plant_id = HiddenField('plant_id', validators=[DataRequired()])
    monday_start = TimeField('Segunda-feira Início', validators=[DataRequired()])
    monday_end = TimeField('Segunda-feira Fim', validators=[DataRequired()])
    tuesday_start = TimeField('Terça-feira Início', validators=[DataRequired()])
    tuesday_end = TimeField('Terça-feira Fim', validators=[DataRequired()])
    wednesday_start = TimeField('Quarta-feira Início', validators=[DataRequired()])
    wednesday_end = TimeField('Quarta-feira Fim', validators=[DataRequired()])
    thursday_start = TimeField('Quinta-feira Início', validators=[DataRequired()])
    thursday_end = TimeField('Quinta-feira Fim', validators=[DataRequired()])
    friday_start = TimeField('Sexta-feira Início', validators=[DataRequired()])
    friday_end = TimeField('Sexta-feira Fim', validators=[DataRequired()])
    saturday_start = TimeField('Sábado Início', validators=[DataRequired()])
    saturday_end = TimeField('Sábado Fim', validators=[DataRequired()])
    sunday_start = TimeField('Domingo Início', validators=[DataRequired()])
    sunday_end = TimeField('Domingo Fim', validators=[DataRequired()])
