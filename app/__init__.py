from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)

    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    print("Registered auth blueprint")

    from app.delivery.routes import bp as delivery_bp
    app.register_blueprint(delivery_bp)
    print("Registered delivery blueprint")

    # Вывод всех зарегистрированных маршрутов
    with app.app_context():
        print("Registered endpoints:", app.url_map)

    return app

app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
