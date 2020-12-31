from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return 'Note %r' % self.id


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    user = db.Column(db.Integer)

    def __repr__(self):
        return 'User %r' % self.id


db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        note_content = request.form['content']
        new_note = Note(content=note_content)

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/')
        except:
            return 'Issue occured'
    else:
        notes = Note.query.order_by(Note.date).all()
        return render_template('index.html', notes=notes)


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    note = Note.query.get_or_404(id)

    if request.method == 'POST':
        Note.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue'
    else:
        return render_template('update.html', note=note)


@app.route('/delete/<int:id>')
def deleteNote(id):
    note = Note.query.get_or_404(id)

    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/')
    except:
        return "Cannot delete this note."


if __name__ == "__main__":
    app.run(debug=True)
