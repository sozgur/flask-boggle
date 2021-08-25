from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)

app.config["SECRET_KEY"] = "43242kdfLSDFKsdfgo#$5"

boggle_game = Boggle()


@app.route("/")
def display_board():
    """ Create a board and show on home page """
    board = boggle_game.make_board()
    session['board'] = board
    total_played = session.get("total_played", 0)
    highscore = session.get("highscore", 0)
    return render_template("home.html", board=board, highscore=highscore, total_played = total_played)


@app.route("/check-word/json")
def check_word_json():
    """ Check if the word in dictionart and on board """
    word = request.args["word"]
    board = session["board"]
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})



@app.route("/final-score", methods=['POST'])
def calculate_score():
    """ Receive score and update the hight score"""
    score = request.json["score"]
    total_played = session.get("total_played",0)
    highscore = session.get("highscore",0)

    session['total_played'] = total_played + 1
    session['highscore'] = max(score, highscore)

    return jsonify({'brokeRecord': score > highscore})