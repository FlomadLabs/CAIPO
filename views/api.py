
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify

from LLM.OpenAIService import OpenAIService
from app import db
from models.User import User
from models.APIKey import APIKey
from flask_login import login_required, current_user
from flask_socketio import emit

import json

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/add_api_key', methods=['GET', 'POST'])
@login_required
def add_api_key():
    if request.method == 'POST':
        service_name = request.form.get('service_name')
        key_value = request.form.get('key_value')
        model_type = request.form.get('model_type')


        # Créer et sauvegarder la nouvelle clé API
        new_api_key = APIKey(user_id=current_user.id, service_name=service_name, key_value=key_value , model_type=model_type)
        db.session.add(new_api_key)
        db.session.commit()

        flash(f'La clé API pour {service_name} a été ajoutée avec succès.', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_api_key.html')


@api_blueprint.route('/edit_api_key/<int:key_id>', methods=['GET', 'POST'])
@login_required
def edit_api_key(key_id):
    api_key = APIKey.query.get_or_404(key_id)

    # Assurez-vous que l'utilisateur modifie uniquement ses propres clés.
    if api_key.user_id != current_user.id:
        flash("Vous n'avez pas la permission de modifier cette clé API.", 'danger')
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        service_name = request.form.get('service_name')
        key_value = request.form.get('key_value')
        model_type = request.form.get('model_type')


        # Mise à jour de la clé API
        api_key.service_name = service_name
        api_key.key_value = key_value
        api_key.model_type = model_type
        db.session.commit()

        flash(f'La clé API pour {service_name} a été mise à jour avec succès.', 'success')
        return redirect(url_for('main.dashboard'))

    # Affiche le formulaire de modification avec les informations existantes de la clé API
    return render_template('edit_api_key.html', api_key=api_key)


# views/api.py
# views/api.py
# views/api.py
# views/api.py
@api_blueprint.route('/ask_llm', methods=['POST'])
@login_required
def ask_llm(prompt, service_name, model_type):
    # Récupérer la clé API de la base de données
    api_key_obj = APIKey.query.filter_by(user_id=current_user.id, service_name=service_name, model_type=model_type).first()
    if not api_key_obj:
        return jsonify({'error': 'API Key for the specified LLM service and model not found.'}), 404

    api_key = api_key_obj.key_value
    llm_service = OpenAIService()
    response = llm_service.query(prompt, api_key, model_type)

    # Envoyer la réponse du modèle LLM au client via SocketIO
    emit('message', {'text': response}, broadcast=True)

    return jsonify({'response': response})