from flask import Flask
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)