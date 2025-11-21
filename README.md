# User Profile Manager - Flask Application

A comprehensive Flask web application for managing user profiles with registration, viewing, and editing capabilities.

## Features

- **User Registration**: Register new users with full validation
- **Profile Viewing**: View detailed user profile information
- **Profile Editing**: Edit existing user profiles with preloaded data
- **Profile Deletion**: Remove user profiles from the database
- **SQLite Database**: All user data is stored persistently in SQLite
- **Input Validation**: Manual validation for all required fields
- **Error Handling**: Comprehensive error handling and user feedback
- **Responsive Design**: Mobile-friendly interface with modern CSS styling

## Requirements

- Python 3.7 or higher
- Flask 2.3.2
- Flask-SQLAlchemy 3.0.5
- SQLAlchemy 2.0.19

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd profileapp
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   ```

   On Windows:
   ```bash
   venv\Scripts\activate
   ```

   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask development server:**
   ```bash
   python app.py
   ```

2. **Open your web browser and navigate to:**
   ```
   http://localhost:5000
   ```

## Application Structure

```
profileapp/
├── app.py                 # Main Flask application with routes and database models
├── requirements.txt       # Project dependencies
├── users.db              # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation and footer
│   ├── index.html        # Homepage displaying all users
│   ├── register.html     # User registration form
│   ├── profile.html      # User profile view
│   ├── edit_profile.html # Edit profile form
│   ├── 404.html          # Page not found error
│   └── 500.html          # Server error page
└── static/               # Static files
    └── style.css         # Main stylesheet
```

## Usage Guide

### Registering a New User

1. Click **"Register"** in the navigation menu
2. Fill in all required fields:
   - **Username** (minimum 3 characters, must be unique)
   - **Email** (must be in valid email format, must be unique)
   - **First Name** (required)
   - **Last Name** (required)
   - **Bio** (optional)
3. Click **"Register User"** to create the account
4. You'll be redirected to the home page with a success message

### Viewing a Profile

1. On the home page, locate the user you want to view
2. Click the **"View Profile"** button on their user card
3. The profile page displays all user information

### Editing a Profile

1. Click the **"Edit"** button on a user's card or on their profile page
2. The form will be preloaded with the current user data
3. Make the desired changes
4. Click **"Save Changes"** to update the profile
5. You'll be redirected back to the profile page with a success message

### Deleting a Profile

1. On the home page, click the **"Delete"** button on a user's card
2. Confirm the deletion when prompted
3. The user will be removed from the database

## Input Validation

The application performs manual validation on all form submissions:

1. **Required Fields**: Checks that all required fields are not empty
2. **Username**: Must be at least 3 characters long and unique
3. **Email**: Must be in valid format (contains @ and .) and unique
4. **First Name & Last Name**: Must not be empty
5. **Duplicate Prevention**: Prevents duplicate usernames and emails

## Database Schema

### Users Table

| Column      | Type    | Constraints        |
|-------------|---------|-------------------|
| id          | Integer | Primary Key       |
| username    | String  | Unique, Not Null  |
| email       | String  | Unique, Not Null  |
| first_name  | String  | Not Null          |
| last_name   | String  | Not Null          |
| bio         | Text    | Default: ''       |

## Code Documentation

The application includes comprehensive inline comments explaining:

- Database model structure and relationships
- Input validation logic
- Route handlers and their purposes
- Error handling and recovery
- Form data processing and storage

### Key Components with Documentation

1. **validate_user_input()** - Input validation helper function
2. **User Model** - Database model with field descriptions
3. **register() Route** - Form submission and validation logic
4. **edit_profile() Route** - Form preloading and update logic
5. **Database Operations** - Transaction handling and error recovery

## Error Handling

The application includes:

- **Form Validation Errors**: Displayed as alert messages
- **Database Errors**: Caught and rolled back with user feedback
- **404 Errors**: Custom page for routes that don't exist
- **500 Errors**: Custom page for server errors

## Features Implemented

✓ User registration with form validation  
✓ Profile viewing with dynamic data display  
✓ Profile editing with preloaded form data  
✓ Manual field validation  
✓ SQLite database for persistent storage  
✓ Input validation (5+ inline/block comments)  
✓ Error handling and user feedback  
✓ Responsive design  
✓ Professional UI with CSS styling  

## Troubleshooting

### Database Issues
If you encounter database errors, delete the `users.db` file and restart the application. The database will be recreated automatically.

### Port Already in Use
If port 5000 is already in use, you can change it in `app.py`:
```python
app.run(debug=True, port=5001)  # Use port 5001 instead
```

### Module Import Errors
Make sure you've installed all required packages:
```bash
pip install -r requirements.txt
```

## Development

To modify the application:

1. Edit `app.py` for backend logic and routes
2. Edit templates in the `templates/` folder for HTML structure
3. Edit `static/style.css` for styling
4. The development server will auto-reload when files are changed (with `debug=True`)

## Notes

- This is a development application. For production, change `debug=True` to `debug=False`
- Change the `SECRET_KEY` value in `app.py` to a secure random string
- Consider adding password hashing for production use
- The database file (`users.db`) will be created automatically in the project directory

## License

This project is provided as-is for educational purposes.
