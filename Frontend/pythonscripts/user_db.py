import csv
import os
import re

def is_valid_email(email):
    # Regex pattern for validating an email address
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    # Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$'
    return re.match(pattern, password) is not None

def is_duplicate_email(email, filename='userdb.csv'):
    if not os.path.isfile(filename):
        return False

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['email'].lower() == email.lower():
                return True
    return False

def create_csv_with_default_user(filename='userdb.csv'):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['firstname', 'lastname', 'email', 'username', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Add a default user
        writer.writerow({
            'firstname': 'Default',
            'lastname': 'User',
            'email': 'defaultuser@example.com',
            'username': 'default_user',
            'password': 'Default@123'
        })
    print("CSV file created with a default user.")

def signup_user(firstname, lastname, email, username, password):
    filename = 'userdb.csv'

    # Create CSV with default user if it doesn't exist
    if not os.path.isfile(filename):
        create_csv_with_default_user(filename)

    # Email validation
    if not is_valid_email(email):
        return {"status": "error", "message": "Invalid email address. Please enter a valid email."}

    # Password validation
    if not is_valid_password(password):
        return {"status": "error", "message": "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one digit, and one special character."}

    # Check for duplicate email
    if is_duplicate_email(email, filename):
        return {"status": "error", "message": f"An account with the email {email} already exists. Please use a different email."}

    # Proceed with signup if validations pass
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['firstname', 'lastname', 'email', 'username', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        user_data = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'username': username,
            'password': password
        }
        writer.writerow(user_data)

    print(f"User {firstname} {lastname} has been successfully signed up!")
    return {"status": "success", "user": user_data}

def check_user_exists(email, filename='userdb.csv'):
    if not os.path.isfile(filename):
        return None

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f"Checking user: {row}")  # Debugging line to see the content of each row
            if row['email'].lower() == email.lower():
                print(f"User found: {row}")  # Debugging line to confirm user found
                return row
    print("User not found")  # Debugging line if no user is found
    return None

def validate_username(username):
    # Validate that the username contains only alphabets and underscores
    return re.match(r'^[A-Za-z_]+$', username) is not None

if __name__ == "__main__":
    # Example usage for testing
    response = signup_user('John', 'Doe', 'johndoe@example.com', 'john_doe', 'SecurePass!123')
    print(response)
