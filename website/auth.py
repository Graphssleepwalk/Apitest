from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort, Response, session, make_response, json
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__) #creating a blueprint for the auth.py file


@auth.route('/login', methods=['GET', 'POST'])#this is the route for the login page
def login():#this is the function for the login page
    if request.method == 'POST':#if the request is a POST request
        email = request.form.get('email')#get the email from the form
        password = request.form.get('password')#get the password from the form

        user = User.query.filter_by(email=email).first()#query the database for the user with the email
        if user:#if the user exists
            if check_password_hash(user.password, password):#if the password is correct
                flash('Logged in successfully!', category='success')#flash a message
                login_user(user, remember=True)#login the user
                return redirect(url_for('views.home'))#redirect the user to the home page
            else:#if the password is incorrect
                flash('Incorrect password, try again.', category='error')#flash a message
        else:#if the user does not exist
            flash('Email does not exist.', category='error')#flash a message

    return render_template("login.html", user=current_user)#render the login page


@auth.route('/logout')#this is the route for the logout page
@login_required#this means that the user must be logged in to access this page
def logout():#this is the function for the logout page
    logout_user()#logout the user
    return redirect(url_for('auth.login'))#redirect the user to the login page


@auth.route('/sign-up', methods=['GET', 'POST'])#this is the route for the sign up page
def sign_up():#this is the function for the sign up page
    if request.method == 'POST':#if the request is a POST request
        email = request.form.get('email')#get the email from the form
        first_name = request.form.get('firstName')#get the first name from the form
        password1 = request.form.get('password1')#get the first password from the form
        password2 = request.form.get('password2')#get the second password from the form

        user = User.query.filter_by(email=email).first()#query the database for the user with the email
        if user:#if the user exists
            
            return jsonify({'exist' : True})#return a json response   
        else:#if the user does not exist
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'))#create a new user
            db.session.add(new_user)#add the new user to the database
            db.session.commit()#commit the changes to the database
            login_user(new_user, remember=True)#login the user
            flash('Account created!', category='success')#flash a message
            return jsonify({'exist': False, 'redirect_url': url_for('views.home')})


    return render_template("sign_up.html", user=current_user)#render the sign up page