import os
import datetime
from flask import Flask, render_template, request
from dotenv import load_dotenv
from peewee import MySQLDatabase
from peewee import Model, CharField, TextField, DateTimeField
from playhouse.shortcuts import model_to_dict

app = Flask(__name__)

#load_dotenv()

mydb = MySQLDatabase(None)  # Placeholder

load_dotenv()

if os.getenv("TESTING") == "true":
    from peewee import SqliteDatabase
    mydb = SqliteDatabase(':memory:')
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

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
        {"role": "MLH Fellow", "company": "MLH", "year": "2025", "description": "Fellowship for production engineering."}

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
@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")

@app.route("/api/timeline_post", methods=["POST"])
def post_timeline_post():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    content = request.form.get("content", "").strip()

    if not name:
        return "Invalid name", 400
    if not email or "@" not in email:
        return "Invalid email", 400
    if not content:
        return "Invalid content", 400

    post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(post)
#@app.route('/api/timeline_post', methods=['POST'])
#def post_time_line_post():
 #   name = request.form['name']
#    email = request.form['email']
 #   content = request.form['content']
  #  timeline_post = TimelinePost.create(name=name, email=email, content=content)

   # return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

