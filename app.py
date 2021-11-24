from flask import Flask
from routes import query
app = Flask(__name__)
app.register_blueprint(query)
@app.route('/api/v1/hello-world-12')
def hello_world():
    return 'Hello world 12'
