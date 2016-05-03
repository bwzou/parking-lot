from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('home00.html')


@app.route('/register')
def register():
    return render_template('home01.html')


@app.route('/reserve')
def reserve():
    return render_template('reserve.html')


@app.route('/pad1')
def pad1():
    return render_template('pad1.html')


@app.route('/pad2')
def pad2():
    return render_template('pad2.html')


if __name__ == '__main__':
    app.run(debug=True)
