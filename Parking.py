from flask import Flask ,render_template
from flask import request
from  database import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/index')
def index():

    return render_template('index.html')

@app.route('/login',methods=["POST"])
def login():
    myform=request.form
    email=myform.get('inputEmail')
    password=myform.get('inputPassword')
    result=user_login(email,password)
    if result=="success":
        return  render_template('login.html')
    else:
        return  render_template('index.html')

@app.route('/register',methods=["POST"])
def register():
    registerForm=request.form
    email=registerForm.get('email')
    username=registerForm.get('username')
    password=registerForm.get('password')
    result=user_register(username,email,"110120",password)
    return result
if __name__ == '__main__':
    app.run(debug=True)
