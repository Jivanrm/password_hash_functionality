from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# File where user data is stored
USER_DATA_FILE = 'users.json'

# Function to load user data from JSON file
def load_users():
    """Load users from the JSON file. Return an empty dict if file not found."""
    try:
        with open(USER_DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Function to save user data to JSON file
def save_users(users):
    """Save the user data (dictionary) to the JSON file."""
    with open(USER_DATA_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Route for the home page (redirects to login or dashboard)
@app.route('/')
def home():
    """Redirect to dashboard if logged in, otherwise to login page."""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Load existing users
        users = load_users()

        # Check if username exists and password is correct
        if username in users and check_password_hash(users[username], password):
            session['username'] = username  # Store username in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

# Route for the sign-up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user sign-up."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Load existing users
        users = load_users()

        # Check if username already exists
        if username in users:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Save new user with hashed password
            users[username] = generate_password_hash(password)
            save_users(users)
            flash('Signup successful! You can now login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html')

# Route for the user dashboard (only accessible after login)
@app.route('/dashboard')
def dashboard():
    """Display the user's dashboard."""
    if 'username' not in session:
        flash('You need to log in first!', 'danger')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', username=session['username'])

# Route for logging out
@app.route('/logout')
def logout():
    """Log the user out and clear the session."""
    session.pop('username', None)  # Remove username from session
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Start the application
if __name__ == '__main__':
    app.run(debug=True)
