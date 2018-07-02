import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

# enlace a base de datos vía sqlalchemy
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "student.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

# modelado
class Student(db.Model):
    """
    """
    idStudent = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombreStudent = db.Column(db.String(80), unique=True, nullable=False)
    apellidoStudent = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return "<Nombre: {}>".format(self.nombreStudent)

# vistas
# @app.route("/")
@app.route("/", methods=["GET", "POST"])
def home():
    # return "My flask app"
    if request.form:
        print(request.form)
        student = Student(nombreStudent=request.form.get("name"),apellidoStudent=request.form.get("lastname"))
        db.session.add(student)
        db.session.commit()
        return redirect("/")
        
    estudiantes = Student.query.all()
    return render_template("home.html", estudiantes = estudiantes)
    # return render_template("home.html")
    
@app.route("/update", methods=["POST"])
def update():
    idestudent = request.form.get("idestudent")
    newname = request.form.get("newname")
    newlastname = request.form.get("newlastname")
    student = Student.query.get(idestudent)
    student.nombreStudent = newname
    student.apellidoStudent = newlastname
    db.session.commit()
    return redirect("/")  

@app.route("/delete", methods=["POST"])
def delete():
    idestudent = request.form.get("idestudent")
    student = Student.query.get(idestudent)
    db.session.delete(student)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)



