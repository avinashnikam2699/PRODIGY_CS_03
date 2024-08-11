from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password', '')
    strength, feedback = evaluate_password(password)
    return jsonify({'strength': strength, 'feedback': feedback})

def evaluate_password(password):
    # Criteria checks
    length_criteria = len(password) >= 8
    uppercase_criteria = any(c.isupper() for c in password)
    lowercase_criteria = any(c.islower() for c in password)
    number_criteria = any(c.isdigit() for c in password)
    special_criteria = any(c in '!@#$%^&*()-_=+[]{};:,.<>?/|\\' for c in password)

    # Calculate points based on criteria
    points = sum([length_criteria, uppercase_criteria, lowercase_criteria, number_criteria, special_criteria])
    
    # Generate feedback
    feedback = []
    if not length_criteria:
        feedback.append('Increase the length to at least 8 characters.')
    if not uppercase_criteria:
        feedback.append('Add at least one uppercase letter.')
    if not lowercase_criteria:
        feedback.append('Add at least one lowercase letter.')
    if not number_criteria:
        feedback.append('Add at least one number.')
    if not special_criteria:
        feedback.append('Add at least one special character.')

    # Determine strength level
    if points <= 2:
        strength = 'Weak'
    elif points == 3:
        strength = 'Fair'
    elif points == 4:
        strength = 'Strong'
    else:
        strength = 'Very Strong'

    return strength, feedback

if __name__ == '__main__':
    app.run(debug=True)
