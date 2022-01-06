from sys import getwindowsversion
from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,LoginManager,login_manager
from flask_login import login_required,current_user
local_server=True #my db cxn
 #initialising application
app=Flask(__name__)
app.secret_key='Ajin'

#This is for getting unique user access that is for accessing particular user account
login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader   # which user getting the request
def load_user(user_id):
    return Signup.query.get(int(user_id))


#app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/database_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/python_proj'
db=SQLAlchemy(app)
#creating DB tables
class Data(db.Model):
    Name=db.Column(db.String(100))
    USN=db.Column(db.String(100),primary_key=True)
    Age=db.Column(db.Integer)

class Signup(UserMixin,db.Model):
    UQ_ID=db.Column(db.String(200),primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
    def get_id(self):
        return self.UQ_ID
class Patient_data(db.Model):
    pid=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50),nullable=False)
    Name=db.Column(db.String(50),nullable=False)
    Gender=db.Column(db.String(50),nullable=False)
    slot=db.Column(db.String(50),nullable=False)
    Symptoms=db.Column(db.String(50),nullable=False)
    Time=db.Column(db.String(50),nullable=False)
    Date=db.Column(db.String(50),nullable=False)
    Department=db.Column(db.String(50),nullable=False)
    Phone_No=db.Column(db.String(50),nullable=False)

class Doctors(db.Model):
    d_id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    Doctor_name=db.Column(db.String(50))
    Department=db.Column(db.String(50))


# Pass endppoints and run the function\
@app.route('/')
def hello_world():

    # a=Data.query.all()
    # print(a)
    # return render_template('index.html')
    return render_template('index.html')
@app.route('/doctors')
def Doctors():
    return render_template('doctors.html')


@app.route('/patients',methods=['POST','GET'])
@login_required
def patients():
    if request.method=='POST':
        email=request.form.get('email')
        Name=request.form.get('name')
        Gender=request.form.get('gender')
        slot=request.form.get('Slot')
        Symptoms=request.form.get('Symptoms')
        Time=request.form.get('Time')
        Date=request.form.get('Date')
        Department=request.form.get('dept')
        Phone_no=request.form.get('number')

        query=db.engine.execute(f"INSERT INTO patient_data(email,Name,Gender,slot,Symptoms,Time,Date,Department,Phone_No) VALUES('{email}','{Name}','{Gender}','{slot}','{Symptoms}','{Time}','{Date}','{Department}','{Phone_no}')")
        flash("Booking Confirmed","info")
        return redirect(url_for('bookings'))
    else:
        return render_template('patients.html')
    return render_template('patients.html')

@app.route('/bookings')
@login_required
def bookings():
    em=current_user.email
    query1=db.engine.execute(f"SELECT * from patient_data WHERE email='{em}'")
    return render_template('bookings.html',query=query1)


@app.route('/edit/<string:pid>',methods=['POST','GET'])
@login_required
def edit(pid):
    posts=Patient_data.query.filter_by(pid=pid).first()
    if request.method=='POST':
        email=request.form.get('email')
        Name=request.form.get('name')
        Gender=request.form.get('gender')
        slot=request.form.get('Slot')
        Symptoms=request.form.get('Symptoms')
        Time=request.form.get('Time')
        Date=request.form.get('Date')
        Department=request.form.get('dept')
        Phone_no=request.form.get('number')
        db.engine.execute(f"UPDATE patient_data SET email='{email}', Name='{Name}',Gender= '{Gender}',slot= '{slot}',Symptoms = '{Symptoms}', Time= '{Time}', Date= '{Date}', Department = '{Department}',Phone_No = '{Phone_no}' WHERE patient_data.pid = {pid}")
        flash("Slot is updated","success")
        return redirect('/bookings')
    return render_template('edit.html',posts=posts)

@app.route('/delete/<string:pid>',methods=['POST','GET'])
@login_required
def delete(pid):
    db.engine.execute(f"DELETE from patient_data where patient_data.pid={pid}")
    flash("Deleted Successfully","danger")
    return redirect('/bookings')


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        username=request.form.get('username')
        email=request.form.get('Email')
        password=request.form.get('password')
        user= Signup.query.filter_by(email=email).first()

        if user:
            flash("Email already exists","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)
        new_user=db.engine.execute(f"INSERT INTO signup (username,email,password) VALUES ('{username}','{email}','{encpassword}')")
        flash("Signup Success please login","success")
        return render_template('login.html')
    return render_template('signup.html')
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form.get('Email')
        password=request.form.get('password')
        user=Signup.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('bookings'))
        else:
            flash('User not present in registry','danger')
            return render_template('login.html')
    return render_template('login.html')
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Successful","warning")
    #The person should be logged in to access logged on function
    return redirect(url_for('login'))



@app.route('/hi')
def hello():
    return 'Hello'
   

app.run(debug=True)
