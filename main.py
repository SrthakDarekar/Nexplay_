import os
from flask import Flask, render_template,request,redirect, url_for,session,flash
from tkinter import messagebox
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv()
app=Flask(__name__)

app.secret_key=os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class matches(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(50), nullable=False)
    Tournament_name = db.Column(db.String(100))
    status = db.Column(db.String(20), nullable=False, default='Upcoming')
    prize_pull = db.Column(db.Integer, nullable=False, default=0)

class user(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    Join_date = db.Column(db.DateTime, nullable=False,default=db.func.current_timestamp())

class joined1(db.Model):
    __tablename__ = 'joined'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    joined_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

@app.route('/')
def home():
    match=matches.query.all()
    return render_template('home.html', matches=match)

@app.route('/tournament')
def tournament():
    match=matches.query.all()
    return render_template('tournament.html',matches=match)

@app.route('/joined')
def joined():
    if "loggedin" in session:
        email=session.get("email")
        user_data=user.query.filter_by(email=email).first()

        joined_data=joined1.query.filter_by(user_id=user_data.id).all()

        matches_id=[]
        for j in joined_data:
            matches_id.append(j.match_id)

        match=matches.query.filter(matches.id.in_(matches_id)).all()
        return render_template("joined.html",matches=match)
    else:
        return render_template("join.html")

@app.route('/joined_tournament/<int:match_id>',methods=['GET','POST'])
def joined_tournament(match_id):
    if request.method == 'POST':
        if "loggedin" in session:
            email = session.get("email")
            user_obj = user.query.filter_by(email=email).first()

            entry_data = joined1.query.filter_by(user_id=user_obj.id, match_id=match_id).first()
            if entry_data:
                flash("You allredy participated in the Tournamnet")
                return redirect(url_for('joined'))
            else:
                status_check=matches.query.filter_by(id=match_id).first()
                if status_check.status=="Cancelled" or status_check.status=="Completed" or status_check.status=="Live":
                    flash("Please Check the status of the Torunament")
                    return redirect(url_for("tournament"))
                else:
                    joined_entry = joined1(user_id=user_obj.id, match_id=match_id)
                    db.session.add(joined_entry)
                    db.session.commit()

                    joined_data=joined1.query.filter_by(user_id=user_obj.id).all()

                    matches_id=[]
                    for j in joined_data:
                        matches_id.append(j.match_id)

                    match=matches.query.filter(matches.id.in_(matches_id)).all()

                    return render_template("joined.html",matches=match)
    else:
        return render_template("joined.html")

@app.route("/leave/<int:match_id>",methods=['GET','POST'])
def leave(match_id):
    if request.method=="POST":
        email=session.get("email")
        user_data=user.query.filter_by(email=email).first()

        joined_entry=joined1.query.filter_by(user_id=user_data.id,match_id=match_id).first()

        if joined_entry:
            db.session.delete(joined_entry)
            db.session.commit()
            flash("Your Tournament Entry Has Been Removed")
            return redirect(url_for("tournament"))
        else:
            flash("There is Some Error In the Database")
            return redirect(url_for("joined"))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        User=user.query.filter_by(email=email , password=password).first()
        if User:
            session["loggedin"]=True
            session["firstname"]=User.firstname
            session["lastname"]=User.lastname
            session["email"]=User.email
            return redirect(url_for('home'))
        else:
            flash("Account Don`t Exist Create Account To Continue")
            return redirect(url_for('join'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session["loggedin"]=None
    session["firstname"]=None
    session["lastname"]=None
    flash("You Hav Been Logged Out !")
    return redirect(url_for("join"))

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method =='POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form["password2"]
        User=user.query.filter_by(email=email).first()
        if User:
            flash("The Email Address Allredy Registerd With Another Account")
            return redirect(url_for('join'))
        else:
            new_user = user(firstname=firstname, lastname=lastname, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Your Account Has been Created Successfully Please Login To Continue , Contact If You Face Any Issue")
            return redirect(url_for('login'))


    return render_template('join.html')

if __name__=='__main__':
    app.run(debug=True)
