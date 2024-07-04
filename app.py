from flask import Flask, render_template, url_for, request
from flask_cors import CORS
app = Flask(__name__)

@app.route('/')
def games():
    return render_template('game.html')

@app.route('/game/winlose')
def game_winlose():
    player = request.args.get("user_choise")
    
    return player


if __name__ == '__main__':
    app.run()