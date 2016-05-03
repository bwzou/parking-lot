# --coding:utf8--
from flask import Flask, request, render_template, session, redirect
import Util
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    result = Util.user_register(
        request.form["registUsername"],
        request.form["registEmail"],
        request.form["registUsername"],
        request.form["registPassword"])
    if result == "success":
        return render_template('home01.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=["POST"])
def login():
    """  check ording"""
    phone = request.form.get('inputPhoneNumber')
    password = request.form.get('inputPassword')
    result = Util.user_login(phone, password)
    if result == "success":
        session['username'] = phone                     # 添加到session
        return render_template('home00.html')
    else:
        return render_template('index.html')


@app.route('/reserve')
def reserve():
    """ information about book"""
    return render_template('reserve.html')


@app.route('/customer_index')
def customer_index():
    pass


@app.route('/logout')
def logout():
    session.pop('username', None)
    redirect('/')


@app.errorhandler(404)             # 扑捉错误并作出响应
def page_not_found(error):
    return render_template('page_not_found.html'), 404   # 告诉 Flask，该页的错误代码是 404 ，即没有找到。默认为 200


if __name__ == '__main__':
    app.run(debug=True)
