from flask import Flask,request,url_for,render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///QuantifiedSelf.db"
db= SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "Users"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email =   db.Column(db.String, unique=True)
    password =   db.Column(db.String, nullable=False)
    #actByUser =  db.relationship("Activity", secondary="Tracker")

class Activity(db.Model):
    __tablename__ = "Activity"
    act_id =   db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    actname =   db.Column(db.String, unique=True)
    #user_act =  db.relationship("User", secondary="Tracker")

class Track(db.Model):
    __tablename__="Track"
    track_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username =   db.Column( db.String,  db.ForeignKey("Users.username"), nullable=False)
    act =   db.Column( db.String, nullable=False)
    value = db.Column( db.String, nullable=False)

engine = create_engine("sqlite:///QuantifiedSelf.db")
session = Session(engine)

@app.route("/", methods = ["GET", "POST"])
def Login(msg=""):
    return render_template("login.html", msg = msg)

@app.route("/signup", methods=["GET", "POST"])
def Sign_up():
    if (request.method=="POST"):
        username=request.form.get("user_name")
        email = request.form.get("email")
        #dob = request.form.get("dob")
        password = request.form.get("password")
        entry = User(username=username, email=email, password=password)
        db.session.add(entry)
        db.session.commit()
    return render_template("signup.html")

@app.route("/log", methods=["GET","POST"])
def log_fun():
    msg=""
    if request.method=="POST":
        user_name = request.form['user_name']
        pswrd = request.form['password']

        #querying the database for an entry with given username and password
        
        inst = session.query(User).filter(User.username==user_name, User.password==pswrd).first()
        
        if inst:
            #session['loggedin']=True
            #session['username']=inst[1]
            return render_template("home.html", username = user_name)
        else:
            msg = "Incorrect username/password"
    return render_template('login.html', msg=msg)

@app.route("/home")
def home():
    return render_template("home.html", username="back")

@app.route("/location", methods=['GET', 'POST'])
def location():
    if request.method=="POST":
        username = request.form['username']
        location = request.form['location']
        #dt = datetime.now()
        entry = Track(username=username, act="location", value=location)
        db.session.add(entry)
        db.session.commit()

    return render_template("location.html")

@app.route("/mood", methods=['GET', 'POST'])
def mood():
    if request.method=="POST":
        username = request.form['username']
        mood = request.form['mood']
        #dt = datetime.now()
        entry = Track(username=username, act="mood", value=mood)
        db.session.add(entry)
        db.session.commit()

    return render_template("mood.html")

@app.route("/height", methods=['GET', 'POST'])
def height():
    if request.method=="POST":
        username = request.form['username']
        height = request.form['height']
        #dt = datetime.now()
        entry = Track(username=username, act="height", value=height)
        db.session.add(entry)
        db.session.commit()

    return render_template("height.html")

@app.route("/weight", methods=['GET', 'POST'])
def weight():
    if request.method=="POST":
        username = request.form['username']
        weight = request.form['weight']
        #dt = datetime.now()
        entry = Track(username=username, act="weight", value=weight)
        db.session.add(entry)
        db.session.commit()

    return render_template("weight.html")

@app.route("/pulse", methods=['GET', 'POST'])
def pulse():
    if request.method=="POST":
        username = request.form['username']
        pulse = request.form['pulse']
        #dt = datetime.now()
        entry = Track(username=username, act="pulse", value=pulse)
        db.session.add(entry)
        db.session.commit()

    return render_template("pulse.html")

@app.route("/temp", methods=['GET', 'POST'])
def temp():
    if request.method=="POST":
        username = request.form['username']
        temp = request.form['temp']
        #dt = datetime.now()
        entry = Track(username=username, act="temperature", value=temp)
        db.session.add(entry)
        db.session.commit()

    return render_template("temp.html")

if __name__ == "__main__":
    #run the flask app
    app.run(
        host = "0.0.0.0",
        debug=True,
        port = 8080)