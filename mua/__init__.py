from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')
    
    return app