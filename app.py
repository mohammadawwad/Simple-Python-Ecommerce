from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#prevents bug as the database tables wont be created first without this code
@app.before_first_request
def create_tables():
    db.create_all()

class Todo(db.Model):
    #creating DB data set in columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("index.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():

    #creating new task
    new_title = request.form.get("title")
    new_todo = Todo(title=new_title, complete=False) 

    #adding the new data entry into the database
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):

    #updating based on ID
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete

    #updating the database
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):

    #deleting the task based on the ID
    todo = Todo.query.filter_by(id=todo_id).first()

    #updating the database to delete the entry
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)