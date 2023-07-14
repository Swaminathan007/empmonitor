from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
import mysql.connector
from datetime import datetime,date
app = Flask(__name__)
app.secret_key = '12345678' 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


mydb = mysql.connector.connect(host = "database-1.clrbethb6kqw.ap-south-1.rds.amazonaws.com",
                               username="root",password = "12345678",port=3306,database="emp")

tasks = []
cursor = mydb.cursor()
def findob(date):
    date = str(date).split("-")[::-1]
    dob = ""
    for i in date:
        dob+=i
    return dob
class User(UserMixin):
    def __init__(self, name, dob,dept,sex,id,tzd):
        self.name = name
        self.dob = dob
        self.dept = dept
        self.sex = sex
        self.id = id
        self.tzd = tzd
        self.age = datetime.now().year - int(self.dob[4:]) 
class Task(UserMixin):
    def __init__(self,task,completed):
        self.task = task 
        self.completed = completed
@login_manager.user_loader
def load_user(user_id):
    cursor.execute(f"select timezone from timezonetable where emp_id = {user_id}")
    td = cursor.fetchone()
    cursor.execute(f'SELECT * FROM employeetable WHERE emp_id = {user_id}')
    user = cursor.fetchone()

    
    
    if user is None:
        return None
    
    return User(user[0],findob(user[6]),user[3],user[4],user[1],td[0])
@app.route("/",methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['dob']
        tzd = request.form['tzd']
        
        cursor.execute(f"insert into timezonetable values({int(id)},'{tzd}','{datetime.today().date()}')")
        mydb.commit()
        
        cursor.execute(f"select * from employeetable where emp_id = {id}")
        user = cursor.fetchone()
        dob = findob(user[6])
        
        if user and password == dob:
            user = User(user[0],dob,user[3],user[4],user[1],tzd)
            login_user(user)
            flash("Signed in successfully")
            return redirect('/welcome')
        else:
            flash('Invalid username or password', 'error')
    return render_template("login.html")
@app.route("/welcome")
@login_required
def welcome():
    cursor.execute(f"select task,compornot,taskid from addtask where emp_id={current_user.id}")
    tasks = cursor.fetchall()
    return render_template('welcome.html', user=current_user,tasks = tasks)
@login_required
@app.route("/addtask",methods = ["GET","POST"])
def addtask():
    if(request.method == "POST"):
        task = request.form["task"]
        cursor.execute(f"insert into addtask(emp_id,task,compornot,tod_date) values({current_user.id},'{task}',{False},'{datetime.today().date()}')")
        mydb.commit()
        flash("Task added successfully")
        return redirect("/welcome")
@login_required
@app.route("/profile")
def profile():
    return render_template("profile.html",user = current_user)
@app.route('/logout')
@login_required
def logout():
    cursor.execute(f"delete from timezonetable where emp_id = {current_user.id}")
    mydb.commit()
    logout_user()
    
    return redirect('/')
app.run(debug = True,host = "0.0.0.0")