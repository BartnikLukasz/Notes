from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notesApp.db'
db = SQLAlchemy(app)


class User:
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    children = relationship("Note")


class Note:
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, ForeignKey('User.id'))


if __name__ == "__main__":
    app.run(debug=True)