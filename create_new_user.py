import bcrypt
import pyodbc
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Establish a connection to the database
server = 'localhost'
database = 'APIchallange'
username = 'said'
password = 'said'
driver = 'SQL Server'  # The ODBC driver for SQL Server
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# Function to create a user
def create_user(name, password):
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Insert the user into the database along with the hashed password
    cursor.execute("INSERT INTO User1 (name, password_hash) VALUES (?, ?)", (name, password_hash))
    connection.commit()
    print("User created successfully.")

# Route to display the registration form
@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')

# Route to handle the registration form submission
@app.route('/register', methods=['POST'])
def register():
    # Get the submitted username and password from the form
    username = request.form.get('username')
    password = request.form.get('password')

    # Create the user
    create_user(username, password)

    # Redirect the user to the index page
    return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
