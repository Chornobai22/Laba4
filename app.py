from routes import query
from check import *
from flask import Flask
from config import *
from flask_jwt_extended import JWTManager
from models import TokenBlockList
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(query)
app.config.from_object(Config)
CORS(app, origins='*',
     headers=['Content-Type', 'Authorization'],
     expose_headers='Authorization')
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = s.query(TokenBlockList.id).filter_by(jti=jti).first()
    return token is not None


if __name__ == '__main__':
    app.run()
