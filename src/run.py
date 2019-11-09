from flask import Flask
from config import config

def create_app(config_name):
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config[config_name])

    # INIT ROUTES
    from users.routes import user_bp, auth_bp
    app.register_blueprint(user_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1')

    # INIT DB
    from users.model import db
    db.init_app(app)

    return app

if __name__ == '__main__':
    app = create_app('default')
    app.run(ssl_context=('config/myCrt.pem', 'config/myKey.pem'), host = '0.0.0.0', port = 8080)
