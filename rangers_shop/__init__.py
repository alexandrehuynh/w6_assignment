from flask import Flask
from flask_migrate import Migrate 


#internal imports 
from .blueprints.site.routes import site 
from .blueprints.auth.routes import auth
from config import Config 
from .models import login_manager, db 

# instantiate our Flask app
app = Flask(__name__) # is passing in the name of our directory as the name of our app
app.config.from_object(Config) # going to tell our app what Class to look to for configuration

#wrap our app in login_manager so we can use it wherever in our app
login_manager.init_app(app)
login_manager.login_view = 'auth.sign_in' 
login_manager.login_message = "Hey you! Log in please!"
login_manager.login_message_category = 'warning'


app.register_blueprint(site) # Here is where we register the blueprints
    # register_blueprint is a method
app.register_blueprint(auth)

#instantiating our datbase & wrapping our app
db.init_app(app)
migrate = Migrate(app, db)