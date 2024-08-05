from flask import Flask, render_template, request, redirect, url_for, session
import sys
import os
import importlib.util

# Define the correct relative path to user_db.py
current_dir = os.path.dirname(__file__)
user_db_path = os.path.join(current_dir, 'pythonscripts/user_db.py')

# Ensure the path is absolute
user_db_path = os.path.abspath(user_db_path)

# Load the module from the specified path
spec = importlib.util.spec_from_file_location("user_db", user_db_path)
user_db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(user_db)

app = Flask(__name__, template_folder='pages', static_folder='assets')
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a strong secret key

# Route for the index page (landing page)
@app.route('/')
def index():
    return render_template('index.html')

# Route for the login page
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the CSV
        user = user_db.check_user_exists(email)

        if user:
            # Now verify the password
            if user['password'] == password:
                session['username'] = f"{user['firstname']} {user['lastname']}"
                # Redirect to the homepage with user details
                return redirect(url_for('homepage', firstname=user['firstname'], lastname=user['lastname'], username=user['username']))
            else:
                error = "Invalid password. Please try again."
        else:
            error = "User not found. Please sign up first."

    return render_template('login.html', error=error)

# Route for the signup page
@app.route('/signup.html', methods=['GET', 'POST'])
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
        if not user_db.validate_username(username):
            error = "Username should contain only alphabets and underscores."
            return render_template('signup.html', error=error)

        # Validate password strength
        if not user_db.is_valid_password(password):
            error = "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
            return render_template('signup.html', error=error)

        # Check if the user already exists
        if user_db.is_duplicate_email(email):
            error = "User already exists. Please log in."
            return redirect(url_for('login'))

        # Proceed with signup if validations pass
        signup_response = user_db.signup_user(firstname, lastname, email, username, password)
        
        if signup_response["status"] == "success":
            user = signup_response["user"]
            session['username'] = f"{user['firstname']} {user['lastname']}"
            # Redirect to the homepage with user details
            return redirect(url_for('homepage', firstname=user['firstname'], lastname=user['lastname'], username=user['username']))
        else:
            error = signup_response["message"]
            return render_template('signup.html', error=error)

    return render_template('signup.html')

# Route for the homepage
@app.route('/homepage.html')
def homepage():
    if 'username' in session:
        firstname = request.args.get('firstname')
        lastname = request.args.get('lastname')
        username = request.args.get('username')
        return render_template('homepage.html', firstname=firstname, lastname=lastname, username=username)
    else:
        return redirect(url_for('login'))

# Route for the forgot password page
@app.route('/forgot_password.html', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = user_db.check_user_exists(email)

        if user:
            # Logic to send a reset link to the user's email would go here
            return redirect(url_for('password_reset', email=email))
        else:
            error = "Email not found. Please try again."
            return render_template('forgot_password.html', error=error)
    
    return render_template('forgot_password.html')

# Route for the password reset page
@app.route('/password_reset.html')
def password_reset():
    email = request.args.get('email')
    return render_template('password_reset.html', email=email)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
