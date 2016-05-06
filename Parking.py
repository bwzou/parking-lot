# --coding:utf8--
from flask import Flask, request, render_template, session,\
    redirect, flash
import datetime
import Util

app = Flask(__name__)
app.secret_key = 'A0Zr98KK/WDW3A/3yX R~XHH!jmN]LWX/,?RT'


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
        return render_template('home01.html', data=None, history=None)
    elif result == "exist":
        flash(u'Username is used, please try another', 'error')  # 用户名已经被使用
        return render_template('index.html')


@app.route('/login', methods=["POST"])
def login():
    """  check ording"""
    phone = request.form.get('inputPhoneNumber')
    password = request.form.get('inputPassword')
    result = Util.user_login(phone, password)
    if result == "success":
        session['username'] = phone                     # 添加到session
        data, history = Util.Booking.diplay_book(session["username"])
        # data, history = Util.divide_data(data)
        return render_template('home01.html', data=data, history=history)
    else:
        flash(u'Invalid password or username provided', 'error')        # 消息错误提示
        return render_template('index.html')


@app.route('/reserve')
def reserve():
    """ information about book"""

    flash(u'Sorry! There is no a Parkinglot available now', 'error')  # 消息错误提示
    return render_template('reserve.html')


@app.route('/reserver', methods=["POST", "GET"])
def reserver():
    if request.method == "POST":
        Time = request.form['slider_value']
        beginTime, endTime = Time[6:11], Time[16:21]

        temp = request.form["picker"] + "/" + beginTime
        beginTime = datetime.datetime.strptime(temp, '%m/%d/%Y/%H:%M')
        temp = request.form["picker"] + "/" + endTime
        endTime = datetime.datetime.strptime(temp, '%m/%d/%Y/%H:%M')

        Book = Util.Booking(Name=session["username"],
                            StartTime=beginTime,
                            EndTime=endTime,
                            PlateNumber=request.form["plate"])
        result = Book.book()
        if result == "success":
            return redirect('/customer_index')
        else:
            return result
    else:
        return redirect('/customer_index')


@app.route('/changereserve/<ID>', methods=["POST", "GET"])
def changereserve(ID):
    result = Util.Booking.query_book(ID)
    print result.StartTime
    print result.EndTime
    if result is not None:
        result = Util.change_bookto(result)
    return render_template('reserve.html', result=result)


@app.route('/change/<Id>', methods=["POST", "GET"])
def change(Id):
    if request.method == "POST":
        Time = request.form['slider_value']
        beginTime, endTime = Time[6:11], Time[16:21]
        print beginTime
        print endTime

        temp = request.form["picker"] + "/" + beginTime
        beginTime = datetime.datetime.strptime(temp, '%m/%d/%Y/%H:%M')
        temp = request.form["picker"] + "/" + endTime
        endTime = datetime.datetime.strptime(temp, '%m/%d/%Y/%H:%M')

        Book = Util.Booking(ID=Id,
                            Name=session["username"],
                            StartTime=beginTime,
                            EndTime=endTime,
                            PlateNumber=request.form["plate"])
        result = Book.alter_book()
        if result == "success":
            return redirect('/customer_index')
        else:
            return result


@app.route('/cancelreserve/<ID>', methods=["POST", "GET"])
def cancelreserve(ID):
    result = Util.Booking.cancel_book(ID)
    if result == "success":
        return redirect('/customer_index')
    else:
        return result


@app.route('/customer_index')
def customer_index():
    data, history = Util.Booking.diplay_book(session["username"])
    return render_template('home01.html', data=data, history=history)
    # 根据data判断如何显示


@app.route('/logout')
def logout():
    session.pop('username', None)
    redirect('/')


@app.route('/get_lot')
def get_lot():
    pass


@app.errorhandler(404)             # 扑捉错误并作出响应
def page_not_found(error):
    return render_template('page_not_found.html'), 404
    # 告诉 Flask，该页的错误代码是 404 ，即没有找到。默认为 200


@app.errorhandler(500)
def internal_error(error):
    # db.session .rollback()    考虑数据库可能处于不正常的状态
    return render_template('internal_error.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
