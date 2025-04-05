from flask import Blueprint

bp = Blueprint('delivery', __name__)

from app.delivery import routes
