from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from datetime import datetime
#defining app and database
app = Flask(__name__)
app.secret_key = '12345678' 
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:12345678@database-1.clrbethb6kqw.ap-south-1.rds.amazonaws.com:3306/emp'
database = SQLAlchemy(app)
#defining login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
#Employee class 
class Employee(database.Model ,UserMixin):
    __tablename__ = "employeetable"
    name = database.Column(database.String)
    emp_id = database.Column(database.Integer,primary_key = True)
    dept_id = database.Column(database.Integer)
    dept_name = database.Column(database.String)
    gender = database.Column(database.String)
    age = database.Column(database.Integer)
    dob = database.Column(database.Date)
    
    def get_id(self):
        return self.emp_id
#Timezone in which the employee is logging in
class Timezone(database.Model):
    __tablename__ = "timezonetable"
    emp_id = database.Column(database.Integer,database.ForeignKey(Employee.emp_id),primary_key = True)
    timezone = database.Column(database.String)
    today_date = database.Column(database.Date)
    def __init__(self,id,tz,td):
        self.emp_id = id
        self.timezone = tz
        self.today_date = td
#Login and out time of employee
class InOut(database.Model):
    __tablename__ = "inouttable"
    emp_id = database.Column(database.Integer,database.ForeignKey(Employee.emp_id),primary_key = True)
    login_time = database.Column(database.Time)
    logout_time = database.Column(database.Time,nullable = True)
    currentdate = database.Column(database.Date)
    def __init__(self,id,lint,dt):
        self.emp_id = id
        self.login_time = lint
        self.logout_time = None
        self.currentdate = dt
#Day to day task of the employee
class Task(database.Model):
    __tablename__ = "addtask"
    emp_id = database.Column(database.Integer,database.ForeignKey(Employee.emp_id))
    task = database.Column(database.String)
    compornot = database.Column(database.Boolean)
    tod_date = database.Column(database.Date)
    taskid = database.Column(database.Integer,primary_key=True,auto_increment = True)
    def __init__(self,id,task,td):
        self.emp_id = id
        self.task = task
        self.compornot = False
        self.tod_date = td
def findob(date):
    date = str(date).split("-")[::-1]
    dob = ""
    for i in date:
        dob+=i
    return dob

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(user_id)

@app.route("/",methods = ["GET","POST"])
def home():
    if(request.method == "POST"):
        id = request.form['id']
        password = request.form['dob'] 
        timezone = request.form["tzd"]
        emp = Employee.query.filter_by(emp_id = int(id)).first()
        dob = database.session.query(Employee.dob).filter_by(emp_id = int(id)).first()
        
        tzd = Timezone(id=id,tz=timezone,td=datetime.now().date())
        InTime = InOut(id=id,lint=datetime.now().time(),dt = datetime.now().date())
        
        database.session.add(tzd)
        database.session.commit()
        database.session.add(InTime)
        database.session.commit()
        
        if emp and password == findob(str(dob[0])):
            login_user(emp)
            flash("Signed in successfully")
            return redirect("/welcome")
        else:
            flash("Invalid username or password")
    return render_template("login.html")

@app.route("/welcome")
@login_required
def welcome():
    emp = Employee.query.filter_by(emp_id = int(current_user.emp_id)).first()
    tasks = Task.query.filter_by(emp_id = int(current_user.emp_id),tod_date = datetime.now().date())
    return render_template('welcome.html', user=emp,tasks=list(tasks))
@login_required
@app.route("/addtask",methods = ["GET","POST"])
def addtask():
    if(request.method == "POST"):
        task = request.form["task"]
        task_to_be_added = Task(id=current_user.emp_id,task=task,td=datetime.now().date())
        database.session.add(task_to_be_added)
        database.session.commit()
        flash("Task added successfully")
        return redirect("/welcome")
@login_required
@app.route("/profile")
def profile():
    return render_template("profile.html",user = current_user)
@login_required
@app.route("/completed/<int:id>")
def complete_task(id):
    task_comp = Task.query.filter_by(taskid=id).first()
    task_comp.compornot = True
    database.session.commit()
    flash("Task completed successfully")
    return redirect("/welcome")
@app.route('/logout')
@login_required
def logout():
    emp_tz = Timezone.query.filter_by(emp_id = int(current_user.emp_id)).first()
    database.session.delete(emp_tz)
    database.session.commit()
    inout = InOut.query.filter_by(emp_id = int(current_user.emp_id),logout_time = None).first()
    inout.logout_time = datetime.now().time()
    database.session.commit()
    logout_user()
    return redirect('/')
if __name__ == "__main__":
    app.run(debug = True,host = "0.0.0.0")