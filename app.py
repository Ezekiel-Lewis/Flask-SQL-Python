from flask import Flask, render_template, request, redirect, url_for #looking for template directory
from flask_sqlalchemy import SQLAlchemy #saves todo items to library for handling database
#SQLAlchemy is a library that facilitates the communication between Python programs and databases.
app2 = Flask(__name__)
app2.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #Name of path to DB, relative path, advs this was dict, used brackets
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app2)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #structuring DB, creating a unique value for each todo item
    title = db.Column(db.String(100)) #string must not exceed 100 char
    complete = db.Column(db.Boolean)
@app2.route('/')
def index(): #prints todo list
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)
@app2.route("/add", methods=["POST"]) #Queries db to get this item
def add():
    #adds new item
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo) #add list item to DB
    db.session.commit()
    return redirect(url_for("index")) # redirects user to index
@app2.route("/update/<int:todo_id>")
def update(todo_id):
    #updates new item
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))
@app2.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))
if __name__ == "__main__":
    db.create_all() #creates database file
    app2.run(debug=True)