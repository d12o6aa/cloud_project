from flask import Blueprint, render_template, session, redirect, url_for
from infrastructure.repositories.sqlalchemy_repo import SQLAlchemyJobRepo

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

