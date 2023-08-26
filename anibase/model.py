from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Anime(db.Model):
    mal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    