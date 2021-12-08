from routes import query
from check import *
from flask import Flask
from config import Config
from flask_jwt_extended import JWTManager
from models import TokenBlockList

app = Flask(__name__)
app.register_blueprint(query)
app.config.from_object(Config)

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = s.query(TokenBlockList.id).filter_by(jti=jti).first()
    return token is not None

'''
@query.route('/api', methods=['GET'])
def hello_world():
    return 'Hello world 12', 200
'''

if __name__ == '__main__':
    app.run()
