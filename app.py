# app.py
from flask import Flask, render_template

from routes.user_routes import user_bp
from routes.pet_routes import pet_bp
from routes.symptom_routes import symptom_bp
from routes.disease_routes import disease_bp
from routes.disease_symptom_routes import disease_symptom_bp
from routes.diagnosis_history_routes import history_bp
from routes.articles_routes import articles_bp
from routes.predict_routes import predict_bp

from util.db import get_db_connection

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

# --- Stránky ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about_app.html")
def about_app():
    return render_template("about_app.html")

@app.route("/articles.html")
def articles():
    return render_template("articles.html")

@app.route("/results.html")
def results():
    return render_template("results.html")

@app.route("/search_page.html")
def search_page():
    return render_template("search_page.html")

@app.route("/sign_in_register.html")
def sign_in_register():
    return render_template("sign_in_register.html")

@app.route("/account.html")
def account():
    return render_template("account.html")

@app.route("/history.html")
def history_page():
    return render_template("history.html")

# --- API blueprints ---
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(pet_bp, url_prefix="/pets")
app.register_blueprint(symptom_bp, url_prefix="/symptoms")
app.register_blueprint(disease_bp, url_prefix="/diseases")
app.register_blueprint(disease_symptom_bp, url_prefix="/disease-symptoms")
app.register_blueprint(history_bp, url_prefix="/diagnosis")
app.register_blueprint(articles_bp, url_prefix="/articles-api")
app.register_blueprint(predict_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
