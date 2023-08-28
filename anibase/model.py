from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Anime(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    title_english = db.Column(db.String)
    episodes = db.Column(db.Integer)
    year = db.Column(db.Integer, nullable=False)
