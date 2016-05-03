# --coding:utf8--
from flask import Flask, request, render_template, session, redirect
import Util
import datetime
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
        return redirect('home')
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
        return redirect('home')
    else:
        return render_template('index.html')


@app.route('/home')
def home():
    result = Util.diplay_book(session["username"])
    if result is None:
        return render_template('home00.html')
    else:
        return render_template('home01.html', result=result)
    pass


@app.route('/reserve')
def display_reserve():
    """ information about book"""
    return render_template('reserve.html')


@app.route('/reserver', methods=["POST", "GET"])
def reserve():
    if request.method == "POST":
        Time = request.form['slider_value']
        beginTime, endTime = Time[6:11], Time[16:21]

        temp = request.form["picker"] + "/" + beginTime
        beginTime = datetime.datetime.strptime(temp, '%d/%m/%Y/%H:%M')
        temp = request.form["picker"] + "/" + endTime
        endTime = datetime.datetime.strptime(temp, '%d/%m/%Y/%H:%M')

        Book = Util.Booking(Name=session["username"],
                            StartTime=beginTime,
                            EndTime=endTime,
                            PlateNumber=request.form["plate"])
        result = Book.book()
        if result == "success":
            return redirect('reserve')
        else:
            return result
    else:
        return redirect('reserve')


@app.route('/customer_index')
def customer_index():
    pass


@app.route('/logout')
def logout():
    session.pop('username', None)
    redirect('/')


@app.errorhandler(404)             # 扑捉错误并作出响应
def page_not_found(error):
    return render_template('page_not_found.html'), 404
    # 告诉 Flask，该页的错误代码是 404 ，即没有找到。默认为 200


if __name__ == '__main__':
    app.run(debug=True)
