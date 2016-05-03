# --coding:utf8--
from flask import Flask
from flask import render_template, redirect, session

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
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


if __name__ == '__main__':
    app.run(debug=True)
