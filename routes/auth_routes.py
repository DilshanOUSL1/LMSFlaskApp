from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import db, User
from flask_bcrypt import Bcrypt

# Create a Blueprint object for auth routes
auth = Blueprint('auth', __name__)

# Create a Bcrypt object for password hashing
bcrypt = Bcrypt()

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # e.g. "student", "instructor", "admin"

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists. Please log in.", "danger")
            return redirect(url_for('auth.register'))

        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # ----- Automatically assign index number for students -----
        if role.lower() == 'student':
            # 1) Query the highest current index_number among students
            last_student = User.query.filter_by(role='student').order_by(User.index_number.desc()).first()

            # 2) Determine the next index number
            if last_student and last_student.index_number:  
                next_index = last_student.index_number + 1
            else:
                next_index = 1  # start numbering at 1 if no students yet

            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                role=role,
                index_number=next_index
            )
        else:
            # For non-student roles, we don't assign an index_number
            new_user = User(
                username=username,
                email=email,
                password=hashed_password,
                role=role
            )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # Store user ID (and maybe role) in session
            session['user_id'] = user.id
            session['user_role'] = user.role

            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
            return redirect(url_for('auth.login'))

    return render_template('login.html')
@auth.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))

