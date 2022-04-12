from flask import Blueprint, render_template, request, redirect, url_for
from website import views

from website.models import User, Result
from website.publish import publish_result
from . import db
import pika

from dotenv import load_dotenv
import os 
load_dotenv()


auth = Blueprint('auth', __name__)
@auth.route('/signin/', methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        roll = request.form.get('roll')
        password = request.form.get('password')
        user = User.query.filter_by(roll=roll).first()
        if user:
            if user.password == password:
                return redirect(url_for('auth.dash', roll=roll))

    return render_template("signin.html")

@auth.route('/signup/',  methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        roll = request.form.get('roll')
        section = request.form.get('section')
        password = request.form.get('password')

        new_user =  User(roll=roll, section=section, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('views.home'))
    

    return render_template("signup.html")

@auth.route('/produce/', methods=['GET','POST'])
def produce():
    if request.method == 'POST':
        roll = request.form.get('roll')
        result = request.form.get('result')

        publish_result(result=result,roll=roll)
    return render_template("pro.html")


@auth.route('/dash/', methods=['GET','POST'])
def dash():
    roll = request.args.get('roll')
    result = Result.query.filter_by(roll=roll).first()
    curr_res = ""
    if result:
        curr_res = result.result
    return render_template("dash.html", roll = roll , res = curr_res)