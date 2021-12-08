from marshmallow import ValidationError
from flask import jsonify, request, Blueprint
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager, get_jwt
from schemas import *
from datetime import timezone,datetime
from models import *

query = Blueprint("query", __name__)
b = Bcrypt()
