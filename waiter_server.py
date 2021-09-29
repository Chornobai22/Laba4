import waitress
import flask_app
print("waitress")
waitress.serve(flask_app.app, host='0.0.0.0', port=80)