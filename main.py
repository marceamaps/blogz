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

    def __init__(self, title):
        self.title = title
        #self.content = content


@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        new_blog_title = Blog(blog_title)
        db.session.add(new_blog_title)

        blog_content = request.form['blog_content']
        new_blog_content = Blog(blog_content)
        db.session.add(new_blog_content)

        db.session.commit()

    blogs = Blog.query.all()
    contents = Blog.query.all()
    return render_template('blog.html',title="Build a Blog!", blogs=blogs, contents=contents)


# @app.route('/newpost', methods=['POST'])
# def delete_task():

#     task_id = int(request.form['task-id'])
#     task = Task.query.get(task_id)
#     db.session.add(task)
#     db.session.commit()

#     return redirect('/')


if __name__ == '__main__':
    app.run()