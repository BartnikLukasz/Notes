from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return self.username + " " + self.password


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    user = db.Column(db.String(20))

    def __repr__(self):
        return 'Note %r' % self.id


db.create_all()


@auth.verify_password
def verify_password(username, password):
    users_list = User.query.all()
    users = {users_list[i].username: users_list[i].password for i in range(0, len(users_list))}
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route('/')
def starting_page():
    return render_template('/start_page.html')


@app.route('/home', methods=['POST', 'GET'])
@auth.login_required
def index():
    if request.method == 'POST':
        note_content = request.form['content']
        new_note = Note(content=note_content, user=auth.current_user().username)

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/home')
        except:
            return 'Issue occured'
    else:
        notes = Note.query.order_by(Note.date).all()
        return render_template('index.html', notes=notes)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['userReg']
        password = request.form['passReg']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        print(username)
        print(hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/home')
        except:
            return 'Issue occured'
    else:
        return render_template('register.html')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    note = Note.query.get_or_404(id)

    if request.method == 'POST':
        note.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/home')
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
        return redirect('/home')
    except:
        return "Cannot delete this note."


if __name__ == "__main__":
    app.run(debug=True)
