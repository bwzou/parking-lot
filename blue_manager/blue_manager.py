# --coding:utf8--
from flask import Blueprint, render_template, abort, request, render_template, session, \
    redirect, flash, url_for, make_response
from jinja2 import TemplateNotFound
import Util

import datetime
import json
import Manage

blue_manager = Blueprint('blue_manager', __name__, template_folder='templates')   # 注册蓝图


@blue_manager.route('/manager_page', defaults={'page': 'manager_login'})      # 此时是默认主界面
@blue_manager.route('/<page>')
def manager_page(page):
    try:
        return render_template('%s.html' % page)      # 打印相应的页
    except TemplateNotFound:
        abort(404)


@blue_manager.route('/manager_login', methods=["POST", "GET"])
def manager_login():
    """  check ording"""
    phone = request.form.get('inputPhoneNumber')
    password = request.form.get('inputPassword')
    result = Manage.manager_login(phone, password)
    print result
    if result == "success":
        session['manager_username'] = phone                     # 添加到session
        return redirect(url_for('blue_manager.manage_index'))
    else:
        flash(u'Invalid password or username provided', 'error')        # 消息错误提示
        return render_template('manager_login.html')


@blue_manager.route('/manage_index')
def manage_index():
    lots_status = Manage.all_lot_status()
    print json.dumps(lots_status)
    return render_template('console.html', lots_status=json.dumps(lots_status))


@blue_manager.route('/show_reservation')
def show_reservation():
    return render_template('show-reservation.html')


@blue_manager.route('/business_price', methods=['GET', 'POST'])
def business_price():  # 显示
    price_reservation = Manage.get_price('0')  # 三种价格：正常价罚款折扣
    price_overstay = Manage.get_price('1')
    price_discount = Manage.get_price('2')
    return render_template('business_price.html', price_reservation=price_reservation, price_overstay=price_overstay,
                           price_discount=price_discount)


@blue_manager.route('/confirm_publish', methods=['GET', 'POST'])
def confirm_publish():
    if request.method == "POST":
        reservprice = request.form['reservPrice']
        overstayfine = request.form['overstayFine']
        discounts = request.form['discounts']
        result = Manage.set_price(reservprice, overstayfine, discounts)
        if result == "success":
            print result
            return redirect(url_for('blue_manager.business_price'))
        else:
            flash(u'failed to summit the price,please try again', 'error')
            return render_template('business_price.html')
    return render_template('business_price.html')


@blue_manager.route('/business_promotion')
def business_promotion():
    data = Manage.get_promotion()
    return render_template('business-promotion.html', data=data)


@blue_manager.route('/man_show_pro/<Id>')
def get_single_promotion(Id):
    data = Manage.get_single_promotion(Id)
    print data
    return render_template('specific-promotion.html', data=data)


@blue_manager.route('/delete_promotion/<ID>', methods=["POST", "GET"])
def delete_promotion(ID):
    result = Manage.delete_promotion(ID)
    if result == "success":
        return redirect('/business_promotion')
    else:
        return result


@blue_manager.route('/add_promotion', methods=["POST", "GET"])
def add_promotion():
    if request.method == "POST":
        title = request.form['addtitle']
        context = request.form['addcontext']
        print context
        result = Manage.set_promotion(title, context)
        print result
        if result == "success":
            return redirect(url_for('blue_manager.business_promotion'))
        else:
            flash(u'failed to summit the promotion,please try again', 'error')
            return redirect('/business_promotion')
    return redirect('/business_promotion')


@blue_manager.route('/show_reservation1/<date>')
def show_reservation1(date):
    the_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    order_date = Manage.oneday_order_lot(the_date)
    print json.dumps(order_date)
    return render_template('show-reservation.html', reservation=json.dumps(order_date), date=date)


@blue_manager.route('/profit')
def profit():
    mlist = Util.get_ex_day_list()
    pp = []
    for t2 in mlist:
        m = Util.salary(t2)
        m.get_all_today_money()
        print m.profit, m.reservation, m.date
        pp.append(m)
        print Util.class_to_dict(pp)
    d = Util.class_to_dict(pp)
    d  = json.dumps(d)
    return render_template('profit.html', date=d)
