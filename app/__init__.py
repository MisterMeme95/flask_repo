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

@app.route('/work')
def work():
    work_data = [
        {"role": "Software Intern", "company": "TechCorp", "year": "2024", "description": "Built backend APIs"},
        {"role": "RA", "company": "Univ Lab", "year": "2023", "description": "Worked on ML models"}
    ]
    return render_template("list_section.html", section_title="Work Experience", items=work_data)

@app.route('/education')
def education():
    education_data = [
        {"school": "ABC University", "degree": "CS B.Sc.", "year": "2020–2024", "description": "Focus on AI"},
    ]
    return render_template("list_section.html", section_title="Education", items=education_data)
