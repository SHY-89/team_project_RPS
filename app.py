import random
from flask import Flask, render_template, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy

# 현재 파일의 절대 경로를 기준으로 데이터베이스 파일의 경로를 설정합니다.
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# Flask 애플리케이션에 SQLAlchemy 데이터베이스 설정을 추가합니다.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')

# SQLAlchemy 객체를 생성하여 Flask 애플리케이션과 연결합니다.
db = SQLAlchemy(app)


# 데이터베이스 모델을 정의합니다.
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 기본 키로 사용할 정수형 ID 컬럼
    user_choice = db.Column(db.String(100), nullable=False)  # 사용자 선택을 저장할 문자열 컬럼
    computer_choice = db.Column(db.String(100), nullable=False)  # 컴퓨터 선택을 저장할 문자열 컬럼
    result = db.Column(db.String(100), nullable=False)  # 게임 결과를 저장할 문자열 컬럼

    def __repr__(self):
        return f'user_choice={self.user_choice}, computer_choice={self.computer_choice}, result={self.result})'


# 애플리케이션 컨텍스트 내에서 데이터베이스를 생성합니다.
with app.app_context():
    db.create_all()


# 루트 URL('/')에 대한 요청을 처리하는 뷰 함수입니다.
@app.route('/')
def index():
    # 최근 10개의 게임 결과를 데이터베이스에서 조회합니다.
    game_results = Users.query.order_by(Users.id.desc()).limit(10).all()
    # 조회한 게임 결과를 템플릿에 전달하여 렌더링합니다.
    return render_template('index.html', game_results=game_results)


# 랜덤으로 가위, 바위, 보 중 하나를 선택하는 함수입니다.
def select_random_hand():
    hands = ["가위", "바위", "보"]
    return random.choice(hands)


# '/submit' URL에 대한 POST 요청을 처리하는 뷰 함수입니다.
@app.route('/submit', methods=['POST'])
def submit():
    choices = ['가위', '바위', '보']  # 사용자 선택 옵션
    user_input = int(request.form['user_input'])  # 폼 데이터에서 사용자 입력을 가져옵니다.
    user_choice = choices[user_input - 1]  # 사용자 입력을 바탕으로 사용자가 선택한 옵션을 결정합니다.
    computer_choice = random.choice(choices)  # 컴퓨터의 선택을 랜덤으로 결정합니다.

    # 사용자와 컴퓨터의 선택에 따른 게임 결과를 결정합니다.
    if user_choice == computer_choice:
        result = 'DRAW'
    elif (user_choice == '가위' and computer_choice == '보') or \
            (user_choice == '바위' and computer_choice == '가위') or \
            (user_choice == '보' and computer_choice == '바위'):
        result = 'WIN'
    else:
        result = 'LOSE'

    # 결과를 데이터베이스에 저장합니다.
    game_result = Users(user_choice=user_choice, computer_choice=computer_choice, result=result)
    db.session.add(game_result)
    db.session.commit()

    # 콘솔에 게임 결과를 출력합니다.
    print(f"User choice: {user_choice}, Computer choice: {computer_choice}, {result}")

    # 최근 10개의 게임 결과를 데이터베이스에서 조회하여 JSON 형태로 변환합니다.
    game_results = Users.query.order_by(Users.id.desc()).limit(10).all()
    game_results_dict = [{'user_choice': r.user_choice, 'computer_choice': r.computer_choice, 'result': r.result} for r
                         in game_results]

    # 게임 결과와 최근 10개의 게임 결과를 JSON 형태로 반환합니다.
    return jsonify({
        'user_choice': user_choice,
        'computer_choice': computer_choice,
        'result': result,
        'game_results': game_results_dict
    })


# 애플리케이션을 디버그 모드에서 실행합니다.
if __name__ == '__main__':
    app.run(debug=True)
