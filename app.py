from flask import Flask, render_template, url_for, request
from flask_cors import CORS
import random
app = Flask(__name__)

@app.route('/')
def games():
    return render_template('game.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/sign')
def sign():
    return render_template('sign.html')

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

    return {'computer' : rps[choice], 'reuslt': reuslt}


if __name__ == '__main__':
    app.run()