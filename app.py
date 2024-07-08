import app
from flask import Flask, request, render_template, redirect, url_for, session, flash
import random
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


# init_db()

# def create_app():
#     app = Flask(__name__)
#     with app.app_context():
#         init_db()
#     return app



# 데이터베이스 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    records = db.relationship('Record', backref='user', lazy=True)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    result = db.Column(db.String(20), nullable=False)



db.create_all()


# 사용자
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


# 가위바위보
class PlayForm(FlaskForm):
    choice = StringField('나의 패 선택하기', validators=[DataRequired()], render_kw={
                         "placeholder": "가위/바위/보 중 하나를 입력하세요"})
    submit = SubmitField('Play')


# 회원가입
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


# 라우트들
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        new=User(username=username, password=password)
        db.session.add(new)
        db.session.commit()
        
        flash('회원가입이 완료되었습니다. 로그인하세요', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('play'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        user = User.query.filter_by(username=username, password=password).first()
            
            
        if user:
            session['username'] = user.username
            flash('로그인 완료', 'success')
            return redirect(url_for('play'))
        else:
            flash('다시 시도해주세요.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('로그아웃했습니다.', 'success')
    return redirect(url_for('index'))


@app.route('/play', methods=['GET', 'POST'])
def play():
    if 'username' not in session:
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
        user = User.query.filter_by(username=session['username']).first()
        new_record = Record(user_id=user.id, result=result)
        db.session.add(new_record)
        db.session.commit()

        return render_template('result.html', user_choice=user_choice, computer_choice=computer_choice, result=result)

    return render_template('play.html', form=form)


# 메인 함수
if __name__ == '__main__':
    app.run(debug=True)
