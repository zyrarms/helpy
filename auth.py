import re
from flask import Blueprint, render_template, url_for,  request, flash, redirect
from werkzeug.utils import redirect
from .models import Admin, User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)



# USER LOGIN
@auth.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
        
    return render_template("login.html", user=current_user)

# USER REGISTRATION
@auth.route('/register', methods = ['GET', 'POST'])
def register():   
    if request.method == 'POST':
        firstname = request.form.get('signup_first_name')
        lastname = request.form.get('signup_last_name')
        email = request.form.get('signup_email')
        password = request.form.get('signup_password')
        cpassword = request.form.get('signup_cpassword')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif password != cpassword:
            flash('Password and confirm password does not match.', category='error')
        else:
            new_user = User(firstname=firstname, lastname=lastname, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    return render_template("signup.html", user=current_user)

# FORGET PASSWORD - USER
@auth.route('/forgotpassword', methods = ['GET', 'POST'])
def forgotpassword(): 
    if request.method == "POST":
        email_text = request.form['emailr']
        pword = request.form['new_password']
        cpword = request.form['cpassword']

        if pword != cpword:
            flash('Password and Confirm password does not match.', category='error')
            return redirect(url_for('auth.forgotpassword'))
        else:
            user = User.query.filter_by(email=email_text).first()
            user.password = generate_password_hash(pword, method='sha256')
        
            # update database
            try:
                db.session.commit()
                flash('Update password successfully!', category= 'success')
                return redirect(url_for('auth.login'))
            except:
                return 'ERROR'
    else:
        return render_template("forgotpassword.html")


    

# LOGOUT USER
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# ADMIN LOGIN
@auth.route('/adminlogin', methods = ['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        admin = Admin.query.filter_by(username=username).first()
        if admin:
            if check_password_hash(admin.password, password):
                login_user(admin, remember=True)
                return redirect(url_for('views.dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Username does not exist.', category='error')
        
    return render_template("admin_login.html", user=current_user)



# LOGOUT ADMIN
@auth.route('/logoutadmin')
@login_required
def adminlogout():
    logout_user()
    return redirect(url_for('auth.admin'))