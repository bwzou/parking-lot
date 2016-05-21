# --coding:utf8--
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
# from Parking import queue  相互导会出现问题

blue_customer = Blueprint('blue_customer', __name__, template_folder='templates')   # 注册蓝图


@blue_customer.route('//', defaults={'page': 'index'})      # 此时是默认主界面
@blue_customer.route('/<page>')
def index(page):
    try:
        return render_template('%s.html' % page)      # 打印相应的页
    except TemplateNotFound:
        abort(404)



