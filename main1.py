import os
import sqlalchemy
from sqlalchemy import create_engine,Table,Column,String,Integer,ForeignKey,select
from sqlalchemy.orm import declarative_base, relationship
from flask import Flask, render_template, request, url_for, redirect,session
from sqlalchemy.orm import sessionmaker
import sqlite3
from sqlite3 import Error as err



app = Flask(__name__)
app.secret_key = "super secret key"

Base = declarative_base()
class User(Base):
    __tablename__ = "Users"
    user_id =  Column(Integer, autoincrement=True, primary_key=True)
    username =  Column(String, unique=True, nullable=False)
    email =  Column(String, unique=True)
    password =  Column(String, nullable=False)
    actByUser =  relationship("Activity", secondary="Tracker")

class Activity(Base):
    __tablename__ = "Activity"
    act_id =  Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    actname =  Column(String, unique=True)
    user_act =  relationship("User", secondary="Tracker")

class Track(Base):
    __tablename__="Tracker"
    user_id =  Column( Integer,  ForeignKey("Users.user_id"), primary_key=True, nullable=False)
    act_name =  Column( String,  ForeignKey("Activity.actname"), primary_key=True, nullable=False)

#conn = sqlite3.connect("QuantifiedSelf.db")

#engine = create_engine("sqlite:///QuantifiedSelf.db")
#session=Session(engine)

@app.route("/", methods = ["GET", "POST"])
def Login(msg="Welcome to Quantified Self Track app"):
    return render_template("login.html", msg = msg)
    #elif request.method == 'POST':
     #   username = request.form["user_name"]
     #   return render_template("home.html", username= username)

@app.route("/signup", methods=["GET", "POST"])
def Sign_up():
    return render_template("signup.html")
    
curr = conn.cursor()
@app.route("/log", methods=["GET","POST"])
def log_fun():
    msg=""
    if request.method=="POST":
        user_name = request.form['user_name']
        pswrd = request.form['password']

        #querying the database for an entry with given username and password
        
        #inst = session.query(User).filter(User.username==user_name, User.password==pswrd)
        curr.execute("select * from users where username = %s and password = %s",(user_name,pswrd))
        inst = curr.fetchone()
        if inst:
            session['loggedin']=True
            session['username']=inst[1]
            return redirect(url_for('home'))
        else:
            msg = "Incorrect username/password"
    return render_template('login.html', msg=msg)

        #cursor.execute("Select * from user where username=%s and password=%s".format(username, password))

@app.route("/home")
def home():
    return render_template("home.html", username="DEVANSH")


if __name__ == "__main__":
    #run the flask app
    app.run(
        host = "0.0.0.0",
        debug=True,
        port = 8080)