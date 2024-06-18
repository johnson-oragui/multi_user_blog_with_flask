from flask import Blueprint

authenticate = Blueprint('authenticate', __name__)
dashboard = Blueprint('dashboard', __name__)
views = Blueprint('views', __name__)
admin = Blueprint('admin', __name__)


from . import comments, auth
from . import users, blogs
from . import home, about
from . import admin