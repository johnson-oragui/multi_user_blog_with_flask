import dotenv
from flask import Flask, g
from flask_wtf import CSRFProtect
from configs.config import Config
from views import views, dashboard, authenticate, admin

dotenv.load_dotenv()


def flask_app():
    

    app = Flask(__name__)
    app.config.from_object(Config)

    csrf = CSRFProtect(app)

    app.url_map.strict_slashes = False

    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(authenticate)
    app.register_blueprint(views)
    app.register_blueprint(admin)

    return app
