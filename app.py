from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Assurez-vous que config.DefaultConfig est bien défini et accessible
# ...

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config.DefaultConfig')
app.config.from_pyfile('config.py', silent=True)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# app.py
from flask_socketio import SocketIO

socketio = SocketIO(app)
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

# Initialisation de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Importation des modèles pour que Flask-Migrate les détecte
from models import User, APIKey, QueryHistory

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Enregistrement des blueprints
from views import auth_blueprint, api_blueprint, main_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(main_blueprint)  # Pas besoin de préfixe d'URL pour le blueprint principal

if __name__ == '__main__':
    socketio.run(app, debug=True)