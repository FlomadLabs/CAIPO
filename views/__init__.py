# views/__init__.py
from .auth import auth_blueprint
from .api import api_blueprint
from .main import main_blueprint  # Make sure this line is present

def register_blueprints(app):
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(main_blueprint)  # And this line too