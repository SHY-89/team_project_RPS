from flask import Flask, render_template, request
import random
import os
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)


class RPSGame(db.Model):
    game_num = db.Column(db.Integer, primary_key=True)
    computer = db.Column(db.String, nullable=False)
    player = db.Column(db.String, nullable=False)
    result = db.Column(db.String, nullable=False)

    # def __repr__(self):
    #     return f'{self.artist} {self.title} 추천 by {self.username}'


with app.app_context():
    db.drop_all()
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def main():
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
            game_win_lose = '승리'

        elif player_choice == computer_choice:
            game_win_lose = '무승부'
        else:
            game_win_lose = '패배'
        new_game = RPSGame(player=player_choice,
                           computer=computer_choice, result=game_win_lose)
        db.session.add(new_game)
        db.session.commit()
        win_count = RPSGame.query.filter_by(result='승리').count()
        draw_count = RPSGame.query.filter_by(result='무승부').count()
        lose_count = RPSGame.query.filter_by(result='패배').count()
    context = {
        "player_choice": player_choice,
        "computer_choice": computer_choice,
        "game_win_lose": game_win_lose,
        "win_count": win_count,
        "draw_count": draw_count,
        "lose_count": lose_count
    }

    return render_template('index.html', data=context)


if __name__ == '__main__':
    app.run(debug=True)
