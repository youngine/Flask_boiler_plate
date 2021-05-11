from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for, session
from flask_login import login_user, current_user, logout_user
from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession
import datetime

blog_abtest = Blueprint('blog', __name__)


@blog_abtest.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'GET':
        print('set_email', request.args.get('user_email'))
        return redirect('/blog/blog_fullstack')
        # return redirect(url_for(blog.test_blog))
        # return make_response(jsonify(success=True), 200)
    else:
        # print('set_email', request.headers)
        # content type이 application/json 인경우만 get_json가능
        # print('set_email', request.get_json())
        # print('set_email', request.form['user_email'])
        # print('blog_id', request.form['blog_id'])

        user = User.create(request.form['user_email'], request.form['blog_id'])
        # https://docs.python.org/3/library/datetime.html
        login_user(user, remember=True, duration=datetime.timedelta(days=365))
        return redirect('/blog/blog_fullstack')


@blog_abtest.route('/blog_fullstack')
def blog_fullstack1():
    if current_user.is_authenticated:
        webpage_name = BlogSession.get_blog_page(current_user.blog_id)
        BlogSession.save_session_info(
            session['client_id'], current_user.user_email, webpage_name)
        return render_template(webpage_name, user_email=current_user.user_email)
    else:
        webpage_name = BlogSession.get_blog_page()
        BlogSession.save_session_info(
            session['client_id'], 'anonymous', webpage_name)
        return render_template(webpage_name)


@blog_abtest.route('/logout')
def logout():
    # 인자없이도 current user이용 알아서 체크
    User.delete(current_user.id)
    logout_user()
    return redirect('/blog/blog_fullstack')
