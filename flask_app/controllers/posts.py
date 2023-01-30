from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.post import Post


@app.route('/create_post', methods = ['POST'])
def save():
    if not Post.validate_post_data(request.form):
        # we redirect to the template with the form.
        return redirect('/success')
    print(request.form)
    data = {
        "user_id": request.form['user_id'],
        "content": request.form['content']
    }
    Post.save(data)
    return redirect('/success')

@app.route('/delete_comment', methods = ['POST'])
def delete():
    Post.delete(request.form)
    return redirect('/success')