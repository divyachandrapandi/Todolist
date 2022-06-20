from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_share import Share
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
import os
from dotenv import load_dotenv
# --------------app config-----------------------#
app=Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECURITY_KEY")
share=Share(app)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASES_URL', 'sqlite:///todo.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# ------------------database----------------------#

class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(500), nullable=False)
    task_status = db.Column(db.Boolean, default=False)     # complete=1 or active=0
    date = db.Column(db.String(250), nullable=True)
    overdue = db.Column(db.Boolean, default=False)  # date overdue=1 not =0

# db.create_all()

@app.route("/", methods=["GET","POST"])
def home():

    todo_list = TodoModel.query.all()
    return render_template('index.html', todo_list=todo_list)


@app.route('/add',methods=["GET","POST"])
def add():
    print(request.form)
    title= request.form.get("todo_title")
    category =request.form.get("category")
    new_todo = TodoModel(title= title , category=category )
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/update/<int:todo_id>",methods=["GET","POST"])
def update(todo_id):
    todo_to_update = TodoModel.query.get(todo_id)

    date = request.form.get('date')
    todo_to_update.date = date
    db.session.commit()
    return redirect((url_for('home')))

@app.route("/complete/<int:todo_id>", methods=["GET","POST"])
def complete(todo_id):
    todo_clicked = TodoModel.query.get(todo_id)
    todo_clicked.task_status = not todo_clicked.task_status
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete/<int:todo_id>", methods=["GET","POST"])
def delete(todo_id):
    todo_to_delete = TodoModel.query.get(todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/filter/<category>", methods=["POST","GET"])
def filter(category):
    if category == "nofilter":

        return redirect(url_for('home'))
    else:
        default_todo  = TodoModel.query.filter_by(category=category).order_by(TodoModel.id.desc())
        for todo in default_todo:
            t = todo.title
            print(t)
    return render_template('index.html', todo_list=default_todo)
#
# @app.route("/filter/<category>", methods=["POST","GET"])
# def filterbywork(category):
#     work_todo = TodoModel.query.get(category)
#     return render_template('index.html', todo_list=work_todo)
#
# @app.route("/filter/<category>", methods=["POST","GET"])
# def filterbystudy(category):
#     study_todo = TodoModel.query.get(category)
#     return render_template('index.html', todo_list=study_todo)


if __name__ == "__main__":
    app.run(host="192.168.68.111", port=5000, debug=True)


# <!--                    {% if todo.task_status%} checked {%endif%}-->