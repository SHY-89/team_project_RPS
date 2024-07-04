from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def games():
    return render_template('game.html')
    
if __name__ == '__main__':
    app.run()