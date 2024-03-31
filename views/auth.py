# views/auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from app import db
from models.User import User
from flask_login import login_user
from flask_login import logout_user


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Vérifier si l'utilisateur existe déjà
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Un utilisateur avec ce nom ou cette adresse email existe déjà.')
            return redirect(url_for('auth.register'))

        # Création d'un nouvel utilisateur
        new_user = User(username=username, email=email, hashed_password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# views/auth.py (continuation)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Nom d’utilisateur ou mot de passe incorrect.', 'danger')

    return render_template('login.html')
# views/auth.py (continuation)


@auth_blueprint.route('/logout')
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for('main.home'))  # Change 'main.index' to 'main.home'