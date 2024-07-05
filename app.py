from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, url_for, request, session, redirect
from flask_cors import CORS
import random
from datetime import datetime
app = Flask(__name__)

# DB 기본 코드
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.secret_key = 'lXiptP4htKFY6SemXVvxNxF4w'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


class Users(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_pw = db.Column(db.String(100), nullable=False)
    join_date = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())


@app.route('/')
def games():
    return_url = ''
    if 'user_id' in session:
        user_id = session['user_id']
        # 전적 검색 부분 
        return_url = 'game.html'
    else:
        return_url = 'login.html'
    return render_template(return_url)

@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return render_template('/')
    elif request.method == 'POST':
        filter_list = Users.query.filter_by(user_id=request.form['user_id'],user_pw=request.form['user_pw']).all()
        if filter_list:
            session['user_id'] = request.form['user_id']
            return redirect(url_for('games'))        
        
    return render_template('login.html')


@app.route('/sign')
def sign():
    return render_template('sign.html')


@app.route('/check/user')
def check_user():
    ruser_id = request.args.get("user_id")
    filter_list = Users.query.filter_by(user_id=ruser_id).all()
    result = 'sussece'
    if filter_list:
        result = 'fail'
    return {'reuslt': result}


@app.route('/user/create', methods=['POST'])
def user_create():
    params = request.form
    ruser_id = params['user_id']
    ruser_pw = params['user_pw']
    ruser_name = params['user_name']
    filter_list = Users.query.filter_by(user_id=ruser_id).all()

    result = 'sussece'
    if filter_list:
        result = 'fail'
    else:
        user = Users(user_id=ruser_id, user_name=ruser_name, user_pw=ruser_pw)
        db.session.add(user)
        db.session.commit()

    return {'reuslt': result}


@app.route('/game/winlose')
def game_winlose():

    user = request.args.get("user_choise")
    # RPS 부분 추가
    rps = {'1': '가위', '2': '바위', '3': '보'}
    computer = ['1', '2', '3']
    choice = random.choice(computer)
    reuslt = ""
    if user == choice:
        reuslt = "비겼 습니다."
    elif (choice == '1' or choice == '3') and (user == '1' or user == '3'):
        if int(choice) % 3 > int(user) % 3:
            reuslt = "컴퓨터 승리!!"
        else:
            reuslt = "사용자 승리!!"
    else:
        if int(choice) > int(user):
            reuslt = "컴퓨터 승리!!"
        else:
            reuslt = "사용자 승리!!"

    return {'computer': rps[choice], 'reuslt': reuslt}


if __name__ == '__main__':
    app.run()
