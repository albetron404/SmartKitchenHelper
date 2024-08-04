from flask import Flask, render_template, request, redirect, url_for, session
import sys
import csv
import os
import re

# Set the path to include pythonscripts directory for importing
sys.path.append('../pythonscripts')

# Create Flask app and specify the template and static folders
app = Flask(__name__, template_folder='pages', static_folder='assets')
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a strong secret key

# Function to check if user already exists
def check_user_exists(email):
    filename = os.path.join(os.path.dirname(__file__), '../userdb.csv')
    if not os.path.isfile(filename):
        return None

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Case-insensitive email check
            if row['email'].lower() == email.lower():
                return row
    return None

# Function to validate password strength
def validate_password(password):
    # Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
    if re.match(pattern, password):
        return True
    return False

# Function to validate username
def validate_username(username):
    # Username should only contain alphabets and underscores
    pattern = r'^[A-Za-z_]+$'
    return re.match(pattern, username) is not None

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        # Check if passwords match
        if password != confirm_password:
            error = "Passwords do not match!"
            return render_template('signup.html', error=error)

        # Validate username
        if not validate_username(username):
            error = "Username should contain only alphabets and underscores."
            return render_template('signup.html', error=error)

        # Validate password strength
        if not validate_password(password):
            error = "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            return render_template('signup.html', error=error)

        # Check if the user already exists
        if check_user_exists(email):
            error = "User already exists. Please log in."
            return render_template('signup.html', error=error)

        # Logic to save the new user in the database or CSV
        with open('../userdb.csv', 'a', newline='') as csvfile:
            fieldnames = ['firstname', 'lastname', 'email', 'username', 'password']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'firstname': firstname,
                'lastname': lastname,
                'email': email.lower(),  # Save email in lowercase
                'username': username,
                'password': password
            })

        return redirect(url_for('login'))  # Redirect to the login page after successful signup

    return render_template('signup.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the CSV
        user = check_user_exists(email)

        if user:
            # Now verify the password
            if user['password'] == password:
                session['username'] = f"{user['firstname']} {user['lastname']}"
                return redirect(url_for('index'))
            else:
                error = "Invalid password. Please try again."
        else:
            error = "User not found. Please sign up first."

    return render_template('login.html', error=error)

# Route for the index page (after login)
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# Route for the forgot password page
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # Process the forgot password request
        email = request.form['email']
        # Logic to send a reset link to the user's email would go here
        return redirect(url_for('login'))  # Redirect back to login after processing
    
    return render_template('forgot_password.html')

# Other routes can be added here...

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
