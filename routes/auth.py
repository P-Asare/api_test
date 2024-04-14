from flask import Blueprint, request, jsonify, session
from utils.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Verify required fields are provided
    if 'email' not in data or 'password' not in data:
        return jsonify({'success': False, 'message': 'Email and password are required fields'}), 400

    email = data['email']
    password = data['password']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        # Check if email address exists
        if not user:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

        # Check if user inputted correct password
        if not check_password_hash(user['password'], password):
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

        # Start user session
        session['user_id'] = user['id']
        session['role'] = user['role_id']

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'session_data': {
                'user_id': user['id'],
                'role': user['role_id']
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    email = data['email']
    fname = data['fname']
    lname = data['lname']
    dob = data['dob']
    password = data['password']
    confirm_password = data['confirm-password']
    role = data['role']
    program = data['program']
    interests = data['interest']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user has an account
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Username already exists'}), 400

        # Confirm that passwords match
        if password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match'}), 400

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert into profile table
        cursor.execute("INSERT INTO profile (program_id) VALUES (%s)", (program,))
        profile_id = cursor.lastrowid

        # Insert into users table
        cursor.execute("INSERT INTO users (email, fname, lname, password, dob, role_id, profile_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                      (email, fname, lname, hashed_password, dob, role, profile_id))
        user_id = cursor.lastrowid

        # Insert user interests
        for interest in interests:
            cursor.execute("INSERT INTO user_interests (user_id, interest_id) VALUES (%s, %s)", (user_id, interest))

        conn.commit()
        return jsonify({'success': True, 'message': 'User registered successfully'})

    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

    finally:
        cursor.close()
        conn.close()