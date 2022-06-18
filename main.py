from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
import os


app = Flask(__name__)
# load_dotenv(r"E:\PYTHON_BOOTCAMP_Dr_ANGELA_YU\Todolist\.env")
app.config['SECRET_KEY'] = "ks#dvjvijrw@WPIVG34V%LAl" #os.environ.get("SECURITY_KEY")
Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASES_URL', 'sqlite:///todolist.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(500), nullable=False)

db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="192.168.68.107", port=5000,debug=True)
