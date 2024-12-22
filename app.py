from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Todo model


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=False)

# Route for home page


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

# Route for adding a To-Do


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

# Route for updating a To-Do's completion status


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))

# Route for deleting a To-Do


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update_title/<int:todo_id>", methods=["GET", "POST"])
def update_title(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if request.method == "POST":
        new_title = request.form.get("title")
        if todo and new_title:
            todo.title = new_title
            db.session.commit()
            return redirect(url_for("home"))
        else:
            return "Invalid Input", 400
    return render_template("update_title.html", todo=todo)


@app.route("/delete_all", methods=["GET"])
def delete_all():
    Todo.query.delete()  # Deletes all rows in the Todo table
    db.session.commit()
    return redirect(url_for("home"))


# Initialize database and run app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the database tables within the application context
    app.run(debug=True)
