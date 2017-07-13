from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:sounders@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    body = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, blog_title, body, owner):
        self.blog_title = blog_title
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

            return redirect('/newPost')

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

            return redirect('/newPost')

    return render_template('signup.html')


@app.route('/logout')
def logout():

    del session['username']

    return redirect('/')


@app.before_request
def require_login():

    allowed_routes = ['signup', 'login', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:

        return redirect('/login')

@app.route('/newPost', methods=['GET', 'POST'])
def new_post():

    return render_template("newPost.html")


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'GET':
        blog_id = request.args.get('id')

        user_id = request.args.get('user')

        if blog_id:

            blog = Blog.query.filter_by(id=blog_id).first()

            return render_template("singlePost.html", blog=blog)

        elif user_id:

            owner = User.query.filter_by(id=user_id).first()

            blogs = Blog.query.filter_by(owner=owner).all()

            return render_template("singleUser.html", owner=owner, blogs=blogs)

        else:
            blogs = Blog.query.all()
            return render_template('blog.html', blogs=blogs)

    blog_title = request.form['blog_title']
    body = request.form['body']
    title_error = ""
    body_error = ""

    if blog_title is '':
        title_error = 'Please enter a title for your new blog post'
        flash(title_error, 'error')

    if body is '':
        body_error = 'Please enter a body for your new blog post'
        flash(body_error, 'error')

    if not title_error and not body_error:
        owner = User.query.filter_by(username=session['username']).first()
        blog = Blog(blog_title, body, owner)
        db.session.add(blog)
        db.session.commit()
        blog_id = blog.id

        return redirect('/blog?id={0}'.format(blog_id))

    else:
        return render_template('newPost.html', blog_title=blog_title, body=body)



@app.route('/index')
def index():

    users = User.query.all()

    return  render_template("index.html", users=users)





app.secret_key = b'\x13\x0eW\xf3s\xc9\xfa\xc7\x8d\xa2h\xd9x\xd70l\xff\xca\xe6[f\xd0\x14\x1b'


if __name__ == '__main__':
    app.run()

