from flask import Flask, render_template, request, redirect
#Flask is a module of python,which provides functionality to create web apps
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

  

app = Flask(__name__)     #frst two lines are used for intialization
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method== 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template('index.html',allTodo=allTodo)
         #render is used in return
  

@app.route("/show") #to move different endpoints(pages)
def products():
    allTodo = Todo.query.all()
    print(allTodo)          # to display todo in terminal
    return 'Products page!'  

@app.route("/update/<int:sno>", methods=['GET', 'POST'])  # Update todo
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()  # Find the Todo item by sno
    if request.method == 'POST':
        # Update the existing todo
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()  # Commit the changes
        return redirect('/')  # Redirect to home page after update

    return render_template('update.html', todo=todo)  # Pass the todo to pre-fill the form


@app.route("/delete/<int:sno>") #to move different endpoints(pages)
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)    #line 15 and 16 is used to run the file