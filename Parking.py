from flask import Flask, request, render_template
import Util
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


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

"""
@app.route('/index')
def index():
    if 'username' in session:
        return 'Logged in as %s' % session.get('username')  # 应该调转到相应的界面去

    return render_template('index.html')


@app.route('/login')
def login():
    session['username'] = 123         # get data from form
    return render_template('home00.html')


@app.route('/register')      # 注册完之后重新回到主页
def register():
    return render_template('home01.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    redirect('/')


@app.route('/reserve')
def reserve():
    return render_template('reserve.html')


@app.route('/pad1')
def select_by_custom():
    return render_template('pad1.html')


@app.errorhandler(404)             # 扑捉错误并作出响应
def page_not_found(error):
    return render_template('page_not_found.html'), 404   # 告诉 Flask，该页的错误代码是 404 ，即没有找到。默认为 200
"""


if __name__ == '__main__':
    app.run(debug=True)
