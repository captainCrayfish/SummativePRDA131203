"""
Flask User Profile Management Application

This application allows users to register, view, and edit their user profiles.
User data is stored in a SQLite database with input validation and error handling.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask application
app = Flask(__name__)

# Configure the SQLite database
# The database file will be stored in the instance folder
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Initialize SQLAlchemy for database management
db = SQLAlchemy(app)


# Database model for User profiles
class User(db.Model):
    """
    User model represents a user profile in the database.
    
    Attributes:
        id: Primary key, auto-incremented unique identifier
        username: Unique username, required field
        email: User's email address, required field
        first_name: User's first name
        last_name: User's last name
        bio: User's biographical information
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.Text, default='')

    def __repr__(self):
        return f'<User {self.username}>'


# Helper function to validate form input
def validate_user_input(data):
    """
    Validates user input from the registration/edit forms.
    
    This function checks that all required fields are provided and contain
    valid data. It returns a tuple (is_valid, error_message).
    
    Args:
        data: Dictionary containing form data
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    # Check if all required fields are present and not empty
    required_fields = ['username', 'email', 'first_name', 'last_name']
    
    for field in required_fields:
        if field not in data or not data[field].strip():
            return False, f"Field '{field.replace('_', ' ')}' is required."
    
    # Validate email format - check for @ symbol and domain
    if '@' not in data['email'] or '.' not in data['email'].split('@')[1]:
        return False, "Please enter a valid email address."
    
    # Validate username - minimum 3 characters
    if len(data['username'].strip()) < 3:
        return False, "Username must be at least 3 characters long."
    
    return True, ""


# Route for the homepage/index page
@app.route('/')
def index():
    """
    Display the homepage with a list of all registered users.
    """
    users = User.query.all()
    return render_template('index.html', users=users)


# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration. 
    
    GET: Display the registration form
    POST: Process the registration form data
    """
    if request.method == 'POST':
        # Extract form data from the POST request
        form_data = {
            'username': request.form.get('username', ''),
            'email': request.form.get('email', ''),
            'first_name': request.form.get('first_name', ''),
            'last_name': request.form.get('last_name', ''),
            'bio': request.form.get('bio', '')
        }
        
        # Validate the form data using the validation function
        is_valid, error_msg = validate_user_input(form_data)
        
        if not is_valid:
            flash(error_msg, 'error')
            return render_template('register.html', form_data=form_data)
        
        # Check if username already exists in the database
        existing_user = User.query.filter_by(username=form_data['username']).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return render_template('register.html', form_data=form_data)
        
        # Check if email already exists in the database
        existing_email = User.query.filter_by(email=form_data['email']).first()
        if existing_email:
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('register.html', form_data=form_data)
        
        try:
            # Create a new User object with the validated form data
            new_user = User(
                username=form_data['username'],
                email=form_data['email'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                bio=form_data['bio']
            )
            
            # Add the new user to the database session and commit
            db.session.add(new_user)
            db.session.commit()
            
            flash(f'User {form_data["username"]} registered successfully!', 'success')
            return redirect(url_for('index'))
        
        except Exception as e:
            # Rollback the transaction if an error occurs
            db.session.rollback()
            flash(f'An error occurred during registration: {str(e)}', 'error')
    
    return render_template('register.html')


# Route to view a user's profile
@app.route('/profile/<int:user_id>')
def view_profile(user_id):
    """
    Display a specific user's profile.
    
    Args:
        user_id: The ID of the user to display
    """
    # Query the database for the user with the specified ID
    user = User.query.get(user_id)
    
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('index'))
    
    return render_template('profile.html', user=user)


# Route to edit a user's profile
@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    """
    Handle user profile editing.
    
    GET: Display the edit form with preloaded user data
    POST: Process the edited profile data
    
    Args:
        user_id: The ID of the user to edit
    """
    # Retrieve the user from the database
    user = User.query.get(user_id)
    
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Extract updated form data from the POST request
        form_data = {
            'username': request.form.get('username', ''),
            'email': request.form.get('email', ''),
            'first_name': request.form.get('first_name', ''),
            'last_name': request.form.get('last_name', ''),
            'bio': request.form.get('bio', '')
        }
        
        # Validate the updated form data
        is_valid, error_msg = validate_user_input(form_data)
        
        if not is_valid:
            flash(error_msg, 'error')
            return render_template('edit_profile.html', user=user, form_data=form_data)
        
        # Check if the new username is already taken by another user
        if form_data['username'] != user.username:
            existing_user = User.query.filter_by(username=form_data['username']).first()
            if existing_user:
                flash('Username already exists. Please choose a different username.', 'error')
                return render_template('edit_profile.html', user=user, form_data=form_data)
        
        # Check if the new email is already taken by another user
        if form_data['email'] != user.email:
            existing_email = User.query.filter_by(email=form_data['email']).first()
            if existing_email:
                flash('Email already registered. Please use a different email.', 'error')
                return render_template('edit_profile.html', user=user, form_data=form_data)
        
        try:
            # Update the user's profile with the new data
            user.username = form_data['username']
            user.email = form_data['email']
            user.first_name = form_data['first_name']
            user.last_name = form_data['last_name']
            user.bio = form_data['bio']
            
            # Commit the changes to the database
            db.session.commit()
            flash(f'Profile updated successfully!', 'success')
            return redirect(url_for('view_profile', user_id=user.id))
        
        except Exception as e:
            # Rollback the transaction if an error occurs
            db.session.rollback()
            flash(f'An error occurred while updating the profile: {str(e)}', 'error')
    
    return render_template('edit_profile.html', user=user)


# Route to delete a user's profile
@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_profile(user_id):
    """
    Delete a user's profile from the database.
    
    Args:
        user_id: The ID of the user to delete
    """
    user = User.query.get(user_id)
    
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('index'))
    
    try:
        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f'User {username} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while deleting the user: {str(e)}', 'error')
    
    return redirect(url_for('index'))


# Error handler for 404 (page not found)
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template('404.html'), 404


# Error handler for 500 (internal server error)
@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    db.session.rollback()
    return render_template('500.html'), 500


# Application entry point
if __name__ == '__main__':
    # Create the database tables
    with app.app_context():
        db.create_all()
    
    # Run the Flask development server
    app.run(debug=True)
