from flask import *
import mysql.connector
app = Flask(__name__)
class Employee:
    def __init__(self,name,age):
        self.name = name
        self.age = age
@app.route("/",methods = ["GET","POST"])
def login():
    
    return render_template("login.html",e = e)
app.run(debug = True,host = "0.0.0.0")