import os
import sys

from flask import Flask
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web.routes.auth_routes import auth_bp
from web.routes.job_routes import job_bp       
from web.routes.offer_routes import offer_bp   
from web.routes.home_routes import home_bp
from web.routes.main_routes import main_bp
from web.routes.client_routes import client_bp
from web.routes.freelance_routes import freelance_bp

if os.environ.get("FLASK_ENV") != "production":
    load_dotenv()

app = Flask(__name__, template_folder="web/templates")

print("SECRET_KEY:", os.getenv("SECRET_KEY"))

app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY not set in environment variables!")

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(home_bp, url_prefix="/")
app.register_blueprint(job_bp, url_prefix="/jobs")
app.register_blueprint(offer_bp, url_prefix="/offers")
app.register_blueprint(client_bp, url_prefix='/client')
app.register_blueprint(freelance_bp, url_prefix="/freelancer")
app.register_blueprint(main_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
