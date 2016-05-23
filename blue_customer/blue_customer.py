# --coding:utf8--
from flask import Blueprint, render_template, abort, request, render_template, session, \
    redirect, flash, url_for, make_response
from jinja2 import TemplateNotFound
from RedisQueue import RedisQueue
from pickle import dumps, loads          # 字符串跟字典间的转换

# json.dumps : dict转成str
# json.loads : str转成dict
# from Parking import queue  相互导会出现问题

import datetime,time

import sys
import Manage
import Util           # 控制层
from globle import gl, Temp

blue_customer = Blueprint('blue_customer', __name__, template_folder='templates')   # 注册蓝图
queue = RedisQueue('my_queue')        # 根据Redis生成queue


@blue_customer.route('/customer_index', defaults={'page': 'home01'})      # 此时是默认主界面
@blue_customer.route('/<page>')
def customer_index(page):
    if session.get('username') is None:
        redirect('/')
    else:
        data, history = Manage.Reservation.diplay_book(session["username"])
        history_data = Manage.Reservation.diplay_history_book(
            session["username"])
        if history is None:
            if history_data == []:
                pass
            else:
                data = []
                history = history_data
        elif history == [] and history_data == []:
            pass
        else:
            history += history_data
        try:
            return render_template('%s.html' % page, data=data, history=history)  # 打印相应的页
        except TemplateNotFound:
            abort(404)


@blue_customer.route('/reserve')
def reserve():
    """ information about book"""
    # flash(u'Sorry! There is no a Parkinglot available now', 'error')  # 消息错误提示
    return render_template('reserve.html')


@blue_customer.route('/reserver', methods=["POST", "GET"])
def reserver():
    if request.method == "POST":
        Time = request.form['slider_value']
        beginTime, endTime = Time[6:11], Time[16:21]

        if endTime == "24:00":
            endTime = "23:59"

        # timeintervel = beginTime + "   to   " + endTime
        temp = request.form["picker"] + "/" + beginTime
        beginTime = datetime.datetime.strptime(temp, '%m/%d/%Y/%H:%M')
        temp = request.form["picker"] + "/" + endTime
        endTime = datetime.datetime.strptime(temp, '%m/%d/%Y/%H:%M')

        produceTime= Util.get_timenow()
        print produceTime
        dict={}
        dict['type'] = 'create'
        dict['id'] = None
        dict['beginTime'] = beginTime
        dict['endTime'] = endTime
        dict['name'] = session["username"]
        dict['PlateNumber'] = request.form["plate"]
        dict['time'] = produceTime   # 不知道出现什么问题
        str = dumps(dict)
        queue.put(str)  # 添加到队列里面

        return render_template('wait.html', time=produceTime)


@blue_customer.route('/pay2')
def pay2():
    return render_template('pay2.html', date=Temp.TempData)


@blue_customer.route('/payreserve/<Id>')
def payreserve(Id):
    Temp.TempData = Manage.Reservation.query_book(Id)
    if Temp.TempData.diff == '0' or Temp.TempData.diff is None:
        return render_template('pay2.html', date=Temp.TempData)
    else:
        return render_template('change2.html', Data=Temp.TempData)
    # return redirect('finish')
    return redirect('pay2')


@blue_customer.route('/paycharge/<Id>')
def paycharge():
    result = Temp.TempCharge.pay_charge()
    if result == "success":
        return render_template('pad1.html')
    else:
        return "fail"


@blue_customer.route('/changereserve/<ID>', methods=["POST", "GET"])
def changereserve(ID):
    result = Manage.Reservation.query_book(ID)
    if result is not None:
        result = Util.change_bookto(result)
    return render_template('reserve.html', result=result)


@blue_customer.route('/change/<Id>', methods=["POST", "GET"])
def change(Id):
    if request.method == "POST":
        Time = request.form['slider_value']
        beginTime, endTime = Time[6:11], Time[16:21]

        if endTime == "24:00":
            endTime = "23:59"

        timeintervel = beginTime + "   to   " + endTime
        temp = request.form["picker"] + "/" + beginTime
        beginTime = datetime.datetime.strptime(temp, '%m/%d/%Y/%H:%M')
        temp = request.form["picker"] + "/" + endTime
        endTime = datetime.datetime.strptime(temp, '%m/%d/%Y/%H:%M')

        dict = {}
        dict['type'] = 'change'
        dict['id'] = Id
        dict['beginTime'] = beginTime
        dict['endTime'] = endTime
        dict['name'] = session["username"]
        dict['PlateNumber'] = request.form["plate"]
        dict['time'] = Util.get_timenow()     # 不知道出现什么问题
        str = dumps(dict)
        queue.put(str)      # 添加到队列里面
        return render_template('wait.html')


@blue_customer.route('/cancelreserve/<ID>', methods=["POST", "GET"])
def cancelreserve(ID):
    dict = {}
    dict['type'] = 'cancel'
    dict['id'] = ID
    dict['beginTime'] = None
    dict['endTime'] = None
    dict['name'] = session["username"]
    dict['PlateNumber'] = None
    dict['time'] = Util.get_timenow()  # 不知道出现什么问题
    str = dumps(dict)
    queue.put(str)  # 添加到队列里面
    return render_template('wait.html')


@blue_customer.route('/finish')
def finish():
    result = Temp.TempData.pay_debt()
    if result == "fail":
        return "false"
    return redirect('/customer_index')


@blue_customer.route('/finishpayreserve')
def finishpayreserve():
    return render_template('finish.html')


@blue_customer.route('/finish3')
def finish3():
    return render_template('finish3.html')


@blue_customer.route('/get_result')
def get_result():
    result = 'wait'
    time1 = request.args.get('name', 0, type=str)
    name = session.get('username')
    print '------------------------------------------------------------------'
    print name, time1

    ans = Manage.Reservation.query_by_name_produceTime(time1, name)

    print '------------------------------------------------------------------'
    print ans

    while ans is None:
        time.sleep(5)
        ans = Manage.Reservation.query_by_name_produceTime(time1, name)
        print ans
        if ans is not None:
            result = 'success'
            break
        else:
            if queue.qsize() == 0:
                result = 'fail'
            break

    return result
