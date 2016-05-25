# --coding:utf8--
import Manage

from blue_customer.blue_customer import blue_customer
from blue_manager.blue_manager import blue_manager
from RedisQueue import RedisQueue
from flask import Flask, request, render_template, session,\
    redirect, flash, make_response
from globle import Temp

app = Flask(__name__)
app.secret_key = 'A0Zr98KK/WDW3A/3yX R~XHH!jmN]LWX/,?RT'
app.config['REDIS_QUEUE_KEY'] = 'my_queue'

app.register_blueprint(blue_customer)   # 注册蓝图,可以多次注册
app.register_blueprint(blue_customer, url_prefix='/customer')
app.register_blueprint(blue_manager)
app.register_blueprint(blue_manager, url_prefix='/manager')

queue = RedisQueue(app.config['REDIS_QUEUE_KEY'])        # 根据Redis生成queue


# ------------------------用户登录注册--------------------------------------------
@app.route('/')
def hello_world():
    if request.cookies.get('username') is not None:
        return redirect('quick')
    # app.make_response(redirect('quick'))
    return render_template('index.html')


@app.route('/quick')
def quick():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if username is None or password is None:
        return render_template('index.html')
    result = Manage.user_login(username, password)
    if result == "success":
        session['username'] = username                     # 添加到session
        repr = make_response(redirect('customer_index'))
        repr.set_cookie('username', username, 1800)
        repr.set_cookie('password', password, 1800)
        return repr
    else:
        flash(u'Invalid password or username provided', 'error')        # 消息错误提示
        return render_template('index.html')


@app.route('/index')
def index():
    if request.cookies.get('username') is not None:
        return redirect('quick')
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    result = Manage.user_register(
        request.form["registUsername"],
        request.form["registEmail"],
        request.form["registUsername"],
        request.form["registPassword"])
    if result == "success":
        return render_template('blue_customer/templates/home01.html', data=None, history=None)
    elif result == "exist":
        flash(u'Username is used, please try another', 'error')  # 用户名已经被使用
        return render_template('index.html')


@app.route('/login', methods=["POST"])
def login():
    """  check ording"""

    phone = request.form.get('inputPhoneNumber')
    password = request.form.get('inputPassword')
    result = Manage.user_login(phone, password)
    if result == "success":
        session['username'] = phone                     # 添加到session
        repr = make_response(redirect('customer_index'))
        repr.set_cookie('username', phone, 1800)
        repr.set_cookie('password', password, 1800)
        return repr
    else:
        flash(u'Invalid password or username provided', 'error')        # 消息错误提示
        return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')


# ---------------------------获取停车位信息--------------------------------------
@app.route('/lot')
def lot():
    return render_template('pad1.html')


@app.route('/getlotname', methods=["POST", "GET"])
def getlotname():
    if request.method == "POST":
        order_number = request.form['inputNumber']
        plate_number = request.form['inputLicenseNumber']
        print order_number
        print plate_number
        if order_number == "" and plate_number == "":
            flash(u'you must input either of blanks', 'error')  # 消息错误提示)
            return render_template('pad1.html')
        else:
            if order_number != "":
                result = Manage.Reservation.query_book(order_number)
                if result:
                    Manage.set_lot_status(result.PID)
                else:
                    flash(u'The order number is not existing,please try again ', 'error')  # 消息错误提示)
                    return render_template('pad1.html')
            else:
                result = Manage.Reservation.query_book_by_plate(plate_number)
                # plate_number不是唯一，这里要修正
                if result:
                    Manage.set_lot_status(result.PID)
                else:
                    flash(u'The plate number is not existing,please try again ', 'error')  # 消息错误提示)
                    return render_template('pad1.html')

        print result.PayStatus
        if result.PayStatus == '0':
            flash(u'No Pay ', 'error')  # 消息错误提示)
            return render_template('pad1.html')
        number = result.insert_parktime()

        if number == 0:
            flash(u'15 minues ago ', 'error')  # 消息错误提示)
            return render_template('pad1.html')
        elif number == 1:
            flash(u'30 minutes behind ', 'error')  # 消息错误提示)
            return render_template('pad1.html')
        elif number == 3:
            flash(u'car is already there ', 'error')  # 消息错误提示)
            return render_template('pad1.html')
        else:
            return render_template('pad2.html', result=result)

    return render_template('pad2.html', result=None)


@app.route('/leave', methods=["POST", "GET"])
def leave():
    if request.method == "POST":
        order_number = request.form['inputNumber2']
        plate_number = request.form['inputLicenseNumber2']
        if order_number == "" and plate_number == "":
            return redirect('/lot')
        else:
            if order_number != "":
                result = Manage.Reservation.query_book(order_number)
                if result:
                    Manage.set_lot_status_idle(result.PID)    # 开后设置车位状态有问题
            else:
                result = Manage.Reservation.query_book_by_plate(plate_number)
                # plate_number不是唯一，这里要修正
                if result:
                    Manage.set_lot_status_idle(result.PID)
            min = result.insert_leavetime()
            if min == 0:
                return "car is not here"
            elif min == 1:
                return "car has left"
            else:
                result.query_money()
                TotalMoney = int(result.Price) + int(result.overpay)
                Temp.TempCharge = result
                return render_template('leave.html', result=result, Total=TotalMoney)
    else:
        return render_template('leave.html')


# ---------------------------系统错误处理----------------------------------------
@app.errorhandler(404)                # 扑捉错误并作出响应
def page_not_found(error):
    # 告诉 Flask，该页的错误代码是 404 ，即没有找到。默认为 200
    return render_template('page_not_found.html'), 404


@app.errorhandler(500)
def internal_error(error):
    # db.session .rollback()    考虑数据库可能处于不正常的状态
    return render_template('internal_error.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
