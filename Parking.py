
# --coding:utf8--
import datetime
import sys
import json

from flask import Flask, request, render_template, session,\
    redirect, flash, jsonify,url_for

import Util
from globle import gl

sys.path.append("E:\\Pycharm\\ParkingLotQQ\\build\\lib.win32-2.7")  # 请把该路径改成你项目lib.win32-2.7的路径
from ParkingAlgorithm import insert                                 # pycharm报错，但不影响

app = Flask(__name__)
app.secret_key = 'A0Zr98KK/WDW3A/3yX R~XHH!jmN]LWX/,?RT'


# ------------------------用户登录注册--------------------------------------------
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


@app.route('/customer_index')
def customer_index():
    data, history = Util.Booking.diplay_book(session["username"])
    return render_template('home01.html', data=data, history=history)
    # 根据data判断如何显示


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')


# ------------------------用户预定和修改订单--------------------------------------------
@app.route('/reserve')
def reserve():
    """ information about book"""
    # flash(u'Sorry! There is no a Parkinglot available now', 'error')  # 消息错误提示
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

        """ we should ascertain whether there is a lot available """
        orders, begin, sustain = Util.all_lot(beginTime, endTime)
        if len(orders) == 0:
            Book = Util.Booking(PID='A101',
                                Name=session["username"],
                                StartTime=beginTime,
                                EndTime=endTime,
                                PlateNumber=request.form["plate"],
                                Price=sustain)
        else:
            mov_dict = insert(orders, gl.Lots_len, begin, sustain)
            print mov_dict
            dict_len = len(mov_dict)
            if dict_len == 0:             # 如果没有可以用返回[]
                flash(u'Sorry! There is no a Parkinglot available now', 'error')  # 消息错误提示
                return render_template('reserve.html')
            for i in range(dict_len):
                if i == 0:
                    Book = Util.Booking(PID=gl.dict1[mov_dict[0].get('to')],
                                        Name=session["username"],
                                        StartTime=beginTime,
                                        EndTime=endTime,
                                        PlateNumber=request.form["plate"],
                                        Price=sustain)
                else:
                    Util.Booking.update_Lot(mov_dict[i].get('to'), mov_dict[i].get('id'))

        result = Book.book()
        if result == "success":
            return redirect('/customer_index')
        else:
            flash(u'failed to summit the order,please try again', 'error')  # 消息错误提示
            return render_template('reserve.html')
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

        temp = request.form["picker"] + "/" + beginTime
        beginTime = datetime.datetime.strptime(temp, '%m/%d/%Y/%H:%M')
        temp = request.form["picker"] + "/" + endTime
        endTime = datetime.datetime.strptime(temp, '%m/%d/%Y/%H:%M')

        print "change"
        print beginTime
        print endTime

        """ we should ascertain whether there is a lot available """
        orders, begin, sustain = Util.all_lot(beginTime, endTime)
        if len(orders) == 0:
            Book = Util.Booking(ID=Id,
                                PID='A101',
                                Name=session["username"],
                                StartTime=beginTime,
                                EndTime=endTime,
                                PlateNumber=request.form["plate"],
                                Price=sustain)              # 根据sustain来计费
        else:
            mov_dict = insert(orders, gl.Lots_len, begin, sustain)
            print mov_dict
            dict_len = len(mov_dict)
            if dict_len == 0:  # 如果没有可以用返回[],此时可以给予提示
                flash(u'Sorry! There is no a Parkinglot available now,failed to alter order', 'error')  # 消息错误提示
                return render_template('reserve.html')
            for i in range(dict_len):
                if i == 0:
                    Book = Util.Booking(ID=Id,
                                        PID=gl.dict1[mov_dict[0].get('to')],
                                        Name=session["username"],
                                        StartTime=beginTime,
                                        EndTime=endTime,
                                        PlateNumber=request.form["plate"],
                                        Price=sustain)
                else:
                    Util.Booking.update_Lot(mov_dict[i].get('to'), mov_dict[i].get('id'))
        result = Book.alter_book()
        if result == "success":
            return redirect('/customer_index')
        else:
            flash(u'failed to summit the order,please try again', 'error')  # 消息错误提示
            return render_template('reserve.html')


@app.route('/cancelreserve/<ID>', methods=["POST", "GET"])
def cancelreserve(ID):
    result = Util.Booking.cancel_book(ID)
    if result == "success":
        return redirect('/customer_index')
    else:
        return result


# ---------------------------获取停车位信息--------------------------------------
@app.route('/lot')
def lot():
    return render_template('pad1.html')


@app.route('/getlotname', methods=["POST", "GET"])
def getlotname():
    print "nihao"
    if request.method == "POST":
        print "nibuhao"
        order_number = request.form['inputNumber']
        plate_number = request.form['inputLicenseNumber']
        print order_number
        print plate_number
        if order_number == "" and plate_number == "":
            redirect('/lot')
        else:
            if order_number != "":
                result = Util.Booking.query_book(order_number)
                if result:
                    ans = Util.ParkingLot.set_lot_status(result.PID)
                else:
                    result = Util.Booking.query_book_by_plate(plate_number)      # plate_number不是唯一，这里要修正
                if result:
                    ans = Util.ParkingLot.set_lot_status(result.PID)
        return render_template('pad2.html', result=result)
    return render_template('pad2.html', result=None)


# ---------------------------经理相关--------------------------------------------

@app.route('/manager_page')
def manager_page():
    return render_template("manager_login.html");

@app.route('/manage_index')
def manage_index():
    lots_status = Util.all_lot_status()
    print json.dumps(lots_status)
    return render_template('console.html', lots_status=json.dumps(lots_status))


@app.route('/show_reservation')
def show_reservation():
    return render_template('show-reservation.html')


@app.route('/business_price', methods=['GET', 'POST'])
def business_price():  # 显示
    price_reservation = Util.Pricedata.get_price('0')  # 三种价格：正常价罚款折扣
    price_overstay = Util.Pricedata.get_price('1')
    price_discount = Util.Pricedata.get_price('2')
    return render_template('business_price.html', price_reservation=price_reservation, price_overstay=price_overstay,
                           price_discount=price_discount)


@app.route('/confirm_publish', methods=['GET', 'POST'])
def confirm_publish():
    if request.method == "POST":
        reservprice = request.form['reservPrice']
        overstayfine = request.form['overstayFine']
        discounts = request.form['discounts']
        result = Util.Pricedata.set_price(reservprice, overstayfine, discounts)
        if result == "success":
            print result
            return redirect(url_for('business_price'))
        else:
            flash(u'failed to summit the price,please try again', 'error')
            print "nifnianfia"
            return render_template('business_price.html')
    return render_template('business_price.html')

@app.route('/business_promotion')
def business_promotion():
    return render_template('business_promotion.html')


@app.route('/show_reservation1/<date>')
def show_reservation1(date):
    the_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    order_date = Util.oneday_lot(the_date)
    print json.dumps(order_date)
    return render_template('show-reservation.html', reservation=json.dumps(order_date), date=date)


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
