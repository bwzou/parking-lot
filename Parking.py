from flask import Flask, request, render_template
import Util

app = Flask(__name__)


@app.before_request
def before_request():
    """  global status  name cookie bookinglist"""
    pass


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    result = Util.user_register(
        request.form["registUsername"],
        request.form["registEmail"],
        "110120",
        request.form["registPassword"])
    if result == "success":
        return render_template('home01.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=["POST"])
def login():
    """  check ording"""
    email = request.form.get('inputEmail')
    password = request.form.get('inputPassword')
    result = Util.user_login(email, password)
    if result == "success":
        return render_template('home00.html')
    else:
        return render_template('index.html')


@app.route('/reserve')
def reserve():
    """ information about book"""
    return render_template('reserve.html')


@app.route('/pad1')
def pad1():
    return render_template('pad1.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/pad2')
def pad2():
    return render_template('pad2.html')


if __name__ == '__main__':
    app.run()
