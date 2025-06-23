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
            "description": "Competitive and casual gaming sessions. Jak and Daxter (pictured below) is my favorite game.",
            "image": "/static/img/game.jpg"
        },
        {
            "name": "Anime",
            "description": "I watch anime and discuss lore with friends. Naturally, I think Dragonball is the best.",
            "image": "/static/img/anime.jpg"
        },
    ]
    return render_template("hobbies.html", hobbies=hobbies)

@app.route('/work')
def work():
    work_data = [
        {"role": "Software Intern", "company": "Los Alamos National Lab", "year": "2025", "description": "Working on Physics Simulations"},
        {"role": "Tech Fellow", "company": "CodePath", "year": "2025", "description": "Teacher aid for techical interviews."}

    ]
    return render_template("list_section.html", section_title="Work Experience", items=work_data)

@app.route('/education')
def education():
    education_data = [
        {"school": "Florida International Univerisity", "degree": "Masters in Computer Science", "year": "2020–2026", "description": "I want to focus on visualization."},
    ]
    return render_template("list_section.html", section_title="Education", items=education_data)


@app.route('/locations')
def locations():
    locations = [
        {"name": "Los Alamos, New Mexico", "image": "/static/img/losalamos.jpg"},
        {"name": "Miami, Florida", "image": "/static/img/miamiflorida.jpg"},
        {"name": "Mexico", "image": "/static/img/mexico.jpg"},
    ]
    return render_template("locations.html", locations=locations, title="Map")

