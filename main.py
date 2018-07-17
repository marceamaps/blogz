from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
# from hashutils import make_pw_hash, check_pw_hash
# from validate_email import validate_email

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/blogz' 
db = SQLAlchemy(app)
#do I need a secret key?

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(100))
    blogs = db.relationship('Blog', backref='owner')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        # to do - validate users data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            flash("The email <strong>{0}</strong> is already registered".format(username), 'danger')

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and password:
            session['username'] = username
            flash("Logged in", 'info')
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'danger')

    return render_template('login.html')

@app.route('/blogs', methods=['POST', 'GET'])
def index():

    blogs = Blog.query.all()
    return render_template('blog.html', title="Build a Blog!", blogs=blogs)

# def logout():

# We'll have a logout function that handles a POST request to 
# /logout and redirects the user to /blog after deleting the 
# username from the session.

# @app.route('index')
# def index():

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']
        new_blog_title = Blog(title=blog_title, content=blog_content)

        db.session.add(new_blog_title)
        
        db.session.commit()

        return redirect ('/blog')

    blogs = Blog.query.all()

    return render_template('newpost.html', title="Build a Blog!")

@app.route('/individual_blog/<blog_id>', methods=['POST', 'GET'])
def individual_post(blog_id):

    #get the blog from the database using the ID!!!!
    blog_id = Blog.query.filter_by(id=blog_id).first()
    indi_title = blog_id.title
    indi_content = blog_id.content 
    
    return render_template('individual_blogs.html', title=indi_title, content=indi_content)



if __name__ == '__main__':
    app.run()