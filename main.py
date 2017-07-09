from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:sounders@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def  __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            print(session)
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')


    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()

        if (username == "") or (" " in username) or (len(username) <= 3):
            flash("That's not a valid username", 'error')
            username = ""

        elif (password == "") or (" " in password) or (len(password) <= 3):
            flash("That's not a valid password", 'error')

        elif verify != password:
            flash("Passwords to not match", 'error')

        elif existing_user:
            flash('Username Already Exists', 'error')

        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

    return render_template('signup.html')


@app.route('/logout')
def logout():


    return

@app.route('/newPost', methods=['GET', 'POST'])
def add_blog():

    owner = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title == '':
            flash('Please enter a title for your new blog post', 'error')
            return render_template('newPost.html', body=body)
        if body == '':
            flash('Please enter a body for your new blog post', 'error')
            return render_template('newPost.html', title=title)
        blog = Blog(title=title, body=body, owner=owner)
        db.session.add(blog)
        db.session.commit()
        return redirect('/blog?id=' + str(blog.id))


    return render_template('newPost.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():

    return

def single_blog():



    return

@app.route('/blog', methods=['GET', 'POST'])
def index():


    return


if __name__ == '__main__':
    app.run()