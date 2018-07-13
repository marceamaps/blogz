from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/build-a-blog' 
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(2000))

    def __init__(self, title, content):
        self.title = title
        self.content = content


@app.route('/blog', methods=['POST', 'GET'])
def index():

    # if request.method == 'POST':
    #     blog_title = request.form['blog_title']
    #     blog_content = request.form['blog_content']
    #     new_blog_title = Blog(blog_title, blog_content)

    #     db.session.add(new_blog_title)
        
    #     db.session.commit()

    #     return redirect ('/blog')

    blogs = Blog.query.all()
    return render_template('blog.html', title="Build a Blog!", blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_content = request.form['blog_content']
        new_blog_title = Blog(blog_title, blog_content)

        db.session.add(new_blog_title)
        
        db.session.commit()

        return redirect ('/blog')

    blogs = Blog.query.all()

    return render_template('newpost.html', title="Build a Blog!")

@app.route('/individual_blog', methods=['POST', 'GET'])

    blog_title = request.form['blog_title'
    blog_content = request.form['blog_content']

    # task_id = int(request.form['task-id'])
    # task = Task.query.get(task_id)
    # db.session.add(task)
    # db.session.commit()

    return render_template('individual_blogs.html', title=title, blog=blog)


if __name__ == '__main__':
    app.run()