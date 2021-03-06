from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
# from hashutils import make_pw_hash, check_pw_hash
# from validate_email import validate_email

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/blogz' 
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B' #stole this from get-it-done, can I do that?

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
        
        existing_user = User.query.filter_by(username=username).first()

        if not username:
            flash('One or more fields is empty')
        elif not password:
            flash('One or more fields is empty')
        elif not verify:
            flash('One or more fields is empty')
        elif password != verify:
            flash('Passwords do not match')
        elif existing_user is True: 
            flash('That username already exists')
        elif len(username) < 3 or len(username) > 20:
            flash('Please make the username between 3-20 characters') 
        else:
            if not existing_user:
                new_user = User(username=username, password=password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')

    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and (user.password == password):
            session['username'] = username
            flash("Logged in", 'info')
            return redirect('/newpost')
        elif user and (user.password != password):
            flash('User password incorrect, please try again', 'danger')
        else:
            if not user:
                flash('User does not exist, please signup')
                return redirect('/signup')

    return render_template('login.html')


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blogs', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect ('/login')

@app.route('/blog', methods=['POST', 'GET'])
def blogs():

    blogs = Blog.query.all()
    users = User.query.all()

    return render_template('blog.html', blogs=blogs, users=users)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['username']
    return redirect('/blog')


@app.route('/', methods=['POST', 'GET'])
def index():

    users = User.query.all()
    return render_template('index.html')


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']
        new_blog_title = Blog(title=blog_title, content=blog_content)

        db.session.add(new_blog_title)
        
        db.session.commit()

        blog_id = new_blog_title.id

        return redirect ('/blog/' + str(blog_id))

    blogs = Blog.query.all()

    return render_template('newpost.html', title="Build a Blog!")

@app.route('/blog/<blog_id>', methods=['POST', 'GET'])
def individual_post(blog_id):

    #get the blog from the database using the ID!!!!
    blog_id = Blog.query.filter_by(id=blog_id).first()
    indi_title = blog_id.title
    indi_content = blog_id.content 
    
    return render_template('individual_blogs.html', title=indi_title, content=indi_content)



if __name__ == '__main__':
    app.run()