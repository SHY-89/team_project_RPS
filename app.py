
from flask_sqlalchemy import SQLAlchemy  # type: ignore
import os
from flask import Flask, render_template, url_for, request, session, redirect, jsonify, flash  # type: ignore
from flask_cors import CORS  # type: ignore
import random
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

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


def rank_list():
    select_game = {}
    for total_data in GameLog.query.filter(GameLog.result.like('%!!')).all():
        if total_data.user_id not in select_game:
            select_game[total_data.user_id] = {}
            select_game[total_data.user_id]['user_id'] = total_data.user_id
            select_game[total_data.user_id]['win'] = 0
            select_game[total_data.user_id]['lose'] = 0
            select_game[total_data.user_id]['total'] = 0
            select_game[total_data.user_id]['avg'] = 0

        if total_data.result == '사용자 승리!!':
            select_game[total_data.user_id]['win'] += 1
        else:
            select_game[total_data.user_id]['lose'] += 1

        select_game[total_data.user_id]['total'] += 1
        select_game[total_data.user_id]['avg'] = int(
            (select_game[total_data.user_id]['win'] / select_game[total_data.user_id]['total']) * 100)

    sorted_data = dict(
        sorted(select_game.items(), key=lambda item: item[1]['avg'], reverse=True))
    custom_data = []
    i = 1
    for key, append_data in sorted_data.items():
        if i == 6:
            break
        custom_data.append(append_data)
        i += 1
    return custom_data


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/game/syh')
def game_syh():
    return_url = ''
    data = []
    if 'user_id' in session:
        return_url = 'game.html'
        suser_id = session['user_id']
        select_game = GameLog.query.filter_by(
            user_id=suser_id).order_by(GameLog.idx.desc()).all()
        data = [{'player': gamedata.player, 'computer': gamedata.computer,
                 'result': gamedata.result} for gamedata in select_game]

    else:
        return_url = 'login.html'
    return render_template(return_url, rend_data=data, rank_data=rank_list())


@app.route('/game/khk')
def game_khk():
    return_url = ''
    data = []
    if 'user_id' in session:
        return_url = 'game_khk.html'
        suser_id = session['user_id']
        data = GameLog.query.filter_by(
            user_id=suser_id).order_by(GameLog.idx.desc()).limit(10).all()

    else:
        return_url = 'login.html'

    return render_template(return_url, game_results=data)


@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('game_syh'))
    elif request.method == 'POST':
        filter_list = Users.query.filter_by(
            user_id=request.form['user_id'], user_pw=request.form['user_pw']).all()
        if filter_list:
            session['user_id'] = request.form['user_id']
            return redirect(url_for('game_syh'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))


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

    return {'computer': rps[choice], 'result': reuslt, 'rank': rank_list()}


@app.route('/submit', methods=['POST'])
def submit():
    choices = ['가위', '바위', '보']
    user_input = int(request.form['user_input'])
    user_choice = choices[user_input - 1]
    computer_choice = random.choice(choices)

    if user_choice == computer_choice:
        result = '비겼 습니다.'
    elif (user_choice == '가위' and computer_choice == '보') or \
            (user_choice == '바위' and computer_choice == '가위') or \
            (user_choice == '보' and computer_choice == '바위'):
        result = '사용자 승리!!'
    else:
        result = '컴퓨터 승리!!'

    # 결과 저장
    suser_id = session['user_id']
    gamelog = GameLog(
        user_id=suser_id, player=user_choice, computer=computer_choice, result=result)

    db.session.add(gamelog)
    db.session.commit()

    print(
        f"User choice: {user_choice}, Computer choice: {computer_choice}, {result}")

    game_results = GameLog.query.filter_by(
        user_id=suser_id).order_by(GameLog.idx.desc()).limit(10).all()
    game_results_dict = [{'user_choice': r.player, 'computer_choice': r.computer, 'result': r.result} for r
                         in game_results]

    return jsonify({
        'user_choice': user_choice,
        'computer_choice': computer_choice,
        'result': result,
        'game_results': game_results_dict
    })


@app.route('/game/kdm', methods=['GET', 'POST'])
def game_kdm():
    return_url = ''
    data = []
    if 'user_id' in session:
        return_url = 'game_kdm.html'
        suser_id = session['user_id']
        data = GameLog.query.filter_by(
            user_id=suser_id).order_by(GameLog.idx.desc()).limit(10).all()

    else:
        return_url = 'login.html'
    game_win_lose = ''
    player_choice = ''
    computer_choice = ''
    win_count = 0
    draw_count = 0
    lose_count = 0
    if request.method == 'POST':
        player_choice = request.form['player_choice']
        computer_choice = random.choice(['가위', '바위', '보'])
        if (player_choice == '가위' and computer_choice == '보') or (player_choice == '바위' and computer_choice == '가위') or (player_choice == '보' and computer_choice == '바위'):
            game_win_lose = '사용자 승리!!'

        elif player_choice == computer_choice:
            game_win_lose = '비겼 습니다.'
        else:
            game_win_lose = '컴퓨터 승리!!'
        new_game = GameLog(user_id=suser_id, player=player_choice,
                           computer=computer_choice, result=game_win_lose)
        db.session.add(new_game)
        db.session.commit()
    win_count = GameLog.query.filter_by(
        user_id=suser_id, result='사용자 승리!!').count()
    draw_count = GameLog.query.filter_by(
        user_id=suser_id, result='비겼 습니다.').count()
    lose_count = GameLog.query.filter_by(
        user_id=suser_id, result='컴퓨터 승리!!').count()
    context = {
        "player_choice": player_choice,
        "computer_choice": computer_choice,
        "game_win_lose": game_win_lose,
        "win_count": win_count,
        "draw_count": draw_count,
        "lose_count": lose_count
    }

    return render_template(return_url, data=context)

# 가위바위보
class PlayForm(FlaskForm):
    choice = SelectField('나의 패 선택하기', choices=['가위','바위','보'])
    submit = SubmitField('Play')

@app.route('/game/cmh', methods=['GET', 'POST'])
def game_cmh():
    if 'user_id' not in session:
        flash('우선 로그인하세요.', 'warning')
        return redirect(url_for('login'))
    
    form = PlayForm()
    if form.validate_on_submit():
        user_choice = form.choice.data
        computer_choice = random.choice(['가위', '바위', '보'])

        # 가위바위보 규칙
        if user_choice == computer_choice:
            result = '비겼습니다'
        elif (user_choice == '가위' and computer_choice == '보') or \
             (user_choice == '바위' and computer_choice == '가위') or \
             (user_choice == '보' and computer_choice == '바위'):
            result = '이겼습니다'
        else:
            result = '졌습니다'

        # 결과 저장
        suser_id = session['user_id']
        new_record = GameLog(user_id=suser_id, player=user_choice,
                           computer=computer_choice, result=result)
        db.session.add(new_record)
        db.session.commit()

        return render_template('result.html', user_choice=user_choice, computer_choice=computer_choice, result=result)


    return render_template('game_cmh.html', form=form)

if __name__ == '__main__':
    app.run()
