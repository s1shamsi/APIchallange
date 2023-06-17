import re
from flask import Flask, request, jsonify, render_template, redirect

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == "admin" and password == "admin":
        return redirect('/index.html')
    else:
        error_message = "Invalid username or password."
        return render_template('login.html', error_message=error_message)

@app.route('/index.html')
def index():
    input_str = request.args.get('str')
    if input_str is None:
        result = []  # Set result to an empty list
    else:
        result = convertMeasurements(input_str)

    return render_template('index.html', result=result)

@app.route('/convert')
def convert_measurements():
    input_str = request.args.get('str')
    result = convertMeasurements(input_str)

    return jsonify(result=result)

def convertMeasurements(string):
    collected_values = []
    if isValidSeq(string):
        is_new_number = True
        is_val_after_z = False
        total_z_values = 0
        round_length = 0
        round_itr = 0
        round_total = 0
        char_val = 0
        for i in range(len(string)):
            char = string[i]
            if char == "_":
                char_val = 0
                if is_val_after_z:
                    char_val += total_z_values
                    total_z_values = 0
                    is_val_after_z = False
            elif char == "z":
                is_val_after_z = True
                total_z_values += char_val
                continue
            else:
                char_val = ord(char) - 96
                if is_val_after_z:
                    char_val += total_z_values
                    total_z_values = 0
                    is_val_after_z = False
            if not is_new_number:
                round_total += char_val
                round_itr += 1
            else:
                round_length = char_val
                round_total = 0
                round_itr = 0
                is_new_number = False
            if round_itr == round_length:
                collected_values.append(round_total)
                is_new_number = True
            if i == len(string) - 1 and round_itr != round_length:
                collected_values.append(0)
    return collected_values

def isValidSeq(string):
    pattern = "^[a-z_]+$"
    match = re.match(pattern, string)
    return match

if __name__ == '__main__':
    app.debug = True
    app.run()
