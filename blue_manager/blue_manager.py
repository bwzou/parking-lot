# --coding:utf8--
from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

blue_manager = Blueprint('blue_manager', __name__, template_folder='templates')   # 注册蓝图


@blue_manager.route('/manager_page', defaults={'page': 'manager_login'})      # 此时是默认主界面
@blue_manager.route('/<page>')
def index(page):
    try:
        return render_template('%s.html' % page)      # 打印相应的页
    except TemplateNotFound:
        abort(404)