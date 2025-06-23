import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    hobbies = [
        {
            "name": "Gaming",
            "description": "Competitive and casual gaming sessions",
            "image": "/static/img/gaming.jpg"
        },
        {
            "name": "Anime",
            "description": "I watch anime and discuss lore with friends",
            "image": "/static/img/anime.jpg"
        },
    ]
    return render_template("hobbies.html", hobbies=hobbies)
