from flask import Blueprint

main_bp = Blueprint('api', __name__)

from api import route
