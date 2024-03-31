# views/main.py
from flask import Blueprint, render_template, redirect, url_for
from flask_socketio import emit
from views.api import ask_llm

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    return redirect(url_for('auth.register'))

@main_blueprint.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# views/main.py
from app import socketio


@socketio.on('message')
def handle_message(data):
    # Récupérer le message de l'utilisateur
    prompt = data['text']

    # Obtenir la réponse du modèle LLM
    response = ask_llm(prompt, 'OPENAI', 'gpt-4-0125-preview')

    # Envoyer la réponse du modèle LLM au client
    emit('message', {'text': response})
