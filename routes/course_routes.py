from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.models import db, User, Course, Enrollment  # Adjust as needed
from flask_bcrypt import Bcrypt  # Only if needed for password hashing

course_bp = Blueprint('course_bp', __name__)

@course_bp.route('/add_course', methods=['POST'])
def add_course():
    # Ensure user is logged in
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('auth.login'))

    # Check if user is instructor or admin
    user_role = session.get('user_role', None)
    if user_role not in ['admin', 'instructor']:
        flash("Access denied. Only admin or instructor can add courses.", "danger")
        return redirect(url_for('dashboard'))

    # Handle the POST request to add a course
    course_name = request.form.get('course_name')
    course_description = request.form.get('course_description')

    if not course_name:
        flash("Please enter a course name.", "danger")
        return redirect(url_for('enrollment_bp.view_courses'))  # Redirect to view_courses if validation fails

    new_course = Course(
        name=course_name,
        description=course_description if course_description else ""
    )
    db.session.add(new_course)
    db.session.commit()

    flash(f"Course '{course_name}' added successfully!", "success")
    return redirect(url_for('enrollment_bp.view_courses'))  # Redirect to view_courses

