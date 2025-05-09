import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask
from dotenv import load_dotenv
from web.routes.auth_routes import auth_bp
from web.routes.job_routes import job_bp       
from web.routes.offer_routes import offer_bp   
from web.routes.home_routes import home_bp
from web.routes.main_routes import main_bp

load_dotenv()

app = Flask(__name__, template_folder="web/templates")

app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(home_bp, url_prefix="/")
app.register_blueprint(job_bp, url_prefix="/jobs")
app.register_blueprint(offer_bp, url_prefix="/offers")
app.register_blueprint(main_bp)
if __name__ == "__main__":
    app.run(debug=True)
