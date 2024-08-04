import csv
import os

def signup_user(firstname, lastname, email, password):
    filename = 'userdb.csv'
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['firstname', 'lastname', 'email', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'password': password
        })

    print(f"User {firstname} {lastname} has been successfully signed up!")
