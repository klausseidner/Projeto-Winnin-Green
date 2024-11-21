# -*- encoding: utf-8 -*-
############################################################################################################
# Arquivo responsável pela rotas da autenticação
############################################################################################################

############################################################################################################
# Importando os bibliotecas necessárias
############################################################################################################
from flask import render_template, redirect, request, url_for,current_app, flash # Importa as funções responsáveis para renderizar templates, redirecionar, etc.
import os
from extensions import db # Importa o a conexão com o banco e o blueprint da planta
from controllers.plant import PlantController # Importa as classes de formulários
from light_schedule import LightScheduleForm
from models.light_schedule import LightSchedule
from models.plants import Plants # Importa a classe da planta
from flask_login import login_required # Importando a função login_required para garantir que apenas usuários logados possam acessar as rotas
from flask import Blueprint # Utilizado para criar o blueprint
from models.system_config import SystemConfig 
from werkzeug.utils import secure_filename


############################################################################################################
# Criando o blueprint plant
############################################################################################################
blueprint = Blueprint(
    'plant_blueprint',
    __name__,
    url_prefix=''
)

############################################################################################################
# Rota padrão
############################################################################################################
@blueprint.route('/plants', methods=['GET'])
@login_required
def plant():
    plants = Plants.query.all()
    return render_template('plant/plant-table.html', plants=plants, segment='plant')

@blueprint.route('/plant/create', methods=['GET', 'POST'])
@login_required
def createPlant():
    create_plant_form = PlantController()
    if create_plant_form.validate_on_submit():
        name = create_plant_form.name.data
        image = create_plant_form.image.data
        recommended_air_humidity = create_plant_form.recommended_air_humidity.data
        max_temperature = create_plant_form.max_temperature.data
        recommended_soil_humidity = create_plant_form.recommended_soil_humidity.data

        plant = Plants(
            name=name,
            recommended_air_humidity=recommended_air_humidity,
            max_temperature=max_temperature,
            recommended_soil_humidity=recommended_soil_humidity
        )

        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            plant.image_filename = filename

        db.session.add(plant)
        db.session.commit()

        set_as_current = request.form.get('set_as_current') == 'on'
        if set_as_current:
            config = SystemConfig.query.first()
            if config:
                config.current_plant_id = plant.id
            else:
                config = SystemConfig(current_plant_id=plant.id)
                db.session.add(config)
            db.session.commit()

        return redirect(url_for('plant_blueprint.plant'))
    else:
        return render_template('plant/plant-create.html', form=create_plant_form)

@blueprint.route('/plant/<name>', methods=['GET', 'POST'])
@login_required
def edit_plant(name):
    plant = Plants.query.filter_by(name=name).first_or_404()
    form = PlantController(obj=plant)

    if form.validate_on_submit():
        plant.name = form.name.data
        plant.recommended_air_humidity = form.recommended_air_humidity.data
        plant.max_temperature = form.max_temperature.data
        plant.recommended_soil_humidity = form.recommended_soil_humidity.data

        image = form.image.data
        if image:
            filename = secure_filename(image.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            plant.image_filename = filename

        db.session.commit()

        set_as_current = request.form.get('set_as_current') == 'on'
        if set_as_current:
            config = SystemConfig.query.first()
            if config:
                config.current_plant_id = plant.id
            else:
                config = SystemConfig(current_plant_id=plant.id)
                db.session.add(config)
            db.session.commit()

        return redirect(url_for('plant_blueprint.plant'))

    config = SystemConfig.query.first()
    is_current_plant = (config.current_plant_id == plant.id) if config else False

    return render_template('plant/plant-edit.html', plant=plant, form=form, is_current_plant=is_current_plant)


@blueprint.route('/plant/<int:plant_id>/update', methods=['POST'])
@login_required
def update_plant(plant_id):
    plant = Plants.query.get_or_404(plant_id)
    plant.name = request.form['name']
    db.session.commit()

    # Verifica se o usuário deseja definir como planta atual
    set_as_current = request.form.get('set_as_current') == 'on'
    if set_as_current:
        config = SystemConfig.query.first()
        if config:
            config.current_plant_id = plant.id
        else:
            config = SystemConfig(current_plant_id=plant.id)
            db.session.add(config)
        db.session.commit()

    return redirect(url_for('plant_blueprint.plant'))

@blueprint.route('/plant/<int:plant_id>/delete', methods=['POST'])
@login_required
def delete_plant(plant_id):
    plant = Plants.query.get_or_404(plant_id)  # Busca a planta pelo id ou retorna 404

    # Verifica se a planta a ser deletada é a planta atual
    config = SystemConfig.query.first()
    if config and config.current_plant_id == plant.id:
        # Remove o registro da tabela SystemConfig, pois ele é único e refere-se à planta atual
        db.session.delete(config)

    db.session.delete(plant)  # Deleta a planta do banco de dados
    db.session.commit()  # Confirma a exclusão no banco de dados

    return redirect(url_for('plant_blueprint.plant'))  # Redireciona de volta à lista de plantas

@blueprint.route('/select_current_plant', methods=['GET', 'POST'])
@login_required
def select_current_plant():
    plants = Plants.query.all()
    if request.method == 'POST':
        plant_id = request.form.get('plant_id')
        config = SystemConfig.query.first()
        if config:
            config.current_plant_id = plant_id
            db.session.commit()
        else:
            config = SystemConfig(current_plant_id=plant_id)
            db.session.add(config)
            db.session.commit()
        return redirect(url_for('home_blueprint.index'))
    return render_template('plant/select_current_plant.html', plants=plants)

@blueprint.route('/update_dashboard_plant', methods=['POST'])
@login_required
def update_dashboard_plant():
    selected_plant_id = request.form.get('plant_id')
    config = SystemConfig.query.first()
    if config:
        config.current_plant_id = selected_plant_id
    else:
        config = SystemConfig(current_plant_id=selected_plant_id)
        db.session.add(config)
    db.session.commit()
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/plant/<name>/scheduledtask', methods=['GET', 'POST'])
@login_required
def configure_light_schedule(name):
    plant = Plants.query.filter_by(name=name).first_or_404()
    config = SystemConfig.query.first()
    form = LightScheduleForm(plant_id=plant.id)

    # Carregar dados de horários, se a planta já tiver uma rotina
    schedules = LightSchedule.query.filter_by(plant_id=plant.id).all()
    if schedules:
        for schedule in schedules:
            field_start = getattr(form, f"{schedule.day_of_week.lower()}_start")
            field_end = getattr(form, f"{schedule.day_of_week.lower()}_end")
            field_start.data = schedule.start_time
            field_end.data = schedule.end_time

    # Processar o formulário ao submeter
    if form.validate_on_submit():
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for day in days:
            start_time = getattr(form, f"{day}_start").data
            end_time = getattr(form, f"{day}_end").data

            # Adiciona ou atualiza o registro de rotina de luz para cada dia da semana
            schedule = LightSchedule.query.filter_by(plant_id=plant.id, day_of_week=day.capitalize()).first()
            if schedule:
                schedule.start_time = start_time
                schedule.end_time = end_time
            else:
                new_schedule = LightSchedule(
                    plant_id=plant.id,
                    day_of_week=day.capitalize(),
                    start_time=start_time,
                    end_time=end_time
                )
                db.session.add(new_schedule)

        db.session.commit()
        flash('Rotina de luz atualizada com sucesso!', 'success')
        return redirect(url_for('plant_blueprint.plant'))

    return render_template('plant/plant-schedule.html', form=form, plant=plant, is_current_plant=(config and config.current_plant_id == plant.id))




############################################################################################################