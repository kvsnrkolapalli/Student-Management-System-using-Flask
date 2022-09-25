from email.policy import default
from flask import Flask, render_template , request
from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///stm.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    rno=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False)
    gender=db.Column(db.String(20),nullable=False)
    contact=db.Column(db.Integer,nullable=False)
    dob=db.Column(db.String(50),nullable=False)
    address=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow())
    
    def __repr__(self)->str:   
        return f"{self.rno} {self.name} {self.email} {self.gender} {self.contact} {self.dob} {self.address}"

@app.route("/", methods=["GET", "POST"])
def hello_world():
    view_all =Student.query.all()
    return render_template("index.html",view_all=view_all)

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")

@app.route("/add", methods=["GET", "POST"])
def add_student():
    already="add"
    if request.method == 'POST':
        rno=request.form['rno']
        name=request.form['name']
        email=request.form['email']
        gender=request.form['gender']
        contact=request.form['contact']
        dob=request.form['dob']
        address=request.form['address']
        already =Student.query.filter_by(rno=rno).first()
        if already==None:
            data=Student(rno=rno,name=name,email=email,gender=gender,contact=contact,dob=dob,address=address,date_created=datetime.utcnow())
            db.session.add(data)
            db.session.commit()
        else:
            already="Already Exists"
        return render_template("add.html",already=already)
    return render_template("add.html",already=already)

@app.route("/view", methods=["GET", "POST"])
def view_student():
    view_all =Student.query.all()
    return render_template("view.html",view_all=view_all)

@app.route("/search_view", methods=["GET", "POST"])
def sview_student():
    if request.method == 'POST':
        rno=request.form['search_rno']
        view_all =Student.query.filter_by(rno=rno).all()
        return render_template("view.html",view_all=view_all)
        
@app.route("/update/<int:rno>", methods=["GET", "POST"])
def update_student(rno):
    if request.method == 'POST':
        u=Student.query.filter_by(rno=rno).first()
        rno=u.rno
        name=request.form['name']
        email=request.form['email']
        gender=request.form['gender']
        contact=request.form['contact']
        dob=request.form['dob']
        address=request.form['address']
        date_created=u.date_created
        db.session.delete(u)
        db.session.commit()
        data=Student(rno=rno,name=name,email=email,gender=gender,contact=contact,dob=dob,address=address,date_created=date_created)
        db.session.add(data)
        db.session.commit()
        view_all =Student.query.filter_by(rno=rno).all()
        return render_template("uview.html",view_all=view_all)
    update_=Student.query.filter_by(rno=rno).first()
    return render_template("update.html",update_=update_)

@app.route("/delete/<int:rno>")
def delete_student(rno):
    del_student =Student.query.filter_by(rno=rno).first()
    db.session.delete(del_student)
    db.session.commit()
    return redirect("/view")


if __name__ == "__main__":
    app.run(debug=True,port=1412) 