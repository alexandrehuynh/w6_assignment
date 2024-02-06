from flask import Flask
from config import Config
from .blueprints.site.routes import site # add this import to grab out site blueprint


# instantiate our Flask app
app = Flask(__name__) # is passing in the name of our directory as the name of our app

# going to tell our app what Class to look to for configuration
app.config.from_object(Config)

app.register_blueprint(site) # Here is where we register the blueprints
    # register_blueprint is a method