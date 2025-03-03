
from flask_sqlalchemy import SQLAlchemy  # type: ignore
import os, random, hashlib, re
from flask import Flask, render_template, url_for, request, session, redirect, jsonify, flash  # type: ignore
from flask_cors import CORS  # type: ignore
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
    error = None
    if 'user_id' in session:
        return redirect(url_for('game_syh'))
    elif request.method == 'POST':
        m = hashlib.sha256()
        m.update(request.form['user_pw'].encode('utf-8'))
        filter_list = Users.query.filter_by(
            user_id=request.form['user_id'], user_pw=m.hexdigest()).all()
        if filter_list:
            session['user_id'] = request.form['user_id']
            return redirect(url_for('game_syh'))
        error = 'login_fail'

    return render_template('login.html', data=error)


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
    error = ''
    result = 'sussece'
    p = re.compile('^(?=.*[a-zA-Z])(?=.*[0-9]).{8,25}$')
    if filter_list or len(ruser_id) < 4:
        result = 'fail'
        error = 'id'
    elif len(ruser_pw) < 8 or p.match(ruser_pw) == None:
        result = 'fail'
        error = 'pw'
    else:
        m = hashlib.sha256()
        m.update(ruser_pw.encode('utf-8'))
        user = Users(user_id=ruser_id, user_name=ruser_name, user_pw=m.hexdigest())
        db.session.add(user)
        db.session.commit()

    return {'reuslt': result, 'error': error}


@app.route('/game/kdm')
def game_kdm():
    return_url = ''
    data = []
    if 'user_id' in session:
        return_url = 'game_kdm.html'
        suser_id = session['user_id']
        data = GameLog.query.filter_by(user_id=suser_id).order_by(GameLog.idx.desc()).limit(10).all()
    else:
        return_url = 'login.html'
    
    win_count = 0
    draw_count = 0
    lose_count = 0
        
    win_count = GameLog.query.filter_by(
        user_id=suser_id, result='사용자 승리!!').count()
    draw_count = GameLog.query.filter_by(
        user_id=suser_id, result='비겼 습니다.').count()
    lose_count = GameLog.query.filter_by(
        user_id=suser_id, result='컴퓨터 승리!!').count()
    context = {
        "player_choice": '',
        "computer_choice": '',
        "game_win_lose": '',
        "win_count": win_count,
        "draw_count": draw_count,
        "lose_count": lose_count
    }
    return render_template(return_url, data=context)

# 가위바위보
class PlayForm(FlaskForm):
    player_choice = SelectField('나의 패 선택하기', choices=['가위','바위','보'])
    submit = SubmitField('Play')

@app.route('/game/cmh')
def game_cmh():
    if 'user_id' not in session:
        flash('우선 로그인하세요.', 'warning')
        return redirect(url_for('login'))

    form = PlayForm()

    suser_id = session['user_id']
    history = GameLog.query.filter_by(user_id=suser_id).order_by(GameLog.idx.desc()).limit(10).all()

    return render_template('game_cmh.html', form=form, history=history)

@app.route('/game/rps', methods=['POST'])
def game_rps():
    return_url = ''
    if 'user_id' in session and request.method == 'POST':
        player_choice = request.form['player_choice']
        if player_choice in ['1','2','3']:
            choices = ['가위', '바위', '보']
            player_choice = choices[int(request.form['player_choice'])-1]
        computer_choice = random.choice(['가위', '바위', '보'])

        if (player_choice == '가위' and computer_choice == '보') or (player_choice == '바위' and computer_choice == '가위') or (player_choice == '보' and computer_choice == '바위'):
            game_win_lose = '사용자 승리!!'
        elif player_choice == computer_choice:
            game_win_lose = '비겼 습니다.'
        else:
            game_win_lose = '컴퓨터 승리!!'
        
        new_game = GameLog(user_id=session['user_id'], player=player_choice, computer=computer_choice, result=game_win_lose)
        db.session.add(new_game)
        db.session.commit()
        
        
        if 'kdm' in request.form:
            win_count = GameLog.query.filter_by(
                user_id=session['user_id'], result='사용자 승리!!').count()
            draw_count = GameLog.query.filter_by(
                user_id=session['user_id'], result='비겼 습니다.').count()
            lose_count = GameLog.query.filter_by(
                user_id=session['user_id'], result='컴퓨터 승리!!').count()
            context = {
                "player_choice": player_choice,
                "computer_choice": computer_choice,
                "game_win_lose": game_win_lose,
                "win_count": win_count,
                "draw_count": draw_count,
                "lose_count": lose_count
            }
            return_url = 'game_kdm.html'
            
            return render_template(return_url, data=context)
        elif 'khk' in request.form:
            
            game_results = GameLog.query.filter_by( user_id=session['user_id']).order_by(GameLog.idx.desc()).limit(10).all()
            game_results_dict = [{'user_choice': r.player, 'computer_choice': r.computer, 'result': r.result} for r in game_results]
            
            return jsonify({
                'user_choice': player_choice,
                'computer_choice': computer_choice,
                'result': game_win_lose,
                'game_results': game_results_dict
            })
        elif 'cmh' in request.form:
            form = PlayForm()
            return_url = 'game_cmh.html'
            
            return render_template(return_url, form=form, result= {'user_choice':player_choice, 'computer_choice':computer_choice, 'result':game_win_lose})
        elif 'syh' in request.form:
            return {'computer': computer_choice, 'result': game_win_lose, 'rank': rank_list()}
     
    return render_template(return_url, data=context)


if __name__ == '__main__':
    app.run()
