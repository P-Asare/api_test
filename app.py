from flask import Flask
from routes.auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix='/auth')
# app.register_blueprint(actions_bp, url_prefix='/actions')

if __name__ == '__main__':
    app.run(debug=True)