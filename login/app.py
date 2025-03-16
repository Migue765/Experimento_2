from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

@app.route('/generate_token', methods=['POST'])
def generate_token():
    data = request.get_json()
    admin_status = True if data['user'] == 'admin' else False
    token = jwt.encode({
        'user': data['user'],
        'admin': admin_status,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})

@app.route('/validate_token', methods=['POST'])
def validate_token():
    token = request.get_json().get('token')
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'valid': True})
    except jwt.ExpiredSignatureError:
        return jsonify({'valid': False, 'error': 'Token expired'})
    except jwt.InvalidTokenError:
        return jsonify({'valid': False, 'error': 'Invalid token'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)