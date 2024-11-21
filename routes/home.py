# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo de Configuração de rotas
############################################################################################################

############################################################################################################
# Importação de bibliotecas necessárias
############################################################################################################
from flask import redirect, render_template, request, url_for # Importando a função render_template para renderizar templates
from flask_login import login_required # Importando a função login_required para garantir que apenas usuários logados possam acessar as rotas
from jinja2 import TemplateNotFound # Importando a exceção TemplateNotFound para tratar erros de template não encontrados
from estufa import EstufaController
from models.plants import Plants  # Importa o modelo Plant
from flask import Blueprint

from models.sensors_data import SensorsData
from models.system_config import SystemConfig # Utilizado para criar o blueprint

############################################################################################################
# Criando o blueprint da home
############################################################################################################
blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix=''
)

############################################################################################################
# Definição de rota principal
############################################################################################################
@blueprint.route('/index')
@login_required
def index():
    config = SystemConfig.query.first()
    estufa = EstufaController()  # Instancia o controlador da estufa

    # Obtenção de dados em tempo real dos sensores
    temperature = estufa.temperatura()
    soil_moisture = estufa.umidade_solo()
    air_humidity = estufa.umidade_ar()
    flame_detected = estufa.chamas()
    water_reserve = estufa.reserva_agua()
    door_status = estufa.luz()

    if config and config.current_plant_id:
        plant = Plants.query.get(config.current_plant_id)
        plants = Plants.query.all()
        latest_sensor_data = SensorsData.query.filter_by(plant_id=plant.id).order_by(SensorsData.timestamp.desc()).first()
        
        # Passa os dados dos sensores em tempo real e do banco de dados para o template
        return render_template(
            'home/index.html',
            segment='index',
            plant=plant,
            plants=plants,
            sensor_data=latest_sensor_data,
            temperature=temperature,
            soil_moisture=soil_moisture,
            air_humidity=air_humidity,
            flame_detected=flame_detected,
            water_reserve=water_reserve,
            door_status=door_status
        )
    else:
        plants = Plants.query.all()
        return render_template(
            'home/index.html',
            segment='index',
            plants=plants,
            plant=None,
            temperature=temperature,
            soil_moisture=soil_moisture,
            air_humidity=air_humidity,
            flame_detected=flame_detected,
            water_reserve=water_reserve,
            door_status=door_status
        )


############################################################################################################
# Rotas para views personalizadas
############################################################################################################
@blueprint.route('/<views>')
@login_required # Garantindo que apenas usuários logados possam acessar as rotas
def route_template(views): # Definindo a função route_template
    try: # Tente executar o seguinte bloco de código
        if not views.endswith('.html'): # Verificando se o views termina com '.html'
            views += '.html' # Se não, adiciona '.html' ao final do view
        segment = get_segment(request) # Capturando o segmento da rota
        return render_template("home/" + views, segment=segment) # Renderizando a view com o segmento
    except TemplateNotFound: # Se o template não for encontrado
        return render_template('home/page-404.html'), 404 # Renderizando a view de erro 404
    except: # Se ocorrer algum erro
        return render_template('home/page-500.html'), 500 # Renderizando a view de erro 500


############################################################################################################
# Função para capturar o segmento da rota
############################################################################################################
def get_segment(request):
    try: # Tente executar o seguinte bloco de código
        segment = request.path.split('/')[-1] # Capturando o segmento da rota
        if segment == '': # Se o segmento for vazio
            segment = 'index' # Definindo o segmento como 'index'
        return segment # Retornando o segmento
    except: # Se ocorrer algum erro
        return None # Retornando None
    
############################################################################################################