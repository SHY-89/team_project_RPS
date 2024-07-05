from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, url_for, request, session, redirect, jsonify
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


class GameLog(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    player = db.Column(db.String(20), nullable=False)
    computer = db.Column(db.String(20), nullable=False)
    result = db.Column(db.String(10), nullable=False)
    w_date = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())


@app.route('/')
def games():
    return_url = ''
    data = []
    if 'user_id' in session:
        return_url = 'game.html'
        suser_id = session['user_id']
        select_game = GameLog.query.filter_by(user_id=suser_id).order_by(GameLog.idx.desc()).all()
        data = [ {'player':gamedata.player,'computer':gamedata.computer, 'result':gamedata.result} for gamedata in select_game]
    else:
        return_url = 'login.html'
    return render_template(return_url,rend_data=data)

@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return render_template('/')
    elif request.method == 'POST':
        filter_list = Users.query.filter_by(
            user_id=request.form['user_id'], user_pw=request.form['user_pw']).all()
        if filter_list:
            session['user_id'] = request.form['user_id']
            return redirect(url_for('games'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('games'))


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
    if 'user_id' in session:
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

        suser_id = session['user_id']
        gamelog = GameLog(
            user_id=suser_id, player=rps[user], computer=rps[choice], result=reuslt)
        db.session.add(gamelog)
        db.session.commit()

    return {'computer': rps[choice], 'reuslt': reuslt}


if __name__ == '__main__':
    app.run()
